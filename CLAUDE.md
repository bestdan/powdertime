# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Powdertime is a ski mountain weather monitoring application that tracks snowfall forecasts and sends notifications when significant snow is expected. It uses the Open-Meteo API (free, no API key required) to fetch 10-day forecasts for ski resorts near a user's location.

## Development Commands

### Running the Application
```bash
python run.py                          # Run with default config.yaml
python run.py --config config.local.yaml  # Run with custom config
python demo.py                         # Run demo with mock data (no internet required)
```

### Testing
```bash
python -m pytest tests/                # Run all tests
python -m pytest tests/test_analyzer.py  # Run specific test file
python tests/test_analyzer.py          # Run tests directly (has __main__ block)
```

### Dependencies
```bash
pip install -r requirements.txt        # Install: requests, pyyaml, geopy
```

## Architecture

### Core Data Flow
1. **Location Resolution** (`resorts.py`): Convert user location (city/state or lat/lon) to coordinates using geopy's Nominatim geocoder
2. **Resort Discovery** (`resorts.py`): Find ski resorts within radius using hardcoded `SKI_RESORTS` list (in-memory database of ~35 major US ski resorts)
3. **Weather Fetching** (`weather.py`): Fetch 10-day forecasts from Open-Meteo API for each resort
4. **Snow Analysis** (`analyzer.py`): Identify "significant events" where total snowfall exceeds threshold
5. **Notification** (`notifier.py`): Send alerts via console/email/webhook

### Key Components

**`main.py` - Application Orchestrator**
- `PowdertimeApp` class coordinates the entire workflow
- Entry point with CLI argument parsing
- Handles errors and user interrupts gracefully

**`config.py` - Configuration Management**
- Loads YAML config with `Config` class
- Provides property accessors for common config values
- Supports dot notation for nested keys (`get('location.city')`)

**`resorts.py` - Ski Resort Database**
- `SKI_RESORTS` is a hardcoded list of ~35 major US ski resorts with coordinates and elevations
- `ResortFinder` handles geocoding and distance calculations
- Uses geopy's `geodesic` for accurate distance measurements

**`weather.py` - Weather API Integration**
- `WeatherService` fetches from Open-Meteo API
- Returns `WeatherForecast` objects with snowfall (inches), temperature (°F), and date
- Converts snowfall from cm to inches (API returns metric)
- Hardcoded timezone to 'America/Denver'

**`analyzer.py` - Snow Event Detection**
- `SnowAnalyzer` finds forecasts exceeding threshold
- `SnowEvent` represents significant snowfall with resort, dates, totals
- Events sorted by total snowfall (descending)

**`notifier.py` - Notification System**
- Pluggable notification services via `NotificationService` base class
- Three implementations: `ConsoleNotification`, `EmailNotification`, `WebhookNotification`
- `NotificationManager` selects service based on config

### Configuration System

Users are expected to:
1. Copy `config.yaml` to `config.local.yaml`
2. Edit `config.local.yaml` with their location and preferences
3. Run with `--config config.local.yaml`

Config structure:
- `location`: Can use lat/lon (preferred) OR city/state/country (requires geocoding)
- `search_radius_miles`: How far to search for resorts
- `snow_threshold.min_inches`: Minimum snowfall to trigger alert
- `snow_threshold.forecast_days`: Forecast window (max 16 days)
- `notifications.method`: "console", "email", or "webhook"

#### Manual Resort Specification

Users can now specify resorts manually instead of location-based search:

```yaml
# Manual mode - skips location search
resorts:
  - name: "Hunter"              # By name from SKI_RESORTS
  - name: "Custom Hill"         # Custom with coordinates
    latitude: 42.0
    longitude: -74.0
    elevation: 2000
    state: "NY"
```

**Implementation details:**
- `Config.resorts` property returns `None` if not configured (triggers location-based search)
- `ResortFinder.get_resorts_from_config()` handles both name lookups and custom resorts
- Name lookups are case-insensitive and validated against `SKI_RESORTS` list
- Error messages list all available resorts when name not found
- Manual mode takes precedence over location config

### Python Version Compatibility

The codebase uses Python 3.10+ type hints (`from __future__ import annotations` is NOT used, so `list[...]` and `dict[...]` are used instead of `List[...]` and `Dict[...]` from typing). When adding new code, maintain this style for consistency.

## Important Implementation Details

### Ski Resort Database
The resort list in `resorts.py` is hardcoded and covers major resorts in CO, UT, CA, WY, VT, NH, NY (including Catskills: Hunter, Bellayre, Windham), MT, ID, WA. To add resorts, append to the `SKI_RESORTS` list with accurate coordinates and elevations.

### Weather API Limitations
- Open-Meteo API allows max 16 forecast days
- Snowfall is returned in cm and converted to inches
- API is free but has rate limits (not currently enforced in code)
- Timezone is hardcoded to 'America/Denver' - may cause issues for non-mountain-time resorts

### Distance Calculations
Uses `geopy.distance.geodesic()` for accurate great-circle distance. Returns miles, not kilometers.

### Testing Strategy
Tests use simple assert-based testing (not pytest fixtures). Each test file has a `__main__` block for direct execution. Tests use mock data rather than hitting real APIs.

## Common Development Patterns

### Adding a New Notification Method
1. Create a new class inheriting from `NotificationService` in `notifier.py`
2. Implement the `send(events, config)` method
3. Add to `NotificationManager.SERVICES` dictionary
4. Document the config structure in `config.yaml`

### Adding New Ski Resorts
Append to the `SKI_RESORTS` list in `resorts.py`:
```python
SkiResort("Resort Name", latitude, longitude, elevation_ft, "STATE")
```

### Modifying Weather Data Sources
If switching from Open-Meteo to another provider:
1. Update `WeatherService.BASE_URL` and `get_forecast()` params
2. Modify `_parse_forecast()` to handle new response format
3. Ensure snowfall is converted to inches if API returns metric
4. Update `config.yaml` with any required API keys
