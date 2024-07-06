def remove_extra_nodes(data, limit):
    if 'nodes' not in data:
        return data
    
    nodes = data['nodes']
    if len(nodes) <= limit:
        return data
    
    node_ids_to_remove = [node['id'] for node in nodes[limit:]]
    new_edges = [edge for edge in data['edges'] if edge['source'] not in node_ids_to_remove and edge['target'] not in node_ids_to_remove]
    new_nodes = [node for node in nodes if node['id'] not in node_ids_to_remove]
    
    new_data = {'edges': new_edges, 'nodes': new_nodes}
    return new_data

