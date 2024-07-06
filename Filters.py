from flask import Flask, request, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j configuration
uri = "bolt://localhost:7687"  # Change this to your Neo4j database URI
username = "fatima"            # Change this to your Neo4j username
password = "12345678"          # Change this to your Neo4j password
database = 'testing'
driver = GraphDatabase.driver(uri, auth=(username, password))

# Convert Node object to JSON-serializable dictionary
def node_to_dict(node):
    node_dict = {
        'id': node.id,
        'label': list(node.labels)[0],
        'properties': dict(node)
    }
    return node_dict

# Convert Relationship object to JSON-serializable dictionary
def relationship_to_dict(rel):
    return {
        'source': rel.start_node.id,
        'target': rel.end_node.id,
        'type': rel.type
    }

# Construct Cypher query conditions for multiple properties
def construct_conditions(properties):
    conditions = []

    for prop in properties:
        conditions.append(f"n.{prop['property']} = '{prop['propertyvalue']}'")

    return " AND ".join(conditions)

#@app.route('/get_nodes_and_edges', methods=['POST'])
def get_nodes_and_edges():
    input_data = request.json

    if not input_data or not isinstance(input_data, list):
        return jsonify({'error': 'Invalid input data'}), 400

    nodes = []
    edges = []

    with driver.session(database=database) as session:
        for item in input_data:
            if "property" not in item or "propertyvalue" not in item:
                return jsonify({'error': 'Invalid input data'}), 400

            existence = item.get("existence", False)
            conditions = construct_conditions([item])
            
            if existence:
                query = f"""
                    MATCH path = (n:Person)-[r]->()
                    WHERE {conditions}
                    RETURN nodes(path) as Nodes, relationships(path) as Rels
                """
                result = session.run(query)
                for record in result:
                    edges.extend([relationship_to_dict(rel) for rel in record["Rels"]])
                    nodes.extend([node_to_dict(node) for node in record["Nodes"]])
            elif not existence:
                alternative_query = f"""
                    MATCH path = (n:Person)-[r]->()
                    WHERE NOT ({conditions})
                    RETURN nodes(path) as Nodes, relationships(path) as Rels
                """
                result = session.run(alternative_query)
                for record in result:
                    edges.extend([relationship_to_dict(rel) for rel in record["Rels"]])
                    nodes.extend([node_to_dict(node) for node in record["Nodes"]])

    return jsonify({'edges': edges, 'nodes': nodes})

if __name__ == '__main__':

    app.run(host='localhost', port=34464, debug=True)