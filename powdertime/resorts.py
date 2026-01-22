"""
Ski resort location finder

Finds ski resorts near a given location
"""
from typing import List, Dict, Tuple, Any
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


class SkiResort:
    """Represents a ski resort"""
    
    def __init__(self, name: str, latitude: float, longitude: float, 
                 elevation: int = None, state: str = None):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.state = state
    
    def distance_from(self, lat: float, lon: float) -> float:
        """Calculate distance from given coordinates in miles"""
        return geodesic((self.latitude, self.longitude), (lat, lon)).miles
    
    def __repr__(self):
        return f"SkiResort({self.name}, {self.state})"


# Major ski resorts in the United States
# In a production app, this would be loaded from a database or API
SKI_RESORTS = [
    # Colorado
    SkiResort("Vail", 39.6403, -106.3742, 8120, "CO"),
    SkiResort("Breckenridge", 39.4817, -106.0384, 9600, "CO"),
    SkiResort("Keystone", 39.6042, -105.9347, 9280, "CO"),
    SkiResort("Aspen Mountain", 39.1911, -106.8175, 7945, "CO"),
    SkiResort("Steamboat", 40.4572, -106.8047, 6900, "CO"),
    SkiResort("Winter Park", 39.8868, -105.7625, 9000, "CO"),
    SkiResort("Copper Mountain", 39.5019, -106.1503, 9712, "CO"),
    SkiResort("Arapahoe Basin", 39.6425, -105.8719, 10780, "CO"),
    SkiResort("Loveland", 39.6800, -105.8978, 10800, "CO"),
    SkiResort("Telluride", 37.9375, -107.8123, 8725, "CO"),
    
    # Utah
    SkiResort("Park City", 40.6514, -111.5079, 6900, "UT"),
    SkiResort("Alta", 40.5885, -111.6381, 8530, "UT"),
    SkiResort("Snowbird", 40.5833, -111.6572, 7760, "UT"),
    SkiResort("Deer Valley", 40.6374, -111.4783, 6570, "UT"),
    SkiResort("Brighton", 40.5981, -111.5831, 8755, "UT"),
    SkiResort("Solitude", 40.6199, -111.5916, 7988, "UT"),
    SkiResort("Snowbasin", 41.2161, -111.8567, 6400, "UT"),
    
    # Wyoming
    SkiResort("Jackson Hole", 43.5875, -110.8278, 6311, "WY"),
    
    # California
    SkiResort("Mammoth Mountain", 37.6308, -119.0326, 7953, "CA"),
    SkiResort("Palisades Tahoe", 39.1970, -120.2356, 6200, "CA"),
    SkiResort("Heavenly", 38.9350, -119.9403, 6565, "CA"),
    SkiResort("Northstar", 39.2731, -120.1186, 6330, "CA"),
    SkiResort("Kirkwood", 38.6836, -120.0661, 7800, "CA"),
    
    # Vermont
    SkiResort("Stowe", 44.5303, -72.7817, 1340, "VT"),
    SkiResort("Killington", 43.6042, -72.8203, 1290, "VT"),
    SkiResort("Sugarbush", 44.1358, -72.9028, 1535, "VT"),
    
    # New Hampshire
    SkiResort("Loon Mountain", 44.0364, -71.6208, 950, "NH"),
    SkiResort("Bretton Woods", 44.2625, -71.4431, 1500, "NH"),
    
    # New York
    SkiResort("Whiteface", 44.3656, -73.9025, 1220, "NY"),
    SkiResort("Hunter", 42.2042, -74.2172, 1600, "NY"),
    SkiResort("Bellayre", 42.127342, -74.518576, 2025, "NY"),
    SkiResort("Windham", 42.3600, -74.2900, 1500, "NY"),
    SkiResort("Plattekill Mountain", 42.2700, -74.6400, 3500, "NY"),
    SkiResort("Holiday Mountain", 41.6300, -74.6200, 1050, "NY"),
    SkiResort("Catamount", 42.1691, -73.4770, 2000, "NY"),

    # Massachusetts
    SkiResort("Butternut", 42.1867, -73.3203, 1800, "MA"),

    # Pennsylvania
    SkiResort("Camelback", 41.0423, -75.3521, 2133, "PA"),

    # Montana
    SkiResort("Big Sky", 45.2847, -111.4008, 7500, "MT"),

    # Idaho
    SkiResort("Sun Valley", 43.6972, -114.3517, 5750, "ID"),

    # Washington
    SkiResort("Crystal Mountain", 46.9358, -121.4747, 4400, "WA"),
    SkiResort("Stevens Pass", 47.7453, -121.0892, 4061, "WA"),
]


