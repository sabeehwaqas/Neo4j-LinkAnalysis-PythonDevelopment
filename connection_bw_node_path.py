from flask import Flask,jsonify,request
from neo4j import GraphDatabase
from flask import json



app=Flask(__name__)

#creating route

@app.route("/getpath",methods = ["GET",'POST'])
def getpath():
    # Get the IDs of the two nodes from the request
    if request.method=="POST":
        requests=request.get_json()
        username = requests['username']
        pwd = requests['password']
        uri = requests['URI']
        database=requests['database']
        driver=GraphDatabase.driver(uri=uri,auth=(username,pwd)) 
        session=driver.session(database=database)
        field=requests['field']
        source_node_identifier = requests['source_node_identifier']
        target_node_identifier = requests['target_node_identifier']
        # Get the path between the two nodes
        start=0
        result=None
        for i in range(9):
            query = f"""
                MATCH p = (source)-[*0..{start}]->(target)
                WHERE source.{field} = "{source_node_identifier}" AND target.{field} = "{target_node_identifier}"
                RETURN p
                """
            #print(query)
            results = session.run(query)
            nodes=[record["elementId"] for record in results]
            start=+i
            a=1
            print(nodes)

                # Return the path as a list of nodes
        path = []
        try:
            for node in nodes:
                path.append(node["source"]["id"])
        except :
            b=1
        return json.dumps(path)


@app.route("/display",methods = ["GET","POST"])
def display_node():
    request=request.get_json()
    username = request['username']
    pwd = request['password']
    uri = request['URI']
    database=request['database2']
    driver=GraphDatabase.driver(uri=uri,auth=(username,pwd)) 
    session=driver.session(database=database)
    q1="""match(n) return n.NAME as NAME, n.ID as ID"""
    results=session.run(q1)
    data=results.data()
    return(jsonify(data))


app.run(port=5050)