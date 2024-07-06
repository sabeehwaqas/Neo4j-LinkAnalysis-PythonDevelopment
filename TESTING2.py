from flask import jsonify
from neo4j import GraphDatabase
import json

def ini_graph(data):
    try:
        URI = data['URI']
        driver = GraphDatabase.driver(URI, auth=(data['username'], data['password']))
        database = data['database']
        Data=list(data['Data'])
        depth = data['depth']
        limit = data['limit']
        edges=[]
        nodes=[]
        Graph_Data={}
        for i, a in enumerate(Data):
            query=''
            table = a['table']
            properties = a['property']
            propertyvalue = str(a['propertyvalue'])
            if table=="" and properties==False and propertyvalue=="" and database!="":
                query= f" MATCH (n) WITH DISTINCT n  OPTIONAL MATCH path=(n)-[r]-(relatedNode)  with n,r,path limit {limit}  RETURN path,r"

            elif table!="" and properties!=False and propertyvalue!="" and depth!="":
                query= f"match (n:{table}"+ "{"  + f"{properties} : '{propertyvalue}'"+"}"+ " ) with distinct n "+" optional MATCH path=(n:"+ f"{table}" +f")-[r*0.."+f"{depth}"+f"]-(relatedNode) "
                query+=f"  with n,r,path limit {limit} RETURN path,r" 

            elif table!="" and properties==False and propertyvalue=="":
                query= " match (n:"+f"{table}) with distinct n  "+" OPTIONAL MATCH path=(n:"+ f"{table}" +")-"+f"[r*0.."+f"{depth}"+"]-"
                query+=f"(relatedNode)  with n,r,path limit {limit}  RETURN path,r"

            with driver.session(database=database) as session:

                print(query)
                result=list(session.run(query))

            driver.close()

            edges1,nodes1=format_to_edge_node_dict(result)
            edges.append(edges1)
            nodes.append(nodes1)

        Graph_Data={"nodes":nodes[0],"edges":edges[0]}
        return Graph_Data
        
    except Exception as e:
        return {'error': str(e)}
    
    
def format_to_edge_node_dict(result):
        
        formatted_result={"nodes":[],"edges":[]}
        try:
            for resul in result:
                # print('//////',resul,'/////////////')
                # resul=result[len(result)-1]
                # print(resul)
                for res in resul :
                    # print("WUHU RESULT IS HERE....",res)
                    # print(res)
                    try:
                        for aaa in res.nodes:
                            # print("I am What you looking for .... ",aaa,'////', type(aaa))
                            node=aaa
                            node_id= node.element_id
                            last_colon_index = node_id.rfind(":")  # Find the last occurrence of ":"

                            if last_colon_index != -1:
                                node_id1 = node_id[last_colon_index + 1:]  # Slice the string after the last ":"
                                
                            # print(node_id1)
                            formatted_node = {
                                "id":node_id1,
                                "label": list(node.labels)[0],  # Assuming a node has only one label
                                "properties": dict(node)
                            }
                            formatted_result["nodes"].append(formatted_node)
                    except:
                        for aa in res:
                            # print("I am What you looking for LISTSTS .... ",aa.nodes,'////', type(aa))

                            # print("I am What you looking for LISTSTS LASTTT.... ",aa.element_id,'////', type(aa))
                            node_id=aa.nodes[0].element_id
                            src = node_id.rfind(":")  # Find the last occurrence of ":"

                            if src != -1:
                                source = node_id[src + 1:]  # Slice the string after the last ":"
                            
                            node_id=aa.nodes[1].element_id
                            trg = node_id.rfind(":")  # Find the last occurrence of ":"
                            if trg != -1:
                                target = node_id[trg + 1:]  # Slice the string after the last ":"
                                
                            # print("Source ID.... ",source,'///', aa.type)
                            # print("Target ID ",target,'//////','/////////////////////////', aa.type)
                            formatted_edge = {
                            
                                "source": source,
                                "target": target,
                                "type": aa.type
                            }
                            # print("HELLO WORLD",formatted_edge)
                            formatted_result["edges"].append(formatted_edge)
                                    # print(formatted_result)
                            # print(formatted_result['edges'])                
                            # formatted_result["edges"],formatted_result['nodes']
                            # print('_________________________________________________________________________________')
            formatted_result["nodes"]=remove_duplicate_dicts(formatted_result["nodes"])
            formatted_result["edges"]=remove_duplicate_dicts(formatted_result['edges'])

            # print(formatted_result["edges"])
            return formatted_result["edges"],formatted_result["nodes"]

        except Exception as e:
            print("ERROR Occured",e)


def remove_duplicate_dicts(data):
    unique_data = []
    seen_data = set()

    for item in data:
        item_json = json.dumps(item, sort_keys=True)

        if item_json not in seen_data:
            seen_data.add(item_json)
            unique_data.append(item)

    return unique_data

