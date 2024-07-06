from flask import Flask, request, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# ... (Neo4j configuration and other code)
# Neo4j configuration
uri = "bolt://localhost:7687"  # Change this to your Neo4j database URI
username = "alinaqi"     # Change this to your Neo4j username
password = "12345678"     # Change this to your Neo4j password
database = "testingdb"


# Cypher query to retrieve nodes by properties
def retrieve_nodes_by_properties(properties):
    query = "MATCH (n) WHERE "
    conditions = []

    for prop_name, prop_value in properties.items():
        conditions.append(f"n.{prop_name} = '{prop_value}'")

    query += " AND ".join(conditions)
    query += " RETURN n"

    with driver.session(database=database) as session:
        result = session.run(query)
        nodes = [record["n"] for record in result]
        return nodes


driver = GraphDatabase.driver(uri, auth=(username, password))

# Flask route that accepts JSON input
@app.route('/nodes', methods=['POST'])
def get_nodes_by_properties():
    properties = request.json

    if not properties:
        return jsonify({'error': 'JSON data is required in the request body'}), 400

    nodes = retrieve_nodes_by_properties(properties)
    return jsonify({'nodes': nodes})

if __name__ == '__main__':
    app.run(host='192.168.137.3',debug=True, port=34465)