class ResortFinder:
    """Finds ski resorts near a given location"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="powdertime")
    
    def get_coordinates(self, location_config: Dict) -> Tuple[float, float]:
        """
        Get coordinates from location configuration
        
        Args:
            location_config: Location configuration dictionary
            
        Returns:
            Tuple of (latitude, longitude)
        """
        # Check if coordinates are directly provided
        if 'latitude' in location_config and 'longitude' in location_config:
            return (location_config['latitude'], location_config['longitude'])
        
        # Otherwise, geocode the location
        city = location_config.get('city', '')
        state = location_config.get('state', '')
        country = location_config.get('country', 'US')
        
        query = f"{city}, {state}, {country}" if state else f"{city}, {country}"
        
        location = self.geolocator.geocode(query)
        if not location:
            raise ValueError(f"Could not find coordinates for: {query}")
        
        return (location.latitude, location.longitude)
    
    def find_nearby_resorts(self, latitude: float, longitude: float, 
                          radius_miles: float) -> List[SkiResort]:
        """
        Find ski resorts within radius of given coordinates
        
        Args:
            latitude: Center point latitude
            longitude: Center point longitude
            radius_miles: Search radius in miles
            
        Returns:
            List of ski resorts within radius, sorted by distance
        """
        nearby_resorts = []
        
        for resort in SKI_RESORTS:
            distance = resort.distance_from(latitude, longitude)
            if distance <= radius_miles:
                nearby_resorts.append((resort, distance))
        
        # Sort by distance
        nearby_resorts.sort(key=lambda x: x[1])

        return [resort for resort, _ in nearby_resorts]

    def get_resorts_from_config(self, resorts_config: list[dict[str, Any]]) -> list[SkiResort]:
        """
        Get ski resorts from manual configuration

        Supports two formats:
        - By name: {'name': 'Vail'} - looks up in SKI_RESORTS
        - Custom: {'name': 'My Hill', 'latitude': 42.0, 'longitude': -74.0, ...}

        Args:
            resorts_config: List of resort configurations from config.yaml

        Returns:
            List of SkiResort objects

        Raises:
            ValueError: If resort name not found or required fields missing
        """
        resorts = []

        for resort_spec in resorts_config:
            # Name-based lookup
            if 'name' in resort_spec and 'latitude' not in resort_spec:
                resort_name = resort_spec['name']
                resort = self._find_resort_by_name(resort_name)
                if not resort:
                    available = ', '.join(r.name for r in SKI_RESORTS)
                    raise ValueError(
                        f"Resort '{resort_name}' not found in database. "
                        f"Available resorts: {available}"
                    )
                resorts.append(resort)

            # Custom resort with coordinates
            elif 'name' in resort_spec and 'latitude' in resort_spec and 'longitude' in resort_spec:
                resort = SkiResort(
                    name=resort_spec['name'],
                    latitude=resort_spec['latitude'],
                    longitude=resort_spec['longitude'],
                    elevation=resort_spec.get('elevation'),
                    state=resort_spec.get('state')
                )
                resorts.append(resort)

            else:
                raise ValueError(
                    f"Invalid resort specification: {resort_spec}. "
                    f"Must have 'name' (for lookup) or 'name' + 'latitude' + 'longitude' (for custom)"
                )

        return resorts

    def _find_resort_by_name(self, name: str) -> SkiResort | None:
        """
        Find resort in SKI_RESORTS by name (case-insensitive)

        Args:
            name: Resort name to search for

        Returns:
            SkiResort if found, None otherwise
        """
        name_lower = name.lower()
        for resort in SKI_RESORTS:
            if resort.name.lower() == name_lower:
                return resort
        return None

    def get_coordinates_from_zipcode(self, zipcode: str) -> Tuple[float, float]:
        """
        Get coordinates from US zipcode

        Args:
            zipcode: US zipcode (5 digits)

        Returns:
            Tuple of (latitude, longitude)

        Raises:
            ValueError: If zipcode cannot be geocoded
        """
        try:
            geolocator = Nominatim(user_agent="powdertime")
            location = geolocator.geocode(zipcode, country_codes='us')

            if location:
                return (location.latitude, location.longitude)
            else:
                raise ValueError(f"Could not geocode zipcode: {zipcode}")
        except Exception as e:
            raise ValueError(f"Geocoding error for zipcode {zipcode}: {e}")
