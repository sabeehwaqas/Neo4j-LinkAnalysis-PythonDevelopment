
from flask import Flask, request, jsonify
from neo4j import GraphDatabase


def get_relationships(request):
    
    input_data = request.json
    uri = input_data.get("URI")
    username = input_data.get("username")
    password = input_data.get("password")
    database = input_data.get("database")

    if not uri or not username or not password or not database:
        return jsonify({'error': 'Invalid credentials'}), 400

    driver = GraphDatabase.driver(uri, auth=(username, password))

    query = """
        MATCH (source)-[relationship]-(target)
        RETURN DISTINCT labels(source) AS source_labels, type(relationship) AS relationship_type, labels(target) AS target_labels
    """

    result_data = []

    with driver.session(database=database) as session:
        result = session.run(query)
        for record in result:
            result_data.append({
                "source": record["source_labels"][0],
                "relationship": record["relationship_type"],
                "target": record["target_labels"][0]
            })

    return result_data

