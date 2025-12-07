import json
import os

class JsonLoader:

    def __init__(self):
        self.dir = "resources"

    def load(self,title) -> dict:
        file_path = os.path.join(self.dir, f'{title}.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
json_loader = JsonLoader()