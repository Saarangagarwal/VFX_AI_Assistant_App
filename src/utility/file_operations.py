import json

def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    

def write_json_to_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
        