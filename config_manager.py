"""
Configuration Manager - Centralized configuration handling for Court Booking Bot
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class BookingConfig:
    """
    Data class for booking configuration settings.

    Attributes:
        username (str): CitySports username
        password (str): CitySports password
        email_to (str): Recipient email for notifications
        email_from (str): Sender email for notifications
        email_password (str): Email account password
        zip_code (str): Club location ZIP code
        club_name (str): Club selector identifier
        login_url (str): CitySports login URL
        preferred_day (str): Preferred day of week for booking
        preferred_time (str): Preferred booking time
        duration (str): Court booking duration in minutes
        booking_ahead_days (int): Days in advance to book
        max_retries (int): Maximum retry attempts
        retry_delay (int): Seconds between retries
    """

    # Credentials
    username: str
    password: str
    email_to: str
    email_from: str
    email_password: str

    # Booking Configuration
    zip_code: str
    club_name: str
    login_url: str

    # Booking Preferences
    preferred_day: str
    preferred_time: str
    duration: str
    booking_ahead_days: int

    # Retry Configuration
    max_retries: int
    retry_delay: int

    def __post_init__(self):
        """Validate configuration after initialization"""
        self._validate()

    def _validate(self) -> None:
        """Validate configuration values"""
        # Validate required fields are not empty
        if not self.username or not self.password:
            raise ValueError("Username and password are required")

        if not self.login_url:
            raise ValueError("Login URL is required")

        # Validate numeric values
        if self.booking_ahead_days < 0:
            raise ValueError("Booking ahead days must be positive")

        if self.max_retries < 1:
            raise ValueError("Max retries must be at least 1")

        if self.retry_delay < 0:
            raise ValueError("Retry delay must be non-negative")

        # Validate duration
        valid_durations = ['30', '60', '90', '120']
        if self.duration not in valid_durations:
            raise ValueError(f"Duration must be one of {valid_durations}")


class ConfigManager:
    """
    Manages application configuration from environment variables and defaults.
    """

    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize ConfigManager and load environment variables.

        Args:
            env_file (Optional[str]): Path to .env file. Defaults to .env in current directory.
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

    @staticmethod
    def get_config() -> BookingConfig:
        """
        Load configuration from environment variables with fallback defaults.

        Returns:
            BookingConfig: Configuration object

        Raises:
            ValueError: If required configuration is missing or invalid
        """
        return BookingConfig(
            # Credentials (required from environment)
            username=os.getenv('CITYSPORTS_USERNAME', ''),
            password=os.getenv('CITYSPORTS_PASSWORD', ''),
            email_to=os.getenv('EMAIL_TO', ''),
            email_from=os.getenv('EMAIL_FROM', ''),
            email_password=os.getenv('EMAIL_PASSWORD', ''),

            # Booking Configuration (with defaults)
            zip_code=os.getenv('ZIP_CODE', '94085'),
            club_name=os.getenv(
                'CLUB_NAME',
                'ctl00$MainContent$gvClub$ctl02$arySelClub'
            ),
            login_url=os.getenv(
                'LOGIN_URL',
                'https://www.citysportsfitness.com/Pages/login.aspx'
            ),

            # Booking Preferences (with defaults)
            preferred_day=os.getenv('PREFERRED_DAY', 'Monday'),
            preferred_time=os.getenv('PREFERRED_TIME', '08:00 PM'),
            duration=os.getenv('DURATION', '120'),
            booking_ahead_days=int(os.getenv('BOOKING_AHEAD_DAYS', '13')),

            # Retry Configuration (with defaults)
            max_retries=int(os.getenv('MAX_RETRIES', '5')),
            retry_delay=int(os.getenv('RETRY_DELAY', '5'))
        )

    @staticmethod
    def get_env_variable(key: str, default: Optional[str] = None) -> str:
        """
        Get a specific environment variable.

        Args:
            key (str): Environment variable key
            default (Optional[str]): Default value if key not found

        Returns:
            str: Environment variable value

        Raises:
            KeyError: If key not found and no default provided
        """
        value = os.getenv(key, default)
        if value is None:
            raise KeyError(f"Environment variable '{key}' not found and no default provided")
        return value

    def print_config_summary(self, config: BookingConfig) -> None:
        """
        Print a summary of the current configuration (excluding sensitive data).

        Args:
            config (BookingConfig): Configuration object to summarize
        """
        print("\n" + "="*50)
        print("CONFIGURATION SUMMARY")
        print("="*50)
        print(f"Username: {config.username[:3]}***")
        print(f"ZIP Code: {config.zip_code}")
        print(f"Preferred Day: {config.preferred_day}")
        print(f"Preferred Time: {config.preferred_time}")
        print(f"Duration: {config.duration} minutes")
        print(f"Booking Ahead: {config.booking_ahead_days} days")
        print(f"Max Retries: {config.max_retries}")
        print(f"Retry Delay: {config.retry_delay} seconds")
        print("="*50 + "\n")


# Convenience function for backward compatibility
def load_config() -> BookingConfig:
    """
    Load configuration with default settings.

    Returns:
        BookingConfig: Loaded configuration object
    """
    manager = ConfigManager()
    return manager.get_config()


if __name__ == "__main__":
    # Example usage and testing
    try:
        manager = ConfigManager()
        config = manager.get_config()
        manager.print_config_summary(config)
        print("✅ Configuration loaded successfully!")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
