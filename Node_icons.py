import json

import json

def addNode_icon(node_label, icon):
    try:
        with open('Node_icons.json', 'r') as json_file:
            data = json.load(json_file)

    except FileNotFoundError:
        print("File not found, creating a new one")
        data = []

    label_exists = False

    for entry in data:
        if entry.get("Node") == node_label:
            entry["iconLabel"] = icon
            label_exists = True
            break

    if not label_exists:
        new_entry = {"Node": node_label, "iconLabel": icon}

        data.append(new_entry)

    with open('Node_icons.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


def get_node_icon(node_labels):
    # Normalize the case of node_labels to lowercase
    node_labels = [label for label in node_labels]

    # Read the JSON data from the file.
    print("node labels: ",node_labels)
    try:
        with open('Node_icons.json', 'r') as json_file:
            data = json.load(json_file)
            print("data: ",data)

    except FileNotFoundError:
        return []

    # Normalize the case of "Node" and "iconLabel" values in data to lowercase and filter
    filtered_data = [
        entry for entry in data 
        if entry.get("Node", "") in node_labels or
           entry.get("iconLabel", "") in node_labels
    ]

    return filtered_data






