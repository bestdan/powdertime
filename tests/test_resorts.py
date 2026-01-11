"""
Tests for Powdertime ski resort finder
"""
from powdertime.resorts import ResortFinder, SkiResort


def test_resort_distance():
    """Test distance calculation"""
    resort = SkiResort("Test Resort", 39.6403, -106.3742, 8120, "CO")
    
    # Test distance from Denver
    denver_lat, denver_lon = 39.7392, -104.9903
    distance = resort.distance_from(denver_lat, denver_lon)
    
    # Vail is about 74 miles from Denver
    assert 70 < distance < 80, f"Expected ~74 miles, got {distance}"
    
    print(f"✅ Resort distance test passed: {distance:.1f} miles")


def test_find_nearby_resorts():
    """Test finding nearby resorts"""
    finder = ResortFinder()
    
    # Denver coordinates
    denver_lat, denver_lon = 39.7392, -104.9903
    
    # Find resorts within 60 miles (should find several)
    nearby = finder.find_nearby_resorts(denver_lat, denver_lon, 60)
    
    assert len(nearby) > 0, "Should find at least one resort"
    assert len(nearby) < 10, "Should not find too many resorts"
    
    # Check that results are sorted by distance
    distances = [r.distance_from(denver_lat, denver_lon) for r in nearby]
    assert distances == sorted(distances), "Results should be sorted by distance"
    
    print(f"✅ Find nearby resorts test passed: found {len(nearby)} resorts")


def test_coordinate_parsing():
    """Test coordinate parsing from config"""
    finder = ResortFinder()
    
    # Test with direct coordinates
    config = {
        'latitude': 40.0,
        'longitude': -105.0
    }
    lat, lon = finder.get_coordinates(config)
    assert lat == 40.0
    assert lon == -105.0
    
    print("✅ Coordinate parsing test passed")


if __name__ == '__main__':
    test_resort_distance()
    test_find_nearby_resorts()
    test_coordinate_parsing()
    print("\n✅ All resort tests passed!")
