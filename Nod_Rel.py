from neo4j import GraphDatabase
from initGraph import ini_graph
from limit import remove_extra_nodes
from Node_icons import get_node_icon
#from TESTING2 import ini_graph
from initGraph import ini_graph

def get_nodes_and_edges(data):
    URI = data['URI']
    driver = GraphDatabase.driver(URI, auth=(data['username'], data['password']))
    database = data['database']
    result={"edges":[],"nodes":[]}
    # print(data['node_id'])
    with driver.session(database=database) as session:
        try:
            for Data in data['node_id']:
                print("node_id",Data)
                query = f'MATCH (n) where ID(n)={Data} '+"OPTIONAL MATCH (n)-[r]-(relatedNode) WITH collect(DISTINCT n) + collect(DISTINCT relatedNode) AS allNodes, collect(DISTINCT r) AS allRels RETURN { nodes: [node IN allNodes | {id: id(node), label: labels(node)[0], properties: properties(node)}], edges: [rel IN allRels | {source: id(startNode(rel)), target: id(endNode(rel)), type: type(rel)}]} AS graphData;"
                result1 = session.run(query).single()["graphData"]
                print("Q:",query)
                for a in result1['edges']:
                    result['edges'].append(a)
                for a in result1['nodes']:    
                    result['nodes'].append(a)
                print("reulst",result)
                print(".............................................")
            driver.close()
            return result
        except Exception as e:
            print('error occured ', e)

def getdata(Request):
    #print(Request)
    try:
        #Request = request.json()
        if 'node_id' in Request:
            nodes_and_edges=get_nodes_and_edges(Request)
        else:
            #nodes_and_edges = ini_graph(Request)
            #print("nodes&edges: ",nodes_and_edges)
            print("REQUEST : ",Request)
            nodes_and_edges = ini_graph(Request)
            #print("nodes&edges: ",nodes_and_edges)
            # nodes_and_edges['edges']=[]
            
        # if  'limit' in Request  :
        #     nodes_and_edges=remove_extra_nodes(nodes_and_edges,Request['limit'])    
        
        nodes = nodes_and_edges.get("nodes", [])

        labels = [node.get("label") for node in nodes]
        #print(labels)
        icons= get_node_icon(list(set(labels)))
        #print(icons)
        nodes_and_edges['iconLabels']=icons

        #print("THE FINAL RETURN: ",nodes_and_edges)
        return nodes_and_edges
    except:
        return 'Invalid Request'