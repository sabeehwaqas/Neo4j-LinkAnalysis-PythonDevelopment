from flask import Flask, request, jsonify
from neo4j import GraphDatabase

import re  # Import the regular expression library

def is_valid_database_name(database_name):
    # Define a regular expression pattern to match valid database names
    # Valid names should contain only alphanumeric characters and underscores
    pattern = r"^[a-zA-Z0-9_]+$"
    return re.match(pattern, database_name) is not None

def manage_database(request):
    data = request.json
    driver = GraphDatabase.driver(data.get('URI'), auth=(data.get("username"), data.get("password")))
    action = data.get('action')
    database_name = data.get('database')
    
    # Check if the database name is valid
    if not is_valid_database_name(database_name):
        return jsonify({"message": "Invalid database name. Database names can only contain letters, numbers, and underscores."}), 400
    
    if action == 'create':
        if create_neo4j_database(database_name, driver):
            return jsonify({"message": f"Database '{database_name}' created successfully!"})
        else:
            return jsonify({"message": f"Failed to create database '{database_name}'."}), 500
    elif action == 'delete':
        if delete_neo4j_database(database_name, driver):
            return jsonify({"message": f"Database '{database_name}' deleted successfully!"})
        else:
            return jsonify({"message": f"Failed to delete database '{database_name}'."}), 500
    else:
        return jsonify({"message": "Invalid action. Use 'create' or 'delete'."}), 400

def create_neo4j_database(database_name,driver):
    try:
        with driver.session(database="system") as session:

            query = f"CREATE DATABASE {database_name}"

            session.run(query)
            return True
    except Exception as e:
        print("Error creating database:", str(e))
        return False

def delete_neo4j_database(database_name,driver):
    try:
        with driver.session(database="system") as session:
            query = f"DROP DATABASE {database_name}"
            session.run(query)
            return True
    except Exception as e:
        print("Error deleting database:", str(e))
        return False

