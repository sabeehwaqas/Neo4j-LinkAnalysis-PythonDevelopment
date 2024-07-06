import pyodbc
from neo4j import GraphDatabase


##################################################################################################### 
# sql_server ='LENOVO-IDEAPAD\SQL_SERVER'                                                             #
# username = 'Project2'
# password = 1234
#database=input("Enter Database Name!! ")

# neo4j_uri = 'bolt://localhost:7687'  # Replace with the appropriate URI
# neo4j_username = 'alinaqi'
# neo4j_password = '12345678'
#database_neo='testingdb'
######################################################################################################

def add_data_source(source_url,source_database,source_user,source_password,neo4j_url,neo4j_database,neo4j_user,neo4j_password,keep_relations):

    try:
        neo4j_driver = GraphDatabase.driver(neo4j_url, auth=(neo4j_user, neo4j_password))
        session = neo4j_driver.session(database=neo4j_database)
        print("NEO4j connection successfull")
    # Connect to SQL Server
    except Exception as e:
        print("Error in connecting to Neo4j server: ",e)
    try:
        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={source_url};DATABASE={source_database};UID={source_user};PWD={source_password}'
            )
        cursor = conn.cursor()
        print("SQL connection Successfull")
    except Exception as e:
        print("Error in connecting to SQL Server : ",e)
    resp=Call_MAIN_FUNCTION(session,cursor,source_database,keep_relations,neo4j_driver,conn)

def get_tables(cursor):
    tables = []
    query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        tables.append(row.TABLE_NAME)
    return tables

def get_relations(cursor,table):
    relations = {}
    query = f"EXEC sp_fkeys @pktable_name = '{table}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        fk_table = row.FKTABLE_NAME
        fk_column = row.FKCOLUMN_NAME
        pk_table = row.PKTABLE_NAME
        pk_column = row.PKCOLUMN_NAME
        if fk_table not in relations:
            relations[fk_table] = [(fk_column, pk_table, pk_column)]
        else:
            relations[fk_table].append((fk_column, pk_table, pk_column))
    return relations

def get_table_data(cursor,table):
    data = []
    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    #print(columns)
    for row in rows:
        data.append(dict(zip(columns, row)))
    return data

def Migrate_SQL_TO_NEO4j(session,cursor,source_database,keep_relations):
    try:
        # Get all tables from the database
        tables = get_tables(cursor)
        # Find relationships between tables
        table_relations = {}
        for table in tables:
            relations = get_relations(cursor,table)
            table_relations[table] = relations
        
        # Create nodes for tables and insert data
        for table, relations in table_relations.items():
            print(f"Processing Table: {table}")
            node_label = table
            data = get_table_data(cursor,table)
            # print(data)
            for row in data:                    
                properties = ", ".join([f"{key}: '{value}'" for key, value in row.items()])
                properties += f", Database:'{source_database}'"
                query = f"CREATE (:{node_label} {{{properties}}})"
                session.run(query)
        # Create relationships between tables
        def keep_relations(value1):
            if keep_relations==1:
                for table, relations in table_relations.items():
                    for related_table, fk_info in relations.items():
                        for fk_column, pk_table, pk_column in fk_info:
                            relationship_type = f"{table}_TO_{related_table}"
                            query = (
                                f"MATCH (a:{table}), (b:{related_table}) "
                                f"WHERE a.{fk_column} = b.{pk_column} "
                                f"CREATE (a)-[]->(b)"
                            )
                            session.run(query)
        keep_relations(keep_relations)

    except Exception as e:
        print(f"Error occurred: {e}")
    return 'Success !!'
#print(Migrate_SQL_TO_NEO4j(0))

def Call_MAIN_FUNCTION(session,cursor,source_database,keep_relations,neo4j_driver,conn):
    Migrate_SQL_TO_NEO4j(session,cursor,source_database,keep_relations)
    try:
        # Close the connections
        session.close()
        neo4j_driver.close()
        cursor.close()
        conn.close()
        return "Data migration to Neo4j completed successfully! " 
    except:
        print('error somewhere')