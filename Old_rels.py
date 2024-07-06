from flask import Flask, request, jsonify
from neo4j import GraphDatabase

def get_node_name(uri,username,password,database,node_name):

    try:
        # Function to execute the query and retrieve relationships
        #this node pointing other nodes
        query = f"""
                   MATCH (n:{node_name})-[r]->(relatedNode)
                    RETURN DISTINCT labels(n) as sourceNode, type(r) AS relationship_type, labels(relatedNode)
                    ,r.basis_1 as sourceProp,r.basis_2 as relatedProp

                """
        #print(query)
        with GraphDatabase.driver(uri, auth=(username, password)) as driver:
            
            with driver.session(database=database) as session:
                
                result = session.run(query, nodeName=node_name)
                result1 = result.data()
                #print("REUSLT!: ",result1)
        driver.close()


        #other points this node
        query = f"""
                   MATCH (n)-[r]->(relatedNode:{node_name})
                    RETURN DISTINCT labels(n) as sourceNode, type(r) AS relationship_type, labels(relatedNode)
                    ,r.basis_1 as sourceProp,r.basis_2 as relatedProp

                """
        #print(query)
        with GraphDatabase.driver(uri, auth=(username, password)) as driver:
            
            with driver.session(database=database) as session:
                
                result = session.run(query, nodeName=node_name)
                result2 = result.data()
                #print("REUSLT2: ",result2)
        driver.close()

        sourceNode = []
        relationship_types = []
        related_labels = []
        sourceProp=[]
        relatedProp=[]

       #inserting the data for it pointing others
        for entry in result1:
            #print("enrty:",entry)
            sourceNode.append(entry['sourceNode'][0])
            relationship_types.append(entry['relationship_type'])
            related_labels.extend(entry['labels(relatedNode)'])
            sourceProp.append(entry['sourceProp'])
            relatedProp.append(entry['relatedProp'])

        #inserting the data for others pointing it
        for entry in result2:
            #print("enrty:",entry)
            sourceNode.append(entry['sourceNode'][0])
            relationship_types.append(entry['relationship_type'])
            related_labels.extend(entry['labels(relatedNode)'])
            sourceProp.append(entry['sourceProp'])
            relatedProp.append(entry['relatedProp'])


        #print("Source Node: ",sourceNode)     
        #print("Relationship Types:", relationship_types)
        #print("Related Labels:", related_labels)
        #print("Source Prop:", sourceProp)
        #print("Related Prop:", relatedProp)


        # Execute the MERGE query for each relationship type and related label
        with driver.session(database=database) as session:
            
            for i in range(len(sourceNode)):
                #print("Eerer",sourceNode[i],related_labels[i],relationship_types[i],sourceProp[i],relatedProp[i])



                query=f"MATCH (source:{sourceNode[i]}) "+f"WHERE source.{sourceProp[i]} IS NOT NULL "+f"MATCH (target:{related_labels[i]}) "+f"WHERE target.{relatedProp[i]} = source.{sourceProp[i]} "+f"MERGE (source)-[:{relationship_types[i]}" + '{basis_1:'+f"'{sourceProp[i]}', "+"basis_2:"+ f"'{relatedProp[i]}'"+"}"+ "]->(target) RETURN source "
                
                session.run(query)

        # Close the Neo4j driver
        driver.close()
        success_response ="Successfully added the old relation to new if exist"
        return success_response


    except Exception as e:
        e = str(e)
        error_response =  f'An error occurred'+'details = {e}'
        
        return error_response
