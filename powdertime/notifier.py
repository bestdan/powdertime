"""
Notification system

Sends notifications about significant snowfall events
"""
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from .analyzer import SnowEvent
from .weather import WeatherForecast
from .resorts import SkiResort


class NotificationService:
    """Base notification service"""

    def send(self, events: List[SnowEvent], config: Dict[str, Any], always_notify: bool = False, 
             resort_forecasts: Dict[SkiResort, List[WeatherForecast]] = None):
        """
        Send notification about snow events

        Args:
            events: List of SnowEvent objects
            config: Notification configuration
            always_notify: If True, send notification even when no events
            resort_forecasts: Optional dict mapping resorts to their full forecasts
        """
        raise NotImplementedError


class ConsoleNotification(NotificationService):
    """Console notification - prints to stdout"""

    def send(self, events: List[SnowEvent], config: Dict[str, Any], always_notify: bool = False,
             resort_forecasts: Dict[SkiResort, List[WeatherForecast]] = None):
        """Print snow events to console"""
        
        # Display forecast totals if available
        if resort_forecasts:
            print("\n📊 Forecast Summary:")
            for resort, forecasts in resort_forecasts.items():
                total_snow = sum(f.snowfall_inches for f in forecasts)
                print(f"   • {resort.name}: {total_snow:.1f}\" total")
        
        if not events:
            print("\n✅ No significant snowfall forecasted in the next 10 days.")
            return

        print("\n" + "=" * 70)
        print("❄️  POWDER ALERT! Significant Snow Forecasted ❄️")
        print("=" * 70)
        print(f"\nFound {len(events)} location(s) with significant snowfall:\n")

        for i, event in enumerate(events, 1):
            print(f"{i}. {event.get_summary()}")

        print("=" * 70 + "\n")


class EmailNotification(NotificationService):
    """Email notification via SMTP"""

    def send(self, events: List[SnowEvent], config: Dict[str, Any], always_notify: bool = False,
             resort_forecasts: Dict[SkiResort, List[WeatherForecast]] = None):
        """Send snow events via email"""
        email_config = config.get('email', {})
        smtp_server = email_config.get('smtp_server')
        smtp_port = email_config.get('smtp_port', 587)
        from_email = email_config.get('from_email')
        to_email = email_config.get('to_email')
        password = email_config.get('password')

        if not all([smtp_server, from_email, to_email, password]):
            print("Error: Email configuration incomplete")
            return

        # If no events but always_notify, send confirmation email
        if not events and always_notify:
            self._send_no_snow_email(email_config, resort_forecasts)
            return

        # No events and not always_notify - skip
        if not events:
            return

        # Create message for snow events
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = f"❄️ Powder Alert! {len(events)} Resort(s) with Significant Snow"

        # Create body
        body = ""
        
        # Add forecast summary if available
        if resort_forecasts:
            body += "Forecast Summary:\n"
            for resort, forecasts in resort_forecasts.items():
                total_snow = sum(f.snowfall_inches for f in forecasts)
                body += f"  • {resort.name}: {total_snow:.1f}\" total\n"
            body += "\n"
        
        body += "Significant snowfall forecasted at the following resort(s):\n\n"
        for event in events:
            body += event.get_summary() + "\n"

        msg.attach(MIMEText(body, 'plain'))

        try:
            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            server.quit()
            print(f"✅ Email notification sent to {to_email}")
        except Exception as e:
            print(f"Error sending email: {e}")

    def _send_no_snow_email(self, email_config: Dict[str, Any], 
                            resort_forecasts: Dict[SkiResort, List[WeatherForecast]] = None):
        """Send confirmation email when no snow detected"""
        smtp_server = email_config.get('smtp_server')
        smtp_port = email_config.get('smtp_port', 587)
        from_email = email_config.get('from_email')
        to_email = email_config.get('to_email')
        password = email_config.get('password')

        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = "✅ Powdertime Check Complete - No Significant Snow"

        body = "Powdertime ran successfully.\n\n"
        
        # Add forecast summary if available
        if resort_forecasts:
            body += "Forecast Summary:\n"
            for resort, forecasts in resort_forecasts.items():
                total_snow = sum(f.snowfall_inches for f in forecasts)
                body += f"  • {resort.name}: {total_snow:.1f}\" total\n"
            body += "\n"
        
        body += "No significant snowfall forecasted at monitored resorts.\n"
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            server.quit()
            print(f"✅ Confirmation email sent to {to_email}")
        except Exception as e:
            print(f"Error sending email: {e}")


