import pyodbc
from py2neo import Graph, Node, Relationship

# SQL Server Connection Parameters
sql_server = 'your_sql_server'
database = 'your_sql_database'
username = 'your_sql_username'
password = 'your_sql_password'

# Neo4j Connection Parameters
neo4j_uri = 'bolt://localhost:7687'  # Replace with the appropriate URI
neo4j_username = 'neo4j'
neo4j_password = 'your_neo4j_password'

# Connect to SQL Server
conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={sql_server};DATABASE={database};UID={username};PWD={password}'
)
cursor = conn.cursor()

def get_tables():
    tables = []
    query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        tables.append(row.TABLE_NAME)
    return tables

def get_relations(table):
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

def get_table_data(table):
    data = []
    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    for row in rows:
        data.append(dict(zip(columns, row)))
    return data

if __name__ == "__main__":
    try:
        # Connect to Neo4j
        graph = Graph(neo4j_uri, auth=(neo4j_username, neo4j_password))

        # Get all tables from the database
        tables = get_tables()

        # Find relationships between tables
        table_relations = {}
        for table in tables:
            relations = get_relations(table)
            table_relations[table] = relations

        # Create nodes for tables and insert data
        for table, relations in table_relations.items():
            print(f"Processing Table: {table}")
            node_label = table
            data = get_table_data(table)
            for row in data:
                node = Node(node_label, **row)
                graph.create(node)

        # Create relationships between tables
        for table, relations in table_relations.items():
            for related_table, fk_info in relations.items():
                for fk_column, pk_table, pk_column in fk_info:
                    relationship_type = f"{table}_TO_{related_table}"
                    query = (
                        f"MATCH (a:{table}), (b:{related_table}) "
                        f"WHERE a.{fk_column} = b.{pk_column} "
                        f"CREATE (a)-[r:{relationship_type}]->(b)"
                    )
                    graph.run(query)

        print("Data migration to Neo4j completed successfully.")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Close the connections
        cursor.close()
        conn.close()
