# Powdertime ❄️⛷️

Preemptive notification of good snow days

Powdertime is a weather monitoring application that tracks forecasts for ski mountains near your location and sends notifications when significant snowfall is expected.

## Features

- 🎿 **Automatic Resort Discovery**: Finds ski resorts within a configurable radius of your location
- 🌨️ **10-Day Forecast Monitoring**: Tracks snowfall predictions up to 10 days in advance
- 📊 **Smart Analysis**: Identifies significant snow accumulation events based on your threshold
- 📬 **Multiple Notification Methods**: Console output, email, or webhook notifications
- 🆓 **Free Weather Data**: Uses Open-Meteo API (no API key required)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bestdan/powdertime.git
cd powdertime
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Copy the example configuration and customize it:

```bash
cp config.yaml config.local.yaml
```

Edit `config.local.yaml` to set your location and preferences:

```yaml
location:
  city: "Denver"
  state: "CO"
  country: "US"

search_radius_miles: 150

snow_threshold:
  min_inches: 6
  forecast_days: 10

notifications:
  method: "console"  # Options: console, email, webhook
```

## Usage

Run the application:

```bash
python run.py
```

Or with a custom config file:

```bash
python run.py --config config.local.yaml
```

### Example Output

```
🎿 Powdertime - Ski Mountain Weather Monitor
======================================================================
📍 Location: Denver (39.7392, -104.9903)
🔍 Searching for ski resorts within 150 miles...
✅ Found 10 resort(s)
   • Loveland, CO (54.2 miles)
   • Arapahoe Basin, CO (55.8 miles)
   • Keystone, CO (65.1 miles)
   ...

🌤️  Fetching 10-day forecasts...
   • Loveland: 12.5" total
   • Arapahoe Basin: 11.8" total
   ...

❄️  Analyzing for significant snowfall (threshold: 6")

======================================================================
❄️  POWDER ALERT! Significant Snow Forecasted ❄️
======================================================================

Found 3 location(s) with significant snowfall:

1. 🎿 Loveland, CO
   Total: 12.5" over 4 day(s)
   Biggest day: 5.2"
   Snow days:
      • Mon Jan 13: 3.1" (High: 28°F)
      • Tue Jan 14: 5.2" (High: 25°F)
      • Wed Jan 15: 2.8" (High: 27°F)
      • Thu Jan 16: 1.4" (High: 30°F)
```

## Notification Methods

### Console
Prints alerts to the terminal (default method).

### Email
Sends email notifications via SMTP:

```yaml
notifications:
  method: "email"
  email:
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    from_email: "your-email@gmail.com"
    to_email: "recipient@gmail.com"
    password: "your-app-password"
```

### Webhook
Posts JSON data to a webhook URL:

```yaml
notifications:
  method: "webhook"
  webhook:
    url: "https://your-webhook-url.com/notify"
```

## Supported Regions

Currently includes major ski resorts in:
- Colorado (Vail, Breckenridge, Aspen, etc.)
- Utah (Park City, Alta, Snowbird, etc.)
- California (Mammoth, Tahoe resorts, etc.)
- Wyoming (Jackson Hole)
- Vermont (Stowe, Killington, etc.)
- New Hampshire, New York, Montana, Idaho, Washington

## Running on a Schedule

To run Powdertime automatically on a schedule, use cron:

```bash
# Run every 6 hours
0 */6 * * * cd /path/to/powdertime && python run.py
```

Or create a systemd timer for more control.

## Development

### Project Structure
```
powdertime/
├── powdertime/          # Main package
│   ├── __init__.py     # Package initialization
│   ├── main.py         # Application entry point
│   ├── config.py       # Configuration management
│   ├── resorts.py      # Ski resort finder
│   ├── weather.py      # Weather API integration
│   ├── analyzer.py     # Snow accumulation analyzer
│   └── notifier.py     # Notification system
├── config.yaml         # Example configuration
├── requirements.txt    # Python dependencies
└── run.py             # Convenience script
```

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.
