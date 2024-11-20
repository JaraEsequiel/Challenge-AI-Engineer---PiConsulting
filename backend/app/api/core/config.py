from dotenv import dotenv_values
from typing import Dict

# Settings class to manage environment variables and configuration
class Settings:
    _config: Dict  # Dictionary to store configuration values
    
    def __init__(self):
        """Initialize Settings by loading environment variables from .env file"""
        print("Loading environment variables from .env file...")
        self._config: Dict = dotenv_values()
        print(f"Loaded {len(self._config)} configuration values")
    
    def get(self, key: str, default=None):
        """
        Get a configuration value by key
        
        Args:
            key (str): The configuration key to look up
            default: Value to return if key is not found
            
        Returns:
            The configuration value or default if not found
        """
        value = self._config.get(key, default)
        return value
    
    def __getattr__(self, name: str):
        """
        Allow accessing config values as attributes
        Example: settings.DATABASE_URL instead of settings.get('DATABASE_URL')
        
        Args:
            name (str): The attribute name to look up
            
        Returns:
            The configuration value for the given attribute name
        """
        return self.get(name)

# Create a single instance to be imported by other modules
print("Initializing global Settings instance...")
settings = Settings()
