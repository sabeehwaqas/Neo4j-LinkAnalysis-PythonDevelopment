from flask import Flask, request, jsonify
from neo4j import GraphDatabase


uri = "bolt://localhost:7687"
username = "alinaqi"
password = "12345678"
database = "testingdb"

driver = GraphDatabase.driver(uri, auth=(username, password))

def get_first_depth_relationships(data):

    start_node_id = data['node_id']
    if not start_node_id:
        return jsonify({"error": "Start node ID is required"}), 400

    try:
        with driver.session(database=database) as session:
            result = session.run(
                "MATCH (startNode)-[r*1..1]->(relatedNode) "
                "WHERE ID(startNode) = $startNodeId "
                "RETURN r, relatedNode",
                startNodeId=start_node_id
            )
            relationships = []

            for record in result:
                relationship_data = {
                    "relationship_type": record['r'][0].type,
                    "related_node_properties": dict(record['relatedNode'])
                }
                relationships.append(relationship_data)

        return jsonify({"relationships": relationships})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

