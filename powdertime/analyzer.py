"""
Snow accumulation analyzer

Analyzes weather forecasts to detect significant snowfall events
"""
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from .weather import WeatherForecast
from .resorts import SkiResort


class SnowEvent:
    """Represents a significant snowfall event at a resort"""
    
    def __init__(self, resort: SkiResort, forecasts: List[WeatherForecast],
                 total_snowfall: float, max_daily_snowfall: float):
        self.resort = resort
        self.forecasts = forecasts
        self.total_snowfall = total_snowfall
        self.max_daily_snowfall = max_daily_snowfall
        self.start_date = forecasts[0].date if forecasts else None
        self.end_date = forecasts[-1].date if forecasts else None
    
    def __repr__(self):
        return f"SnowEvent({self.resort.name}, {self.total_snowfall:.1f}in)"
    
    def get_summary(self) -> str:
        """Get human-readable summary of snow event"""
        days_with_snow = [f for f in self.forecasts if f.snowfall_inches > 0]
        
        summary = f"🎿 {self.resort.name}, {self.resort.state}\n"
        summary += f"   Total: {self.total_snowfall:.1f}\" over {len(days_with_snow)} day(s)\n"
        summary += f"   Biggest day: {self.max_daily_snowfall:.1f}\"\n"
        summary += f"   Snow days:\n"
        
        for forecast in days_with_snow:
            date_str = forecast.date.strftime('%a %b %d')
            summary += f"      • {date_str}: {forecast.snowfall_inches:.1f}\""
            if forecast.temperature_f:
                summary += f" (High: {forecast.temperature_f:.0f}°F)"
            summary += "\n"
        
        return summary


class SnowAnalyzer:
    """Analyzes weather forecasts for significant snowfall"""
    
    def __init__(self, threshold_inches: float = 6.0):
        """
        Initialize analyzer
        
        Args:
            threshold_inches: Minimum snowfall to be considered significant
        """
        self.threshold_inches = threshold_inches
    
    def analyze_forecast(self, resort: SkiResort, 
                        forecasts: List[WeatherForecast]) -> Optional[SnowEvent]:
        """
        Analyze forecast for significant snowfall
        
        Args:
            resort: Ski resort
            forecasts: Weather forecasts
            
        Returns:
            SnowEvent if significant snow is forecasted, None otherwise
        """
        if not forecasts:
            return None
        
        # Calculate total snowfall
        total_snowfall = sum(f.snowfall_inches for f in forecasts)
        
        # Check if it meets threshold
        if total_snowfall < self.threshold_inches:
            return None
        
        # Calculate max daily snowfall
        max_daily = max((f.snowfall_inches for f in forecasts), default=0)
        
        # Only include days with snow in the event
        snow_days = [f for f in forecasts if f.snowfall_inches > 0]
        
        return SnowEvent(
            resort=resort,
            forecasts=snow_days,
            total_snowfall=total_snowfall,
            max_daily_snowfall=max_daily
        )
    
    def find_significant_events(self, resort_forecasts: Dict[SkiResort, List[WeatherForecast]]) -> List[SnowEvent]:
        """
        Find all significant snow events from resort forecasts
        
        Args:
            resort_forecasts: Dictionary mapping resorts to their forecasts
            
        Returns:
            List of significant SnowEvent objects, sorted by total snowfall
        """
        events = []
        
        for resort, forecasts in resort_forecasts.items():
            event = self.analyze_forecast(resort, forecasts)
            if event:
                events.append(event)
        
        # Sort by total snowfall (descending)
        events.sort(key=lambda e: e.total_snowfall, reverse=True)
        
        return events
