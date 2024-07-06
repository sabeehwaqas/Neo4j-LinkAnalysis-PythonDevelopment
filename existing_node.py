from flask import Flask, request, jsonify
from neo4j import GraphDatabase


def get_node_labels(request):
    data = request.json

    if "database" in data and "username" in data and "password" in data and "URI" in data:
        try:

            driver_uri = data["URI"]
            driver_user = data["username"]
            driver_password = data["password"]
            database = data["database"]
            global driver
            driver = GraphDatabase.driver(driver_uri, auth=(driver_user, driver_password))

            query = """
            MATCH (n)
            RETURN DISTINCT labels(n) AS node_labels;
            """

            with driver.session(database=database) as session:
                result = session.run(query)

                node_labels = [{"node_labels": record["node_labels"][0]} for record in result]
            
            return jsonify(node_labels)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    else:
        return jsonify({"error": "Invalid JSON body"}), 400

def delete_node(request):
    
    data = request.json

    driver_uri = data["URI"]
    driver_user = data["username"]
    driver_password = data["password"]
    database = data["database"]
    driver = GraphDatabase.driver(driver_uri, auth=(driver_user, driver_password))

    to_del = data['delete']

    if to_del is list:

        try:
            for i in range(len(to_del)):

                current_del = int(to_del[i])


                with driver.session(database=database) as session:
                    # Construct and execute a Cypher query to delete the node by ID
                    query = f"MATCH (n) WHERE id(n) = {current_del} DELETE n"

                    session.run(query)

            driver.close()

            return "Successfully deleted the node/s",200
        except Exception as e:
            driver.close()
            return jsonify({"error": str(e)}), 500
    else:

        try:

            current_del = str(to_del)

            with driver.session(database=database) as session:
                # Construct and execute a Cypher query to delete the node by ID
                query = f"MATCH (n:{current_del}) DETACH DELETE n"

                session.run(query)

            driver.close()

            return "Successfully deleted the Whole node",200
        except Exception as e:
            driver.close()
            return jsonify({"error": str(e)}), 500





def get_existing_nodes_or_delete(request):
    data = request.json

    if data["delete"]!='' or data['delete'] in data:

        return jsonify(delete_node(request))
    else:

        return get_node_labels(request)

