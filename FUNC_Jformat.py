from neo4j import GraphDatabase
from flask import Flask, request,json, jsonify
from Node_icons import addNode_icon


# Connect to the Neo4j database
uri = "bolt://localhost:7687"
username = "alinaqi"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(username, password))
database = 'testingdb'

def import_data(data, node_name, unique_id_field):
    with driver.session(database=database) as session:
        for item in data:
            if unique_id_field in item:
                cypher_query = f"MERGE (r:{node_name} {{id: ${unique_id_field}}})"
                params = {
                    unique_id_field: item[unique_id_field]
                }
                for key, value in item.items():
                    if key != unique_id_field:
                        if isinstance(value, dict) or isinstance(value, list):
                            # Convert complex data structures to string for storage
                            value = json.dumps(value)
                            
                            # Create a node for the nested data
                            nested_node_name = f'{node_name}_{key}'
                            cypher_query += f" MERGE ({nested_node_name}:{key} {{value: ${key}}})"
                            params[key] = value
                            
                            # Create a relationship between the main node and nested node
                            cypher_query += f" MERGE (r)-[:HAS_{key.upper()}]->({nested_node_name})"
                        else:
                            cypher_query += f" SET r.{key} = ${key}"
                            params[key] = value
                session.run(cypher_query, params)

def import_jformat_data(request):
    try:
        data = request.json
        node_name = request.args.get('node_name')
        unique_id_field = request.args.get('unique_id_field')
        icon=request.args.get('icon')
        addNode_icon(node_name,icon)
        
        if not data or not node_name or not unique_id_field:
            return jsonify({"error": "Missing required parameters"}), 400
        
        import_data(data, node_name, unique_id_field)
        
        return jsonify({"message": "Data imported successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

