"""
Court Booking Bot - Automated court reservation system for CitySports Fitness

Main entry point for the booking bot application.
"""

from court_booking import CourtBooker


def main():
    """Main entry point for the booking bot."""
    booker = CourtBooker()
    booker.run_with_retry()


if __name__ == "__main__":
    main()