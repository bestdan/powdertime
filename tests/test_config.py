"""
Tests for Powdertime configuration module
"""
import os
import tempfile
import yaml
from powdertime.config import Config


def test_config_loading():
    """Test configuration file loading"""
    # Create a temporary config file
    config_data = {
        'location': {
            'city': 'TestCity',
            'state': 'TS'
        },
        'search_radius_miles': 100,
        'snow_threshold': {
            'min_inches': 8,
            'forecast_days': 7
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config_data, f)
        temp_path = f.name
    
    try:
        # Load config
        config = Config(temp_path)
        
        # Test properties
        assert config.location['city'] == 'TestCity'
        assert config.search_radius_miles == 100
        assert config.snow_threshold_inches == 8
        assert config.forecast_days == 7
        
        print("✅ Config loading test passed")
    finally:
        os.unlink(temp_path)


def test_config_dot_notation():
    """Test dot notation key access"""
    config_data = {
        'notifications': {
            'email': {
                'smtp_server': 'smtp.example.com'
            }
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config_data, f)
        temp_path = f.name
    
    try:
        config = Config(temp_path)
        
        # Test dot notation
        assert config.get('notifications.email.smtp_server') == 'smtp.example.com'
        assert config.get('notifications.webhook.url', 'default') == 'default'
        
        print("✅ Config dot notation test passed")
    finally:
        os.unlink(temp_path)


if __name__ == '__main__':
    test_config_loading()
    test_config_dot_notation()
    print("\n✅ All config tests passed!")
