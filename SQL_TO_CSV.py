import os
import pyodbc
import csv

# SQL Server Connection Parameters
sql_server ='LENOVO-IDEAPAD\SQL_SERVER'
database = 'TELECOM1'
username = 'Project2'
password = '1234'

# Function to fetch data from a table and save it to a CSV file
def table_to_csv(cursor, table_name):
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    csv_file_path = f"{table_name}.csv"
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(columns)
        csv_writer.writerows(rows)
    print(f"Table '{table_name}' data has been saved to '{csv_file_path}'.")

try:
    # Connect to SQL Server
    conn = pyodbc.connect(
        f'DRIVER={{SQL Server}};SERVER={sql_server};DATABASE={database};UID={username};PWD={password}'
    )
    cursor = conn.cursor()

    # Get all table names from the database
    query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
    cursor.execute(query)
    table_names = [row.TABLE_NAME for row in cursor.fetchall()]

    # Convert each table to a CSV file
    for table_name in table_names:
        table_to_csv(cursor, table_name)

    print("All tables have been converted to CSV files successfully.")

except Exception as e:
    print("Error occurred: ", e)

finally:
    # Close the connection
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()
