from itertools import permutations
from neo4j import GraphDatabase
import ast
from flask import Flask, request, jsonify
from Node_icons import get_node_icon


'''
Request from API input body json e.g:

1) {
    "database": "alidata",
    "username": "neo4j",
    "password": "123456789",
    "URI": "bolt://localhost:7687",
    "Data": [
        {
            "node_id": "547"
        },
        {
            "node_id": "552"
        },
        {
            "node_id": "610"
        }
    ],
    "depth": "0",
    "limit": "140"
}



2) 
{
    "database": "alidata",
    "username": "neo4j",
    "password": "123456789",
    "URI": "bolt://localhost:7687",
    "Data": [
{
            "table": "Person",
            "property": "CNIC",
            "propertyvalue": "5551077777"
        },
        {
            "table": "Person",
            "property": "CNIC",
            "propertyvalue": "5557999999"
        },
        {
            "table": "Person",
            "property": "CNIC",
            "propertyvalue": "2554464646"
}
    ],
    "depth": "0",
    "limit": "140"
}

'''


def create_node_data(node, labels, properties):
    node_data = {
        "id": node.id,
        "label": labels[0],
        "properties": {prop: node[prop] for prop in properties}
    }
    return node_data

def create_edge_data(linked_graph):
    edges = []
    for i in range(len(linked_graph)-1):
        edge = {
            "source": linked_graph[i].start.id,
            "target": linked_graph[i].end.id,
            "type": linked_graph[i].type
        }
        edges.append(edge)
    return edges

def find_shortest_paths_by_ids(uri, user, password, data,database):
    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        linked_graphs = []
        
        for perm in permutations(data):
            match_clauses = []

            for index, item in enumerate(perm):
                if "node_id" in item:
                    node_id = int(item["node_id"])
                    match_clauses.append(f"(node{index}) WHERE id(node{index}) = {node_id}")

            match_clause = " MATCH ".join(match_clauses)
            node_names = ", ".join([f"node{i}" for i in range(len(perm))])

            match_paths = " ".join([f"OPTIONAL MATCH p{i} = shortestPath((node{i})-[*]-(node{i+1}))" for i in range(len(perm)-1)])
            
            query = f"""
            MATCH {match_clause}
            WITH {node_names} ORDER BY id(node0)
            {match_paths}
            RETURN {", ".join([f"p{i}" for i in range(len(perm)-1)])};
            """
            
            with driver.session(database=database) as session:
                result = session.run(query)
                if result.peek() is not None:
                    linked_graphs.append(result.graph())

        return linked_graphs
            
def find_shortest_paths_by_properties(uri, user, password, data,database):
    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        linked_graphs = []

        for perm in permutations(data):
            match_clauses = []

            for index, item in enumerate(perm):
                if "property" in item and "propertyvalue" in item:
                    table = item["table"]
                    property_name = item["property"]
                    property_value = item["propertyvalue"]
                    match_clauses.append(f"(node{index}:{table} {{{property_name}: '{property_value}'}})")

            match_clause = ", ".join(match_clauses)
            node_names = ", ".join([f"node{i}" for i in range(len(perm))])

            match_paths = " ".join([f"OPTIONAL MATCH p{i} = shortestPath((node{i})-[*]-(node{i+1}))" for i in range(len(perm)-1)])

            query = f"""
            MATCH {match_clause}
            WITH {node_names} ORDER BY id(node0)
            {match_paths}
            RETURN {", ".join([f"p{i}" for i in range(len(perm)-1)])};
            """

            with driver.session(database=database) as session:
                result = session.run(query)
                if result.peek() is not None:
                    print("in")
                    print(linked_graphs)
                    linked_graphs.append(result.graph())

        return linked_graphs


def find_given_nodes_properties(input_data,database):
    uri = input_data["URI"]
    user = input_data["username"]
    password = input_data["password"]
    data = input_data["Data"]
    database = input_data['database']
    
    nodes_found = []

    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        for item in data:
            table = item["table"]
            property_name = item["property"]
            property_value = item["propertyvalue"]
            
            query = f"""
            MATCH (node:{table} {{{property_name}: '{property_value}'}})
            RETURN node;
            """

            with driver.session(database=database) as session:
                result = session.run(query)
                for record in result:
                    node = record["node"]
                    labels = list(node.labels)
                    properties = dict(node)
                    node_data = {
                        "id": node.id,
                        "label": labels[0],
                        "properties": properties
                    }
                    nodes_found.append(node_data)

    return nodes_found

def find_given_nodes_by_id(input_data,database):
    uri = input_data["URI"]
    user = input_data["username"]
    password = input_data["password"]
    data = input_data["Data"]
    database = input_data['database']
    
    nodes_found = []

    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        for item in data:
            node_id = item["node_id"]
            
            query = f"""
            MATCH (node)
            WHERE id(node) = {node_id}
            RETURN node;
            """

            with driver.session(database=database) as session:
                result = session.run(query)
                for record in result:
                    node = record["node"]
                    labels = list(node.labels)
                    properties = dict(node)
                    node_data = {
                        "id": node_id,
                        "label": labels[0],
                        "properties": properties
                    }
                    nodes_found.append(node_data)

    return nodes_found

def Remove_given_nodes_id(result, input_data,database):
    data1 =  find_given_nodes_by_id(input_data,database)
    data1_ids = {obj['id'] for obj in data1}
    
    result['nodes'] = [node for node in result['nodes'] if node['id'] not in data1_ids]
    #result['edges'] = [edge for edge in result['edges'] if edge['source'] not in data1_ids and edge['target'] not in data1_ids]
    
    return result


def Add_given_nodes_properties(result,input_data,database):

    data1 = find_given_nodes_properties(input_data,database)
    combined_nodes = result['nodes'] + [node for node in data1 if node['id'] not in {n['id'] for n in result['nodes']}]
    
    combined_edges = result['edges']  # Keep the edges as-is
    
    combined_result = {'nodes': combined_nodes, 'edges': combined_edges}
    
    return combined_result




# Your existing functions here


def shortest_path(request):

    input_data = request.json
    
    uri = input_data["URI"]
    user = input_data["username"]
    password = input_data["password"]
    data = input_data["Data"]
    database = input_data['database']

    if any("node_id" in item for item in data):
        linked_result = find_shortest_paths_by_ids(uri, user, password, data,database)
    else:
        linked_result = find_shortest_paths_by_properties(uri, user, password, data,database)
    
    nodes = []
    edges = []
    
    for graph in linked_result:
        for node in graph.nodes:
            labels = list(node.labels)
            properties = list(node.keys())
            node_data = create_node_data(node, labels, properties)
            
            if node_data not in nodes:
                nodes.append(node_data)
        
        for rel in graph.relationships:
            edge_data = {
                "source": rel.start_node.id,
                "target": rel.end_node.id,
                "type": rel.type
            }
            
            if edge_data not in edges:
                edges.append(edge_data)
    
    result = {
        "edges": edges,
        "nodes": nodes
    }
    

    nodes = result.get("nodes", [])
    labels = [node.get("label") for node in nodes]
    icons= get_node_icon(list(set(labels)))
    result['iconLabels']=icons

    if any("node_id" in item for item in data):
        newResult = Remove_given_nodes_id(result, input_data,database)

    else:
        newResult = Add_given_nodes_properties(result, input_data,database)
    

    return newResult

