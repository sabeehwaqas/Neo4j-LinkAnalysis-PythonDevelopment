from flask import Flask, request, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

def get_neighboring_nodes(uri, username, password, node_id, database):
    # Query for relationships where startNode is the source
    query_source = (
        f"MATCH (startNode)-[relationship]->(neighbor) WHERE ID(startNode) = {node_id} "
        "RETURN ID(startNode) as source, type(relationship) as type, ID(neighbor) as target, neighbor, labels(neighbor) as neighborLabels"
    )

    # Query for relationships where startNode is the target
    query_target = (
        f"MATCH (startNode)-[relationship]->(neighbor) WHERE ID(neighbor) = {node_id} "
        "RETURN ID(startNode) as source, type(relationship) as type, ID(neighbor) as target, startNode, labels(startNode) as neighborLabels"
    )
    print(".....................")
    print(query_source)
    print(".....................")
    print(query_target)
    print(".....................")
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session(database=database) as session:
            results_source = list(session.run(query_source))  # Fetch into a list
            results_target = list(session.run(query_target))  # Fetch into a list

            data_source = [record.data() for record in results_source]
            data_target = [record.data() for record in results_target]
    print(".....................")
    print(data_source)
    print(".....................")
    print(data_target)
    print(".....................")
    return data_source + data_target

def expandnode(request):
    data = request  # Use request.get_json() to access the incoming JSON data

    # Extract input data from JSON
    username = data['username']
    password = data['password']
    uri = data['URI']
    database = data["database"]
    node_id = data['node_id']

    # Execute the Cypher queries
    results = get_neighboring_nodes(uri, username, password, node_id, database)
    print("RESULT_,-,-,-,-: ",results)
    # Create the response structure with "edges" and "nodes"
    response = {"edges": [], "nodes": [], "iconLabels": []}

    for result in results:
        edge = {
            "source": result["source"],
            "target": result["target"],
            "type": result["type"]
        }
        response["edges"].append(edge)

        if "neighbor" in result:
            print("first case")
            rex = result["neighbor"]
            idd = result["target"]
        else:
            print("second case")
            rex = result["startNode"]
            idd = result["source"]
        print("REX________________; ",rex)

        node = {
            "id": idd,
            "label": result["neighborLabels"][0] if result["neighborLabels"] else "",
            "properties": rex
        }
        response["nodes"].append(node)
    print(response)
    return jsonify(response)
