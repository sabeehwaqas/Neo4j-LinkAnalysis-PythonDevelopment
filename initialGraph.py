from flask import jsonify,Flask
from neo4j import GraphDatabase
import json

def ini_graph(data):
    try:
        URI = data['URI']
        driver = GraphDatabase.driver(URI, auth=(data['username'], data['password']))
        database = data['database']
        Data=list(data['Data'])
        depth = data['depth']
        limit = data['limit']
        query=''
        nodes=''
        allRelationships=''
        node=''

        for i, a in enumerate(Data):
            table = a['table']
            properties = a['property']
            propertyvalue = str(a['propertyvalue'])
            if table=="" and properties==False and propertyvalue=="" and database!="":
                query+= f" OPTIONAL MATCH (n)-[r*0..{depth}]-(c) RETURN c "+f"limit {limit} "
                # print("NO 1 is executing")
        
            elif table!="" and properties!=False and propertyvalue!="" and depth!="":
                query+= " OPTIONAL MATCH path=(n:"+ f"{table}" + '{'+ f"{properties} :"+ f'"{propertyvalue}"'+"})-"+f"[r*0.."+f"{depth}"+"]-"
                query+=f"(relatedNode) WITH {node} COLLECT(DISTINCT relatedNode) AS nodes{i}, COLLECT(r) AS allRelationships{i} " 
                # print("NO 2 is executing")
            elif table!="" and properties==False and propertyvalue=="":
                query+= " OPTIONAL MATCH path=(n:"+ f"{table}" +")-"+f"[r*0.."+f"{depth}"+"]-"
                query+=f"(relatedNode) WITH {node} COLLECT(DISTINCT relatedNode) AS nodes{i}, COLLECT(r) AS allRelationships{i}  "
                # print("NO 3 is executing")
            else:
                return {'error': "No Query Executed"} 
            if i!=0:
                nodes+=f"+nodes{i}"
                allRelationships+=f"+allRelationships{i} "
            elif i==0:
                nodes+=f"nodes{i}"
                allRelationships+=f"allRelationships{i} "
            node+=f" nodes{i},allRelationships{i}, "

        mid_query=f'''WITH {nodes} AS nodes, {allRelationships} AS allRelationships '''
        fixed_query='''WITH REDUCE(edges = [], rels IN allRelationships |    edges + [rel in rels |       { source: ID(startNode(rel)), target: ID(endNode(rel)), type: type(rel) }     ]) AS edges, nodes RETURN { edges: edges, nodes: nodes } AS graphData;'''    
        
        finalquery=str(query+mid_query+fixed_query)
        print(finalquery)
        with driver.session(database=database) as session:
            result = session.run(finalquery).single()
        driver.close()
        return format_to_edge_node_dict(result)
        
    except Exception as e:
        return {'error': str(e)}
    
    
def format_to_edge_node_dict(result):
        if result is None:
            return jsonify({'error': 'No data found'})

        result_data = result.get("graphData", None)
       
        if result_data is None:
            return jsonify({'error': 'No graph data found in the result'})
        formatted_nodes = []
        for node in result_data.get("nodes", []):
            id= node.element_id
            id= int(id[id.rfind(":") + 1:])
            result_properties = dict(zip(list(node.keys()), list(node.values())))
            formatted_nodes.append({
                "id": id,
                "label": str(list(node.labels)[0]),  # Assuming each node has only one label
                "properties": result_properties
            })

        formatted_edges = []
        for edge in result_data.get("edges", []):
            formatted_edges.append({
                "source": edge["source"],
                "target": edge["target"],
                "type": edge["type"]
            })        

        formatted_result = {
            "nodes": remove_duplicate_dicts(formatted_nodes),
            "edges": remove_duplicate_dicts(formatted_edges)
        }
        return formatted_result

def remove_duplicate_dicts(data):
    unique_data = []
    seen_data = set()

    for item in data:
        item_json = json.dumps(item, sort_keys=True)

        if item_json not in seen_data:
            seen_data.add(item_json)
            unique_data.append(item)

    return unique_data