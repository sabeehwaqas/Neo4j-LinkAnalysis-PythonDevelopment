from flask import Flask, request, jsonify
from neo4j import GraphDatabase
import re

#app = Flask(__name__)

def create_driver(uri, username, password):
    return GraphDatabase.driver(uri, auth=(username, password))

def serialize_record(record):
    # Convert frozenset to list
    if 'labels' in record:
        record['labels'] = list(record['labels'])
    return record

def label_query(session, query):
    labels = ["Person", "SimInfo", "Taxpayer", "Taxtype", "TransactionsI", "Logs", "UserI"]
    results = {}

    for label in labels:
        result = session.run(
            f'CALL db.index.fulltext.queryNodes("{label}", "{query}") YIELD node, score '
            'RETURN node, labels(node) AS labels'
        )

        # Process query results for the label into a list of dictionaries
        results[label] = [{"node": dict(record["node"]), "labels": record["labels"]} for record in result]

    return results

def property_value_query(session, query):
    labels = ["Person", "SimInfo", "Taxpayer", "Taxtype", "TransactionsI", "Logs", "UserI"]
    results = {}

    for label in labels:
        regex_pattern = f"(?i)^{query}.*"  # Match the query at the start of property values (case-insensitive)
        result = session.run(
            f'MATCH (node:{label}) WHERE ANY(key IN keys(node) WHERE node[key] =~ $regex) '
            'RETURN node, labels(node) AS labels',
            regex=regex_pattern
        )

        # Process query results for the label into a list of dictionaries
        processed_results = []
        for record in result:
            node = dict(record["node"])
            labels = record["labels"]

            processed_results.append({"node": node, "labels": labels})

        results[label] = processed_results

    return results

#@app.route("/search", methods=["POST"])
def search():
    try:
        request_data = request.get_json()
        query = request_data.get("query")
        database = request_data.get("database")
        username = request_data.get("username")
        password = request_data.get("password")
        uri = request_data.get("URI")

        # Validate user input (e.g., check for empty query)
        if not query:
            return jsonify({"error": "Invalid query"}), 400

        driver = create_driver(uri, username, password)

        # Execute the Cypher query in the same session
        with driver.session(database=database) as session:
            results = label_query(session, query)

            # If no label-based results, proceed with regex query for labels
            if not any(results.values()):
                results = property_value_query(session, query)

            # Property keys with regex pattern matching
            regex_pattern = f"(?i).*{query}.*"
            result_props = session.run(
                'MATCH (n) WHERE ANY(key IN keys(n) WHERE key =~ $regex) RETURN n',
                regex=regex_pattern
            )

            # Process query results for Properties into a list of dictionaries
            results["Props"] = [{"node": dict(record["n"]), "labels": record["n"].labels} for record in result_props]

        # Filter out empty lists and serialize the records
        filtered_results = {
            key: [serialize_record(record) for record in value if record.get('node')]
            for key, value in results.items()
        }

        # Remove empty categories from filtered_results
        filtered_results = {key: value for key, value in filtered_results.items() if value}

        return jsonify({"results": filtered_results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#if __name__ == '__main__':
#   app.run(host="localhost", debug=True, port=34465)
