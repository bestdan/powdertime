#!/usr/bin/env python3
"""
Powdertime - Ski Mountain Weather Monitor

Main application that monitors weather forecasts for ski mountains
and sends notifications about significant snowfall.
"""
import sys
import argparse
from typing import Dict
from .config import Config
from .resorts import ResortFinder
from .weather import WeatherService
from .analyzer import SnowAnalyzer
from .notifier import NotificationManager


class PowdertimeApp:
    """Main application orchestrator"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize application
        
        Args:
            config_path: Path to configuration file
        """
        self.config = Config(config_path)
        self.resort_finder = ResortFinder()
        self.weather_service = WeatherService()
        self.snow_analyzer = SnowAnalyzer(self.config.snow_threshold_inches)
        self.notification_manager = NotificationManager(
            self.config.get('notifications', {})
        )
    
    def run(self):
        """Run the main monitoring loop"""
        print("🎿 Powdertime - Ski Mountain Weather Monitor")
        print("=" * 70)
        
        # Get user location
        try:
            lat, lon = self.resort_finder.get_coordinates(self.config.location)
            location_name = self.config.location.get('city', 'Unknown')
            print(f"📍 Location: {location_name} ({lat:.4f}, {lon:.4f})")
        except Exception as e:
            print(f"❌ Error: Could not determine location: {e}")
            return 1
        
        # Find nearby resorts
        radius = self.config.search_radius_miles
        print(f"🔍 Searching for ski resorts within {radius} miles...")
        nearby_resorts = self.resort_finder.find_nearby_resorts(lat, lon, radius)
        
        if not nearby_resorts:
            print(f"❌ No ski resorts found within {radius} miles")
            return 1
        
        print(f"✅ Found {len(nearby_resorts)} resort(s)")
        for resort in nearby_resorts:
            distance = resort.distance_from(lat, lon)
            print(f"   • {resort.name}, {resort.state} ({distance:.1f} miles)")
        
        # Fetch weather forecasts
        print(f"\n🌤️  Fetching {self.config.forecast_days}-day forecasts...")
        resort_forecasts = {}
        
        for resort in nearby_resorts:
            forecasts = self.weather_service.get_forecast(
                resort.latitude,
                resort.longitude,
                self.config.forecast_days
            )
            if forecasts:
                resort_forecasts[resort] = forecasts
                total_snow = sum(f.snowfall_inches for f in forecasts)
                print(f"   • {resort.name}: {total_snow:.1f}\" total")
        
        # Analyze for significant snowfall
        print(f"\n❄️  Analyzing for significant snowfall (threshold: {self.config.snow_threshold_inches}\")")
        events = self.snow_analyzer.find_significant_events(resort_forecasts)
        
        # Send notifications
        self.notification_manager.notify(events)
        
        return 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Monitor ski mountain weather forecasts for significant snowfall'
    )
    parser.add_argument(
        '-c', '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        app = PowdertimeApp(args.config)
        sys.exit(app.run())
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\nPlease create a config.yaml file. See config.yaml for an example.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
