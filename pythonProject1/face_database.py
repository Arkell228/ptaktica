import json
import os

class FaceDateBase:
    def __init__(self, json_folder):
        self.json_folder = json_folder
        self.metadata_dict = {}
        self.load_metadata()

    def load_metadata(self):
        for filename in os.listdir(self.json_folder):
            if filename.endswith('.json'):
                with open(os.path.join(self.json_folder, filename), 'r') as f:
                    data = json.load(f)
                person_name = data['name']
                self.metadata_dict[person_name] = data

    def get_metadata(self, person_name):
        return self.metadata_dict.get(person_name)