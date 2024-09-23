import json
import os

class SystemConfiguration:
    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemConfiguration, cls).__new__(cls)
            cls._instance._read_config()
        return cls._instance


    def _read_config(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(script_dir, "system_parameters.json")
        try:
            with open(json_file_path, 'r') as file:
                self.config = json.load(file)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            self.config = {}
            
    
    def get(self, key, default=None):
        value = self.config.get(key)
        if value is None:
            return default
        return value