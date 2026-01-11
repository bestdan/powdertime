"""
Weather forecast fetcher

Fetches weather forecasts for ski resort locations
"""
import requests
from typing import Dict, List, Any
from datetime import datetime, timedelta


class WeatherForecast:
    """Represents weather forecast for a location"""
    
    def __init__(self, date: datetime, snowfall_inches: float, 
                 temperature_f: float = None, conditions: str = None):
        self.date = date
        self.snowfall_inches = snowfall_inches
        self.temperature_f = temperature_f
        self.conditions = conditions
    
    def __repr__(self):
        return f"WeatherForecast({self.date.strftime('%Y-%m-%d')}, {self.snowfall_inches}in)"


class WeatherService:
    """Fetches weather forecasts using Open-Meteo API"""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def get_forecast(self, latitude: float, longitude: float, 
                    days: int = 10) -> List[WeatherForecast]:
        """
        Get weather forecast for a location
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            days: Number of days to forecast (max 16)
            
        Returns:
            List of WeatherForecast objects
        """
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'daily': 'snowfall_sum,temperature_2m_max',
            'temperature_unit': 'fahrenheit',
            'forecast_days': min(days, 16),
            'timezone': 'America/Denver'
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return self._parse_forecast(data)
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return []
    
    def _parse_forecast(self, data: Dict[str, Any]) -> List[WeatherForecast]:
        """Parse API response into WeatherForecast objects"""
        forecasts = []
        
        daily = data.get('daily', {})
        times = daily.get('time', [])
        snowfall = daily.get('snowfall_sum', [])
        temps = daily.get('temperature_2m_max', [])
        
        for i, date_str in enumerate(times):
            date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # Convert snowfall from cm to inches
            snowfall_cm = snowfall[i] if i < len(snowfall) else 0
            snowfall_inches = snowfall_cm / 2.54 if snowfall_cm else 0
            
            temp_f = temps[i] if i < len(temps) else None
            
            forecasts.append(WeatherForecast(
                date=date,
                snowfall_inches=snowfall_inches,
                temperature_f=temp_f
            ))
        
        return forecasts
    
    def get_total_snowfall(self, forecasts: List[WeatherForecast]) -> float:
        """Calculate total snowfall from forecasts"""
        return sum(f.snowfall_inches for f in forecasts)
    
    def get_max_daily_snowfall(self, forecasts: List[WeatherForecast]) -> float:
        """Get maximum single-day snowfall from forecasts"""
        return max((f.snowfall_inches for f in forecasts), default=0)
