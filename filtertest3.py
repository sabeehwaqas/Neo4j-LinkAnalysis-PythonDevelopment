from flask import Flask, request, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j configuration
uri = "bolt://localhost:7687"  # Change this to your Neo4j database URI
username = "alinaqi"            # Change this to your Neo4j username
password = "12345678"          # Change this to your Neo4j password
database='testingdb'
driver = GraphDatabase.driver(uri, auth=(username, password))

# Convert Node object to JSON-serializable dictionary
def node_to_dict(node):
    return dict(node)

# Construct Cypher query conditions for multiple properties
def construct_conditions(properties):
    conditions = []

    for prop in properties:
        conditions.append(f"n.{prop['property']} = '{prop['propertyvalue']}'")

    return " AND ".join(conditions)

# Flask route that accepts JSON input as a POST argument
@app.route('/get_person', methods=['POST'])
def get_person_by_properties():
    input_data = request.json

    if not input_data:
        return jsonify({'error': 'Invalid input data'}), 400

    conditions = construct_conditions(input_data)

    query = f"MATCH (n:Person) WHERE {conditions} RETURN n"
    # print(query)
    with driver.session(database=database) as session:
        result = session.run(query)
        nodes = [node_to_dict(record["n"]) for record in result]

    return jsonify({'nodes': nodes})


if __name__ == '__main__':
    app.run(host='localhost', port=34456, debug=True)