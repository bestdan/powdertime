"""
Tests for Powdertime notification system
"""
from datetime import datetime
from io import StringIO
import sys
from powdertime.notifier import ConsoleNotification, NotificationManager
from powdertime.analyzer import SnowEvent
from powdertime.weather import WeatherForecast
from powdertime.resorts import SkiResort


def test_console_notification_with_forecasts():
    """Test console notification includes forecast summary"""
    notifier = ConsoleNotification()
    
    # Create test data
    resort1 = SkiResort("Test Resort A", 39.0, -106.0, 9000, "CO")
    resort2 = SkiResort("Test Resort B", 40.0, -107.0, 8500, "CO")
    
    forecasts1 = [
        WeatherForecast(datetime(2026, 1, 12), 8.0, 28.0),
        WeatherForecast(datetime(2026, 1, 13), 0.0, 30.0),
    ]
    
    forecasts2 = [
        WeatherForecast(datetime(2026, 1, 12), 2.0, 28.0),
        WeatherForecast(datetime(2026, 1, 13), 1.0, 30.0),
    ]
    
    resort_forecasts = {
        resort1: forecasts1,
        resort2: forecasts2
    }
    
    # Create event for resort1 only
    event = SnowEvent(resort1, [forecasts1[0]], 8.0, 8.0)
    
    # Capture output
    captured_output = StringIO()
    sys.stdout = captured_output
    
    notifier.send([event], {}, resort_forecasts=resort_forecasts)
    
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    
    # Verify forecast summary is present
    assert "📊 Forecast Summary:" in output, "Should include forecast summary header"
    assert "Test Resort A: 8.0\" total" in output, "Should show resort A forecast"
    assert "Test Resort B: 3.0\" total" in output, "Should show resort B forecast"
    
    # Verify powder alert is present
    assert "POWDER ALERT" in output, "Should show powder alert"
    
    print("✅ Console notification with forecasts test passed")


def test_console_notification_no_events_with_forecasts():
    """Test console notification with forecasts but no significant events"""
    notifier = ConsoleNotification()
    
    # Create test data
    resort1 = SkiResort("Test Resort A", 39.0, -106.0, 9000, "CO")
    
    forecasts1 = [
        WeatherForecast(datetime(2026, 1, 12), 1.0, 28.0),
        WeatherForecast(datetime(2026, 1, 13), 0.5, 30.0),
    ]
    
    resort_forecasts = {
        resort1: forecasts1
    }
    
    # Capture output
    captured_output = StringIO()
    sys.stdout = captured_output
    
    notifier.send([], {}, resort_forecasts=resort_forecasts)
    
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    
    # Verify forecast summary is present
    assert "📊 Forecast Summary:" in output, "Should include forecast summary header"
    assert "Test Resort A: 1.5\" total" in output, "Should show resort A forecast"
    
    # Verify no significant snow message
    assert "No significant snowfall" in output, "Should show no significant snow message"
    
    print("✅ Console notification without events but with forecasts test passed")


def test_console_notification_without_forecasts():
    """Test console notification works without forecast data (backward compatibility)"""
    notifier = ConsoleNotification()
    
    # Create test data
    resort1 = SkiResort("Test Resort A", 39.0, -106.0, 9000, "CO")
    
    forecasts1 = [
        WeatherForecast(datetime(2026, 1, 12), 8.0, 28.0),
    ]
    
    # Create event for resort1
    event = SnowEvent(resort1, forecasts1, 8.0, 8.0)
    
    # Capture output
    captured_output = StringIO()
    sys.stdout = captured_output
    
    # Call without resort_forecasts parameter
    notifier.send([event], {})
    
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    
    # Verify forecast summary is NOT present
    assert "📊 Forecast Summary:" not in output, "Should not include forecast summary when not provided"
    
    # Verify powder alert is still present
    assert "POWDER ALERT" in output, "Should show powder alert"
    
    print("✅ Console notification without forecasts (backward compatibility) test passed")


if __name__ == '__main__':
    test_console_notification_with_forecasts()
    test_console_notification_no_events_with_forecasts()
    test_console_notification_without_forecasts()
    print("\n✅ All notifier tests passed!")
