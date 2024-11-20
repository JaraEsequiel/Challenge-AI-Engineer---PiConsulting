from dotenv import dotenv_values
from typing import Dict

class Settings:
    _config: Dict
    def __init__(self):
        self._config: Dict = dotenv_values()
        print("config: ", self._config)
    
    def get(self, key: str, default=None):
        """Get a configuration value by key"""
        return self._config.get(key, default)
    
    def __getattr__(self, name: str):
        """Allow accessing config values as attributes"""
        return self.get(name)

# Create a single instance to be imported by other modules
settings = Settings()
