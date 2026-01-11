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


def test_get_resorts_by_name():
    """Test getting resorts by name from config"""
    finder = ResortFinder()
    config = [{'name': 'Vail'}, {'name': 'breckenridge'}]  # Test case-insensitive
    resorts = finder.get_resorts_from_config(config)
    assert len(resorts) == 2
    assert resorts[0].name == "Vail"
    assert resorts[1].name == "Breckenridge"
    print("✅ Get resorts by name test passed")


def test_get_custom_resorts():
    """Test custom resort specification with coordinates"""
    finder = ResortFinder()
    config = [{'name': 'My Custom Resort', 'latitude': 42.0, 'longitude': -74.0, 'elevation': 2000, 'state': 'NY'}]
    resorts = finder.get_resorts_from_config(config)
    assert len(resorts) == 1
    assert resorts[0].name == "My Custom Resort"
    assert resorts[0].latitude == 42.0
    print("✅ Custom resort test passed")


def test_invalid_resort_name():
    """Test error handling for invalid resort name"""
    finder = ResortFinder()
    config = [{'name': 'Nonexistent Resort'}]
    try:
        finder.get_resorts_from_config(config)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "not found in database" in str(e)
        assert "Available resorts:" in str(e)
    print("✅ Invalid resort name error test passed")


def test_mixed_resort_config():
    """Test mixing named and custom resorts"""
    finder = ResortFinder()
    config = [
        {'name': 'Vail'},
        {'name': 'Custom Hill', 'latitude': 40.0, 'longitude': -105.0}
    ]
    resorts = finder.get_resorts_from_config(config)
    assert len(resorts) == 2
    assert resorts[0].name == "Vail"
    assert resorts[1].name == "Custom Hill"
    print("✅ Mixed resort config test passed")


def test_catskills_resorts_exist():
    """Test that Catskills resorts are in database"""
    finder = ResortFinder()
    hunter = finder._find_resort_by_name("Hunter")
    bellayre = finder._find_resort_by_name("Bellayre")
    windham = finder._find_resort_by_name("Windham")
    assert hunter is not None and hunter.state == "NY"
    assert bellayre is not None and bellayre.state == "NY"
    assert windham is not None and windham.state == "NY"
    print("✅ Catskills resorts exist test passed")


def test_find_resort_by_name():
    """Test case-insensitive resort name lookup"""
    finder = ResortFinder()
    vail1 = finder._find_resort_by_name("Vail")
    vail2 = finder._find_resort_by_name("vail")
    vail3 = finder._find_resort_by_name("VAIL")
    assert vail1 == vail2 == vail3
    assert vail1.name == "Vail"
    print("✅ Find resort by name test passed")


if __name__ == '__main__':
    test_resort_distance()
    test_find_nearby_resorts()
    test_coordinate_parsing()
    test_get_resorts_by_name()
    test_get_custom_resorts()
    test_invalid_resort_name()
    test_mixed_resort_config()
    test_catskills_resorts_exist()
    test_find_resort_by_name()
    print("\n✅ All resort tests passed!")
