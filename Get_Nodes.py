from neo4j import GraphDatabase
import json

# neo4j_uri = 'bolt://localhost:7687'
# neo4j_username = 'alinaqi'
# neo4j_password = '12345678'
# database='testingdb'

def get_child_nodes(session, node_id):
    query = (
        "MATCH (a)-[relations*0..1]->(child) "
        f"WHERE ID(a) = {node_id} RETURN child"
    )
    result = session.run(query)
    child_nodes = [record["child"] for record in result]
    
    return child_nodes

def get_node_and_child_nodes(session,data):
    for Data in data:
        field=Data['field']
        field_value=Data['field_value']

        if field=='node_id':
            query=f"MATCH (a) where id(a)={field_value}  "+"RETURN a"
            result = session.run(query)
            s= result.single()
            Parent=s['a']
            node_id=field_value

        try:
            child_nodes =get_child_nodes(session, node_id)
        except :
            print("No child elements! ")
    Parent.append(Parent)
    child_nodes.append(child_nodes)
    return Parent, child_nodes

def close(session,neo4j_driver):
    session.close()
    neo4j_driver.close()

def convert_to_json(node):
    # print("\here i amaeddwedwedwedwedwed")
    labels = node.labels
    properties = dict(node)
    json_data = {
        "id":node.id,
        "labels": list(labels),
        "relation":'rel',
        "properties": properties
    }

    json_string = json.dumps(json_data, indent=None)

    #print(json_string,"JSON_STRING........")
    return json_string


def Get_Nodes_Data(Data):
    AUTH=(Data['username'],Data['password'])
    database=Data['database']
    URI=Data['URI']
    neo4j_driver = GraphDatabase.driver(URI, auth=AUTH)
    session = neo4j_driver.session(database=database)
    Parent_node,Child_node=get_node_and_child_nodes(session,Data)
    children=[]

    for child in Child_node:
        if child.id!=Parent_node.id:
            res=convert_to_json(child)
            children.append(res)

    json_dicts = [json.loads(json_str) for json_str in children]
    #print(json_dicts)
    Parent_node=json.loads(convert_to_json(Parent_node))
    #print(Parent_node)
    close(session,neo4j_driver)
    return {"Parent_Node":Parent_node,"Child_Node":json_dicts}
