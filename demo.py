#!/usr/bin/env python3
"""
Demo script that showcases Powdertime with mock data

Since the weather API requires internet access, this demo uses mock data
to demonstrate the application's functionality.
"""
import sys
from datetime import datetime, timedelta
from powdertime.config import Config
from powdertime.resorts import ResortFinder, SkiResort
from powdertime.weather import WeatherForecast
from powdertime.analyzer import SnowAnalyzer
from powdertime.notifier import NotificationManager


def create_mock_forecasts(base_date, snowfall_pattern):
    """Create mock weather forecasts"""
    forecasts = []
    for i, snow in enumerate(snowfall_pattern):
        date = base_date + timedelta(days=i)
        temp = 28 - (snow * 2)  # Colder on snowier days
        forecasts.append(WeatherForecast(date, snow, temp))
    return forecasts


def main():
    print("🎿 Powdertime - Demo Mode (Mock Data)")
    print("=" * 70)
    
    # Load config
    config = Config("config.yaml")
    
    # Get location
    finder = ResortFinder()
    lat, lon = finder.get_coordinates(config.location)
    print(f"📍 Location: Denver, CO ({lat:.4f}, {lon:.4f})")
    
    # Find nearby resorts
    print(f"🔍 Searching for ski resorts within {config.search_radius_miles} miles...")
    nearby_resorts = finder.find_nearby_resorts(lat, lon, config.search_radius_miles)
    print(f"✅ Found {len(nearby_resorts)} resort(s)")
    
    # Show first few
    for resort in nearby_resorts[:5]:
        distance = resort.distance_from(lat, lon)
        print(f"   • {resort.name}, {resort.state} ({distance:.1f} miles)")
    if len(nearby_resorts) > 5:
        print(f"   ... and {len(nearby_resorts) - 5} more")
    
    # Create mock forecasts for demonstration
    print(f"\n🌤️  Generating mock {config.forecast_days}-day forecasts...")
    print("   (Using simulated data for demonstration)")
    
    base_date = datetime.now()
    resort_forecasts = {}
    
    # Create varied forecast patterns for different resorts
    patterns = [
        [0, 0, 4.5, 6.2, 3.8, 0, 0, 1.2, 0, 0],  # Major storm mid-week
        [0, 1.0, 2.0, 5.0, 4.0, 1.5, 0, 0, 0, 0],  # Extended storm
        [0, 0, 0, 0, 0, 0, 2.5, 3.5, 2.0, 1.0],  # Weekend storm
        [0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0],  # Minimal snow
        [1.0, 1.5, 2.0, 1.5, 1.0, 0.5, 0.5, 0, 0, 0],  # Steady but light
    ]
    
    for i, resort in enumerate(nearby_resorts[:5]):
        pattern = patterns[i % len(patterns)]
        forecasts = create_mock_forecasts(base_date, pattern)
        resort_forecasts[resort] = forecasts
        total_snow = sum(f.snowfall_inches for f in forecasts)
        print(f"   • {resort.name}: {total_snow:.1f}\" total")
    
    # Analyze for significant snowfall
    print(f"\n❄️  Analyzing for significant snowfall (threshold: {config.snow_threshold_inches}\")")
    analyzer = SnowAnalyzer(config.snow_threshold_inches)
    events = analyzer.find_significant_events(resort_forecasts)
    
    # Send notifications
    notification_manager = NotificationManager(config.get('notifications', {}))
    notification_manager.notify(events, resort_forecasts=resort_forecasts)
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
