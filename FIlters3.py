
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

# Function to find common nodes and edges based on multiple conditions
def find_common_nodes_and_edges(session, conditions):
    query = f"""
        MATCH path = (n:Person)-[r]->()
        WHERE {conditions}
        RETURN DISTINCT nodes(path) as Nodes, relationships(path) as Rels
    """
    result = session.run(query)
    common_nodes = []
    common_edges = []

    for record in result:
        nodes = [node_to_dict(node) for node in record["Nodes"]]
        edges = [relationship_to_dict(rel) for rel in record["Rels"]]

        if not common_nodes:
            common_nodes.extend(nodes)
        else:
            common_nodes = [node for node in common_nodes if node in nodes]

        common_edges.extend(edges)

    return common_nodes, common_edges
##########################################################################
##########################################################################

#@app.route('/get_nodes_and_edges', methods=['POST'])
def get_nodes_and_edges():

    input_data = request.json
    if not input_data or not isinstance(input_data, (list, dict)):
        return jsonify({'error': 'Invalid input data'}), 400

    nodes = []
    edges = []

    with driver.session(database=database) as session:
        if isinstance(input_data, dict):
            # Handle "is" and "is not" conditions with dictionary input
            condition_type = input_data.get("condition")

            if condition_type in ["is", "is not"]:
                if "property" not in input_data or "propertyvalue" not in input_data:
                    return jsonify({'error': 'Invalid input data'}), 400

                property_name = input_data["property"]
                property_value = input_data["propertyvalue"]

                # IS
                if condition_type == "is":
                    is_query = f"""
                        MATCH path = (n:Person)-[r]->()
                        WHERE n.{property_name} = '{property_value}'
                        RETURN nodes(path) as Nodes, relationships(path) as Rels
                    """
                    result = session.run(is_query)
                    for record in result:
                        edges.extend([relationship_to_dict(rel) for rel in record["Rels"]])
                        nodes.extend([node_to_dict(node) for node in record["Nodes"]])

                # IS NOT
                elif condition_type == "is not":
                    is_not_query = f"""
                        MATCH path = (n:Person)-[r]->()
                        WHERE NOT n.{property_name} = '{property_value}'
                        RETURN nodes(path) as Nodes, relationships(path) as Rels
                    """
                    result = session.run(is_not_query)
                    for record in result:
                        edges.extend([relationship_to_dict(rel) for rel in record["Rels"]])
                        nodes.extend([node_to_dict(node) for node in record["Nodes"]])

            if condition_type in ["property exists", "property does not exist"]:
                if "property" not in input_data:
                    return jsonify({'error': 'Invalid input data'}), 400

                property_name = input_data["property"]

                if condition_type == "property exists":
                    exists_query = f"""
                        MATCH path = (n:Person)-[r]->()
                        WHERE n.{property_name} IS NOT NULL
                        RETURN nodes(path) as Nodes, relationships(path) as Rels
                    """
                    result = session.run(exists_query)
                    for record in result:
                        edges.extend([relationship_to_dict(rel) for rel in record["Rels"]])
                        nodes.extend([node_to_dict(node) for node in record["Nodes"]])

                elif condition_type == "property does not exist":
                    not_exists_query = f"""
                        MATCH path = (n:Person)-[r]->()
                        WHERE n.{property_name} IS NULL
                        RETURN nodes(path) as Nodes, relationships(path) as Rels
                    """
                    result = session.run(not_exists_query)
                    for record in result:
                        edges.extend([relationship_to_dict(rel) for rel in record["Rels"]])
                        nodes.extend([node_to_dict(node) for node in record["Nodes"]])

        elif isinstance(input_data, list):
            # Handle "is one of" and "is not one of" conditions with list input
            for item in input_data:
                if "property" not in item or "propertyvalue" not in item or "condition" not in item:
                    return jsonify({'error': 'Invalid input data'}), 400

                condition_type = item["condition"]
                conditions = construct_conditions([item])

                # IS ONE OF
                if condition_type == "is one of":
                    query = f"""
                        MATCH path = (n:Person)-[r]->()
                        WHERE {conditions}
                        RETURN nodes(path) as Nodes, relationships(path) as Rels
                    """
                    result = session.run(query)
                    for record in result:
                        edges.extend([relationship_to_dict(rel) for rel in record["Rels"]])
                        nodes.extend([node_to_dict(node) for node in record["Nodes"]])

                # IS NOT ONE OF
                elif condition_type == "is not one of":
                    alternative_query = f"""
                        MATCH path = (n:Person)-[r]->()
                        WHERE NOT ({conditions})
                        RETURN nodes(path) as Nodes, relationships(path) as Rels
                    """
                    result = session.run(alternative_query)
                    for record in result:
                        edges.extend([relationship_to_dict(rel) for rel in record["Rels"]])
                        nodes.extend([node_to_dict(node) for node in record["Nodes"]])

                else:
                    common_conditions = [item for item in input_data if item.get("condition") == "is common node"]
                    if common_conditions:
                        common_nodes, common_edges = find_common_nodes_and_edges(
                            session,
                            construct_conditions(common_conditions)
                        )
                        nodes.extend(common_nodes)
                        edges.extend(common_edges)
        
    return jsonify({'edges': edges, 'nodes': nodes})

if __name__ == '__main__':
    app.run(host='localhost', port=34464, debug=True)
