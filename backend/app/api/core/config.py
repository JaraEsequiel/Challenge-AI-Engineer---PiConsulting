from dotenv import dotenv_values
from typing import Dict, Any


class Settings:
    """Settings class to manage environment variables and configuration"""
    
    def __init__(self) -> None:
        """Initialize Settings by loading environment variables from .env file"""
        self._config: Dict[str, Any] = dotenv_values()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key.
        
        Args:
            key: The configuration key to look up
            default: Value to return if key is not found
            
        Returns:
            The configuration value or default if not found
        """
        return self._config.get(key, default)
    
    def __getattr__(self, name: str) -> Any:
        """Allow accessing config values as attributes.
        
        Example: settings.DATABASE_URL instead of settings.get('DATABASE_URL')
        
        Args:
            name: The attribute name to look up
            
        Returns:
            The configuration value for the given attribute name
        """
        return self.get(name)


settings = Settings()
