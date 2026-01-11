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


def test_resorts_property_returns_none_when_absent():
    """Test that resorts property returns None when not configured"""
    # Test backward compatibility
    config_data = {'location': {'latitude': 40.0, 'longitude': -105.0}, 'search_radius_miles': 100}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config_data, f)
        temp_path = f.name
    try:
        config = Config(temp_path)
        assert config.resorts is None
        assert config.location['latitude'] == 40.0
        print("✅ Resorts property default test passed")
    finally:
        os.unlink(temp_path)


def test_resorts_property_returns_list():
    """Test that resorts property returns list when configured"""
    config_data = {'resorts': [{'name': 'Vail'}, {'name': 'Custom', 'latitude': 40.0, 'longitude': -105.0}]}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config_data, f)
        temp_path = f.name
    try:
        config = Config(temp_path)
        assert config.resorts is not None
        assert len(config.resorts) == 2
        print("✅ Resorts property with list test passed")
    finally:
        os.unlink(temp_path)


if __name__ == '__main__':
    test_config_loading()
    test_config_dot_notation()
    test_resorts_property_returns_none_when_absent()
    test_resorts_property_returns_list()
    print("\n✅ All config tests passed!")
