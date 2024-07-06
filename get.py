import requests

def get_all_data_from_elasticsearch():
    es_url = 'http://localhost:9200'
    index_name = 'sim_info'

    url = f'{es_url}/{index_name}/_search'
    headers = {'Content-Type': 'application/json'}
    query = {"query": {"match_all": {}}
              ,"size": 160
             }

    response = requests.get(url, json=query, headers=headers)

    if response.status_code == 200:
        data = response.json()
        hits = data.get('hits', {}).get('hits', [])
        for hit in hits:
            source = hit.get('_source', {})
            print(source)
    else:
        print("Failed to retrieve data from Elasticsearch")

if __name__ == "__main__":
    get_all_data_from_elasticsearch()
