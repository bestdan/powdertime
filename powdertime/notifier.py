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


class NotificationService:
    """Base notification service"""
    
    def send(self, events: List[SnowEvent], config: Dict[str, Any]):
        """
        Send notification about snow events
        
        Args:
            events: List of SnowEvent objects
            config: Notification configuration
        """
        raise NotImplementedError


class ConsoleNotification(NotificationService):
    """Console notification - prints to stdout"""
    
    def send(self, events: List[SnowEvent], config: Dict[str, Any]):
        """Print snow events to console"""
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
    
    def send(self, events: List[SnowEvent], config: Dict[str, Any]):
        """Send snow events via email"""
        if not events:
            return
        
        email_config = config.get('email', {})
        smtp_server = email_config.get('smtp_server')
        smtp_port = email_config.get('smtp_port', 587)
        from_email = email_config.get('from_email')
        to_email = email_config.get('to_email')
        password = email_config.get('password')
        
        if not all([smtp_server, from_email, to_email, password]):
            print("Error: Email configuration incomplete")
            return
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = f"❄️ Powder Alert! {len(events)} Resort(s) with Significant Snow"
        
        # Create body
        body = "Significant snowfall forecasted at the following resort(s):\n\n"
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


class WebhookNotification(NotificationService):
    """Webhook notification - POST to URL"""
    
    def send(self, events: List[SnowEvent], config: Dict[str, Any]):
        """Send snow events to webhook"""
        if not events:
            return
        
        webhook_config = config.get('webhook', {})
        url = webhook_config.get('url')
        
        if not url:
            print("Error: Webhook URL not configured")
            return
        
        # Prepare payload
        payload = {
            'alert_type': 'powder_alert',
            'event_count': len(events),
            'events': [
                {
                    'resort_name': event.resort.name,
                    'resort_state': event.resort.state,
                    'total_snowfall_inches': event.total_snowfall,
                    'max_daily_snowfall_inches': event.max_daily_snowfall,
                    'start_date': event.start_date.isoformat() if event.start_date else None,
                    'end_date': event.end_date.isoformat() if event.end_date else None,
                }
                for event in events
            ]
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            print(f"✅ Webhook notification sent to {url}")
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
    
    def notify(self, events: List[SnowEvent]):
        """Send notification about snow events"""
        self.service.send(events, self.config)
