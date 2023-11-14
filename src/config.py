import yaml
import os

class Config:
    def __init__(self, path):
        self.defaultConfig = {
            "db": {
                "host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "password": "",
                "database": "creatia_panel"
            },
            "rcon": {
                "host": "127.0.0.1",
                "password": "",
                "port": 25575
            }
        }
        self.path = path
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.path):
            self.create_config()
        with open(self.path, "r") as f:
            return yaml.load(f, Loader=yaml.FullLoader)
        
    def create_config(self):
        with open(self.path, "w") as f:
            yaml.dump(self.defaultConfig, f, default_flow_style=False)

    def getDBHost(self):
        return self.config['db']['host']
    
    def getDBPort(self):
        return self.config['db']['port']
    
    def getDBUser(self):
        return self.config['db']['user']
    
    def getDBPassword(self):
        return self.config['db']['password']
    
    def getDBDatabase(self):
        return self.config['db']['database']
    
    def getRCONHost(self):
        return self.config['rcon']['host']
    
    def getRCONPort(self):
        return self.config['rcon']['port']
    
    def getRCONPassword(self):
        return self.config['rcon']['password']
    
    def save_config(self):
        with open(self.path, "w") as f:
            yaml.dump(self.config, f, default_flow_style=False)

if __name__ == '__main__':
    Config('config.yml')