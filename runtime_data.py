from neo4j import GraphDatabase
from flask import jsonify
from Get_Nodes import convert_to_json

# Neo4j Configuration
# URI = "bolt://localhost:7687"
# AUTH = ("neo4j","123456789")
# database = 'neo4j'
# driver= GraphDatabase.driver(URI, auth=AUTH)  
def get_graph_data_by_query(Data):
    URI=Data['URI']
    AUTH=(Data['username'],Data['password'])
    query=Data['query']
    driver= GraphDatabase.driver(URI, auth=AUTH)  
    
    with driver.session(database=Data['database']) as session:
        result = session.run(query)
        records = result.data()
        
    driver.close()
    
    json_records = []
    for record in records:
        node = record['node']
        labels = node.labels
        properties = dict(node)
        json_data = {
            "id": node.id,
            "labels": list(labels),
            "properties": properties
        }
        json_records.append(json_data)
    
    return json_records

# def get_graph_data_by_query(Data):
#     print(Data)
#     URI=Data['URI']
#     AUTH=(Data['username'],Data['password'])
#     query=Data['query']
#     driver= GraphDatabase.driver(URI, auth=AUTH)  

    
#     try:
#         if not query:
#             return jsonify({"error": "Missing 'query' parameter"}), 400
#         print(query)
#         with driver.session(database=Data['database']) as session:
#             result = session.run(query)
#             query_result = []
#             result=result.single()
#             for record in result:
        
#                 print(type(record))
#                 print("........................sfcwevwevweve")
#                 query_result.append(convert_to_json(record))
#             #print(query_result)
#             return query_result

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         driver.close()