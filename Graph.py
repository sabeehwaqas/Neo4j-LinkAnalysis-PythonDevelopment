import networkx as nx
import pyodbc
import graphviz

# Define your SQL Server connection details
server = 'LENOVO-IDEAPAD\SQL_SERVER'
database1 = 'NADRA'
database2 = 'TELECOM1'
database3 = 'TAXATION_DEPT'
username = 'Project2'
password = '1234'

# Function to fetch data from SQL Server database and create a NetworkX graph
def create_graph_from_sql():
    # Define the ODBC connection strings for each database
    conn_str1 = f'DRIVER={{SQL SERVER}};SERVER={server};DATABASE={database1};UID={username};PWD={password}'
    conn_str2 = f'DRIVER={{SQL SERVER}};SERVER={server};DATABASE={database2};UID={username};PWD={password}'
    conn_str3 = f'DRIVER={{SQL SERVER}};SERVER={server};DATABASE={database3};UID={username};PWD={password}'

    # Connect to the SQL Server databases
    conn1 = pyodbc.connect(conn_str1)
    conn2 = pyodbc.connect(conn_str2)
    conn3 = pyodbc.connect(conn_str3)

    # Define your SQL queries to fetch data from each database
    query1 = "SELECT CNIC, date_of_birth FROM Person"  # Replace Table1 with the actual table name in database1
    query2 = "SELECT CNIC, SIM_NUM FROM SIM_Info"  # Replace Table2 with the actual table name in database2
    query3 = "SELECT CNIC, Person_Name FROM TAX_Payer"  # Replace Table3 with the actual table name in database3

    # Fetch data from each database and create a dictionary to store node attributes
    node_attributes = {}

    with conn1, conn2, conn3:
        # Execute the queries and fetch data from the first database
        cursor1 = conn1.cursor()
        cursor1.execute(query1)
        for row in cursor1.fetchall():
            cnic, other_attribute = row[0], row[1]  # Assuming CNIC is in the first column and OtherAttribute1 is in the second column
            node_attributes.setdefault(cnic, {})
            node_attributes[cnic].update({'Attribute1': other_attribute})

        # Fetch data from the second database
        cursor2 = conn2.cursor()
        cursor2.execute(query2)
        for row in cursor2.fetchall():
            cnic, other_attribute = row[0], row[1]  # Assuming CNIC is in the first column and OtherAttribute2 is in the second column
            node_attributes.setdefault(cnic, {})
            node_attributes[cnic].update({'Attribute2': other_attribute})

        # Fetch data from the third database
        cursor3 = conn3.cursor()
        cursor3.execute(query3)
        for row in cursor3.fetchall():
            cnic, other_attribute = row[0], row[1]  # Assuming CNIC is in the first column and OtherAttribute3 is in the second column
            node_attributes.setdefault(cnic, {})
            node_attributes[cnic].update({'Attribute3': other_attribute})

    # Create a NetworkX graph and add nodes with attributes
    graph = nx.Graph()

    for cnic, attributes in node_attributes.items():
        graph.add_node(cnic, **attributes)

    # Add edges between nodes based on CNIC attribute
    for cnic in graph.nodes():
        for other_cnic in graph.nodes():
            if cnic != other_cnic and 'CNIC' in graph.nodes[cnic] and 'CNIC' in graph.nodes[other_cnic]:
                if graph.nodes[cnic]['CNIC'] == graph.nodes[other_cnic]['CNIC']:
                    graph.add_edge(cnic, other_cnic)

    return graph

# Create the graph from SQL Server databases
graph = create_graph_from_sql()

# Use Graphviz to visualize the graph
graphviz_graph = nx.nx_agraph.to_agraph(graph)
graphviz_graph.layout(prog='dot')  # You can change the layout engine here (e.g., 'neato', 'fdp', 'sfdp', etc.)
graphviz_graph.draw('output_graph.png', format='png', prog='dot')  # Save the graph as an image
