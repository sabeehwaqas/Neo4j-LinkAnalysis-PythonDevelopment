from neo4j import GraphDatabase
import re


# Define a function to execute the Cypher query and format the result
def execute_query_and_format_result(uri, username, password,database='testingdb'):
    formatted_result = {
        "edges": [],
        "nodes": []
    }

    # Connect to the Neo4j database
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session(database=database) as session:
            # Your Cypher query
            cypher_query = """
            MATCH (n:CDR)
            WHERE (n)-[]->()
            WITH DISTINCT n
            LIMIT 5
            MATCH (n)-[r*0..1]-(relatedNode)
            RETURN COLLECT(DISTINCT relatedNode) AS nodes, COLLECT(DISTINCT r) AS relationships
            """

            result = session.run(cypher_query).single()
            #print(result)
            # Format nodes
            for node in result["nodes"]:
 

                node_id= node.element_id

                last_colon_index = node_id.rfind(":")  # Find the last occurrence of ":"

                if last_colon_index != -1:
                    node_id1 = node_id[last_colon_index + 1:]  # Slice the string after the last ":"
                   

                formatted_node = {
                    "id":node_id1,
                    "label": list(node.labels)[0],  # Assuming a node has only one label
                    "properties": dict(node)
                }

                formatted_result["nodes"].append(formatted_node)

            # Format relationships

            for rel in result["relationships"][1]:
               
                
                rel_node1 = rel.nodes[0].element_id
                rel_node2 = rel.nodes[1].element_id


                last_colon_index = rel_node1.rfind(":")  # Find the last occurrence of ":"

                if last_colon_index != -1:
                    source_id = rel_node1[last_colon_index + 1:]  # Slice the string after the last ":"

                last_colon_index = rel_node2.rfind(":")  # Find the last occurrence of ":"

                if last_colon_index != -1:
                    target_id = rel_node2[last_colon_index + 1:]  # Slice the string after the last ":"


                formatted_edge = {
                    "source": source_id,
                    "target": target_id,
                    "type": rel.type
                }
                formatted_result["edges"].append(formatted_edge)
    # print(formatted_result)
    return formatted_result

# Define your Neo4j connection details
neo4j_uri = "bolt://localhost:7687"
neo4j_username = "alinaqi"
neo4j_password = "12345678"
database='testingdb'
# Execute the query and format the result
formatted_result = execute_query_and_format_result(neo4j_uri, neo4j_username, neo4j_password,database)

# Print or use the formatted result as needed
# print(formatted_result)
