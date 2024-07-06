from flask import Flask, request, jsonify
from neo4j import GraphDatabase
import json


# Define your Neo4j connection parameters
app = Flask(__name__)


from neo4j import GraphDatabase

def import_json_to_neo4j(json_data, label, username, password, database, uri):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    try:
        with driver.session(database=database) as session:
            for data in json_data:
                properties = ", ".join([f"{key}: '{value}'" for key, value in data.items()])
                query = (
                    f"MERGE (n:{label} {{{properties}}})"
                )

                print("q", query)

                # Execute the query with parameters
                session.run(query)

        return 200
    except Exception as e:
        print("Error:", e)
        return 500
    finally:
        driver.close()






def data_formating(file_data):
    cleaned_data = []
    special_chars = ['!',"@","#","$","%","^",' ',"&","*","(",")","_","-","=","+","[","{","]","}",";",":","'",'"',",","<",".",">","/","?","\\","|"] 

    for data in file_data:
        cleaned_dict = {}
        for key, value in data.items():
            cleaned_key = key
            for char in special_chars:
                cleaned_key = cleaned_key.replace(char, '_')
            cleaned_dict[cleaned_key] = value
        cleaned_data.append(cleaned_dict)
    print(cleaned_data)
    return cleaned_data


def label_format(string):
    special_chars = ['!',"@","#","$","%","^",' ',"&","*","(",")","_","-","=","+","[","{","]","}",";",":","'",'"',",","<",".",">","/","?","\\","|"] 
    for char in special_chars:
        string = string.replace(char, '_')
    print("LABEL;",string)
    return string


@app.route('/upload_csv_neo', methods=['POST'])
def upload_csv():


    try:
        request_data = request.json
        

        if "database" in request_data:
            uri = request["URI"]
            username = request["username"]
            password = request["password"]
            database = request["database"]
        else:
            uri = "bolt://localhost:7687"
            username = "alinaqi"
            password = "12345678"
            database = "testingdb"


        label = request_data.get("label_name", "Node")  # Default label is 'Node'
        file_data = request_data.get("file_data", [])

        if not file_data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        label = label_format(label)
        print("LABEL",label)
        file_data_formated = data_formating(file_data)
        success = import_json_to_neo4j(file_data_formated, label,username,password,database,uri)
        if success == 200:
            return jsonify({"message": "JSON data inserted successfully in Neo4j"}), 200
        else:
            return jsonify({"error": "Error in Inserting data to Database"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host="192.168.18.84",debug=True, port=34465)

