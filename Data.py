import pyodbc
import requests 

def get_sql_server_data():
    server = 'LENOVO-IDEAPAD\SQL_SERVER'
    database = 'TAXATION_DEPT'
    username = 'Project2'
    password = 1234

    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    query = "SELECT * FROM transactions"
    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor]

    cursor.close()
    connection.close()
    return data


#def index_data_to_elasticsearch(data):
    es_url = 'http://192.168.1.106:9200'
    index_name = 'tax_transactions'

    for record in data:
        cnic = record['Transaction_id']  # Assuming 'CNIC' is the unique identifier
        url = f'{es_url}/{index_name}/_doc/{cnic}'
        headers = {'Content-Type': 'application/json'}
        response = requests.put(url, json=record, headers=headers)

        if response.status_code not in [200, 201]:
            print(f"Failed to index record with CNIC: {cnic}",response)

if __name__ == "__main__":
    sql_data = get_sql_server_data()
    print(sql_data)
    #index_data_to_elasticsearch(sql_data)