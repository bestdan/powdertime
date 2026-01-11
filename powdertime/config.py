"""
Configuration management for Powdertime
"""
import yaml
import os
from typing import Dict, Any


class Config:
    """Configuration loader and accessor"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Load configuration from YAML file
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'location.city')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    @property
    def location(self) -> Dict[str, Any]:
        """Get location configuration"""
        return self.config.get('location', {})
    
    @property
    def search_radius_miles(self) -> float:
        """Get search radius in miles"""
        return self.config.get('search_radius_miles', 100)
    
    @property
    def snow_threshold_inches(self) -> float:
        """Get minimum snow threshold in inches"""
        return self.config.get('snow_threshold', {}).get('min_inches', 6)
    
    @property
    def forecast_days(self) -> int:
        """Get number of forecast days to check"""
        return self.config.get('snow_threshold', {}).get('forecast_days', 10)
    
    @property
    def notification_method(self) -> str:
        """Get notification method"""
        return self.config.get('notifications', {}).get('method', 'console')
    
    @property
    def check_frequency_hours(self) -> int:
        """Get check frequency in hours"""
        return self.config.get('check_frequency_hours', 6)
