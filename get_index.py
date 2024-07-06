import requests

def search_data_in_elasticsearch(query_string):
    es_url = 'http://192.168.1.106:9200'
    index_name = ['nadra_persons','sim_information','']  # Replace with the actual name of your Elasticsearch index

    #url = f"{es_url}/{','.join(index_name)}/_search"
    url = f"{es_url}/_search"
    headers = {'Content-Type': 'application/json'}

    query = {
        "query": {
    "match": {
      "transaction_id":3
    }
  },
    "size": 160
    }


    response = requests.get(url, json=query, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to execute the search query")
        return None

if __name__ == "__main__":
    query_string = "search_term_here"
    search_result = search_data_in_elasticsearch(query_string)
    print(search_result)
