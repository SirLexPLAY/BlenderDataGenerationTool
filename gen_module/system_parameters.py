import json

class SystemConfiguration:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemConfiguration, cls).__new__(cls)
            cls._instance._read_config()
        return cls._instance

    def _read_config(self):
        with open("system_parameters.json") as file:
            self.config = json.load(file)
            
    
    def get(self, key, default=None):
        value = self.config.get(key)
        if value is None:
            return default
        return value