import json


def load_data(path):
    with open(path, mode='r', encoding='utf-8') as file:
        return json.loads(file.read())
