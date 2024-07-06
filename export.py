from neo4j import GraphDatabase
import json

def export_data(Data):
    URI = Data['URI']
    AUTH = Data['AUTH']
    database_name = Data['database']
    types = Data['types']
    how = Data['how']
    path = Data['path']
    config = Data['config']
    query = Data['query']
    AUTH = (AUTH['username'], AUTH['password'])
    driver = GraphDatabase.driver(URI, auth=AUTH)

    if not types.lower() in ['json', 'graphml', 'csv']:
        return ({"error": "incorrect 'types' parameter entered"})
    if not how.lower() in ['all', 'data', 'graph', 'query']:
        return ({"error": "incorrect 'how' parameter entered"})

    try:
        if how.lower() == 'query' and query:
            if config is None:
                export_query = f"CALL apoc.export.{types}.{how}('{query}', 'file:///{path}')"
            else:
                config_json = json.dumps(config)
                export_query = f"CALL apoc.export.{types}.{how}('{query}', 'file:///{path}', {config_json})"
        else:
            if config is None:
                export_query = f"CALL apoc.export.{types}.{how}('file:///{path}')"
            else:
                config_json = json.dumps(config)
                export_query = f"CALL apoc.export.{types}.{how}('file:///{path}', {config_json})"
        # print(export_query)
        with driver.session(database=database_name) as session:
            session.run(export_query)
        
        return ({"message": f"Exported data to {types} successfully to {path}"}), 200
    except Exception as e:
        return ({"error": str(e)}), 404
    finally:
        driver.close()
