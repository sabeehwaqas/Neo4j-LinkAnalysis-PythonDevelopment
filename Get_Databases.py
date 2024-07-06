from neo4j import GraphDatabase

# Neo4j connection settings
uri = "bolt://localhost:7687"  # Replace with your Neo4j server URI
username = "alinaqi"
password = "12345678"

# Function to retrieve databases, node labels, and properties
def get_database_info(driver,session):
    databases_query = "SHOW DATABASES"
    databases_result = session.run(databases_query)
    RETURNED_DATA=[]

    for record in databases_result:
        database_name = record["name"]
        # print(f"Database: {database_name}")

        with driver.session(database=database_name) as session2:

            labels_query = "CALL db.labels()"
            labels_result = session2.run(labels_query)
            labels=[]
            
            for label_record in labels_result:

                label = label_record["label"]
                properties_query = f"""MATCH (p:{label}) WITH DISTINCT keys(p) AS keys
                UNWIND keys AS keyslisting WITH DISTINCT keyslisting AS allfields
                RETURN allfields;"""
                properties_result = session2.run(properties_query)
                properties=[]
                for prop in properties_result:
                    properties.append(prop["allfields"])

                properties=list(set(properties))
                labels.append({"label":label,"properties":properties})

        RETURNED_DATA.append({"Database":database_name,"Labels":labels})
    return RETURNED_DATA
# Connect to the Neo4j database
def GET_DATABASE():
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session(database="system") as session:
            data=get_database_info(driver,session)
    return data