class WebhookNotification(NotificationService):
    """Webhook notification - POST to URL"""

    def send(self, events: List[SnowEvent], config: Dict[str, Any], always_notify: bool = False,
             resort_forecasts: Dict[SkiResort, List[WeatherForecast]] = None):
        """Send snow events to webhook"""
        webhook_config = config.get('webhook', {})
        url = webhook_config.get('url')

        if not url:
            print("Error: Webhook URL not configured")
            return

        # If no events but always_notify, send confirmation message
        if not events and always_notify:
            self._send_no_snow_webhook(url, resort_forecasts)
            return

        # No events and not always_notify - skip
        if not events:
            return

        # Format message for Slack compatibility
        message_lines = [
            "❄️ *POWDER ALERT!* Significant Snow Forecasted ❄️",
            "",
        ]
        
        # Add forecast summary if available
        if resort_forecasts:
            message_lines.append("*Forecast Summary:*")
            for resort, forecasts in resort_forecasts.items():
                total_snow = sum(f.snowfall_inches for f in forecasts)
                message_lines.append(f"  • {resort.name}: {total_snow:.1f}\" total")
            message_lines.append("")
        
        message_lines.append(f"Found {len(events)} location(s) with significant snowfall:")
        message_lines.append("")

        for i, event in enumerate(events, 1):
            message_lines.append(f"{i}. *{event.resort.name}* ({event.resort.state})")
            message_lines.append(f"   • Total: *{event.total_snowfall:.1f} inches*")
            message_lines.append(f"   • Period: {event.start_date.strftime('%b %d')} to {event.end_date.strftime('%b %d')}")
            message_lines.append(f"   • Max daily: {event.max_daily_snowfall:.1f} inches")
            message_lines.append("")

        text = "\n".join(message_lines)

        # Slack-compatible payload with required "text" field
        payload = {
            'text': text,
            'attachments': [
                {
                    'color': '#36a64f',
                    'fields': [
                        {
                            'title': event.resort.name + ', ' + event.resort.state,
                            'value': f"{event.total_snowfall:.1f}\" total ({event.start_date.strftime('%b %d')} - {event.end_date.strftime('%b %d')})",
                            'short': True
                        }
                        for event in events[:5]  # Limit to 5 for readability
                    ]
                }
            ]
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            print(f"✅ Webhook notification sent to {url}")
        except Exception as e:
            print(f"Error sending webhook: {e}")

    def _send_no_snow_webhook(self, url: str, resort_forecasts: Dict[SkiResort, List[WeatherForecast]] = None):
        """Send confirmation webhook when no snow detected"""
        message_lines = ['✅ *Powdertime Check Complete*', '']
        
        # Add forecast summary if available
        if resort_forecasts:
            message_lines.append('*Forecast Summary:*')
            for resort, forecasts in resort_forecasts.items():
                total_snow = sum(f.snowfall_inches for f in forecasts)
                message_lines.append(f'  • {resort.name}: {total_snow:.1f}" total')
            message_lines.append('')
        
        message_lines.append('No significant snowfall forecasted at monitored resorts.')
        
        payload = {
            'text': '\n'.join(message_lines)
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            print(f"✅ Status check webhook sent to {url}")
        except Exception as e:
            print(f"Error sending webhook: {e}")


class NotificationManager:
    """Manages notifications based on configuration"""
    
    SERVICES = {
        'console': ConsoleNotification,
        'email': EmailNotification,
        'webhook': WebhookNotification,
    }
    
    def __init__(self, notification_config: Dict[str, Any]):
        """
        Initialize notification manager
        
        Args:
            notification_config: Notification configuration from config file
        """
        self.config = notification_config
        method = notification_config.get('method', 'console')
        
        service_class = self.SERVICES.get(method)
        if not service_class:
            print(f"Warning: Unknown notification method '{method}', using console")
            service_class = ConsoleNotification
        
        self.service = service_class()
    
    def notify(self, events: List[SnowEvent], always_notify: bool = False, 
               resort_forecasts: Dict[SkiResort, List[WeatherForecast]] = None):
        """Send notification about snow events"""
        self.service.send(events, self.config, always_notify=always_notify, 
                         resort_forecasts=resort_forecasts)
