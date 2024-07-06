from flask import Flask, request, jsonify
from neo4j import GraphDatabase

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

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session(database=database) as session:
            results_source = list(session.run(query_source))  # Fetch into a list
            results_target = list(session.run(query_target))  # Fetch into a list

            data_source = [record.data() for record in results_source]
            data_target = [record.data() for record in results_target]

    return data_source + data_target

def get_relationship_count(driver, database, node_id):
    query = (
        f"MATCH (n) WHERE ID(n) = {node_id} "
        "OPTIONAL MATCH (n)-[r]-() "
        "RETURN count(r) AS relationshipCount"
    )

    with driver.session(database=database) as session:
        result = session.run(query)
        count = result.single()['relationshipCount']

    return count

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

    # Create the response structure with "edges" and "nodes"
    response = {"edges": [], "nodes": [], "iconLabels": []}

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        for result in results:
            edge = {
                "source": result["source"],
                "target": result["target"],
                "type": result["type"]
            }
            response["edges"].append(edge)

            if "neighbor" in result:
                rex = result["neighbor"]
                idd = result["target"]
            else:
                rex = result["startNode"]
                idd = result["source"]

            # Get the relationship count for the current node
            relationship_count = get_relationship_count(driver, database, idd)

            node = {
                "id": idd,
                "label": result["neighborLabels"][0] if result["neighborLabels"] else "",
                "properties": rex,
                "relationship_count": relationship_count  # Add relationship count here
            }
            response["nodes"].append(node)

    return jsonify(response)