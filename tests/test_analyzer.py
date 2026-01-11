"""
Tests for Powdertime snow analyzer
"""
from datetime import datetime
from powdertime.analyzer import SnowAnalyzer, SnowEvent
from powdertime.weather import WeatherForecast
from powdertime.resorts import SkiResort


def test_analyze_forecast_significant():
    """Test analyzing forecast with significant snow"""
    analyzer = SnowAnalyzer(threshold_inches=6.0)
    resort = SkiResort("Test Resort", 39.0, -106.0, 9000, "CO")
    
    forecasts = [
        WeatherForecast(datetime(2026, 1, 12), 3.0, 28.0),
        WeatherForecast(datetime(2026, 1, 13), 5.0, 25.0),
        WeatherForecast(datetime(2026, 1, 14), 2.0, 27.0),
        WeatherForecast(datetime(2026, 1, 15), 0.0, 30.0),
    ]
    
    event = analyzer.analyze_forecast(resort, forecasts)
    
    assert event is not None, "Should detect significant snow event"
    assert event.total_snowfall == 10.0
    assert event.max_daily_snowfall == 5.0
    assert len(event.forecasts) == 3, "Should only include days with snow"
    
    print("✅ Significant snow analysis test passed")


def test_analyze_forecast_insignificant():
    """Test analyzing forecast with insignificant snow"""
    analyzer = SnowAnalyzer(threshold_inches=6.0)
    resort = SkiResort("Test Resort", 39.0, -106.0, 9000, "CO")
    
    forecasts = [
        WeatherForecast(datetime(2026, 1, 12), 1.0, 28.0),
        WeatherForecast(datetime(2026, 1, 13), 2.0, 25.0),
        WeatherForecast(datetime(2026, 1, 14), 1.5, 27.0),
    ]
    
    event = analyzer.analyze_forecast(resort, forecasts)
    
    assert event is None, "Should not detect event below threshold"
    
    print("✅ Insignificant snow analysis test passed")


def test_find_significant_events():
    """Test finding significant events from multiple resorts"""
    analyzer = SnowAnalyzer(threshold_inches=6.0)
    
    resort1 = SkiResort("Resort A", 39.0, -106.0, 9000, "CO")
    resort2 = SkiResort("Resort B", 40.0, -107.0, 8500, "CO")
    
    forecasts1 = [
        WeatherForecast(datetime(2026, 1, 12), 8.0, 28.0),
    ]
    
    forecasts2 = [
        WeatherForecast(datetime(2026, 1, 12), 2.0, 28.0),
    ]
    
    resort_forecasts = {
        resort1: forecasts1,
        resort2: forecasts2
    }
    
    events = analyzer.find_significant_events(resort_forecasts)
    
    assert len(events) == 1, "Should find only one significant event"
    assert events[0].resort.name == "Resort A"
    
    print("✅ Find significant events test passed")


if __name__ == '__main__':
    test_analyze_forecast_significant()
    test_analyze_forecast_insignificant()
    test_find_significant_events()
    print("\n✅ All analyzer tests passed!")
