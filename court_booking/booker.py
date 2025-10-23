"""
Court Booker Module - Handles automated court booking logic
"""

from playwright.sync_api import sync_playwright, Page, Browser
import time
from datetime import datetime, timedelta
from typing import Tuple, Optional
from config_manager import BookingConfig, load_config


class CourtBooker:
    """
    Handles automated court booking for CitySports Fitness.

    Attributes:
        config (BookingConfig): Configuration object containing all settings
        username (str): CitySports login username
        password (str): CitySports login password
        login_url (str): URL for CitySports login page
        zip_code (str): ZIP code for club location
        club_name (str): Club selector identifier
        preferred_time (str): Preferred booking time
        duration (str): Court booking duration in minutes
        booking_ahead_days (int): Days in advance to book
    """

    def __init__(self, config: Optional[BookingConfig] = None):
        """
        Initialize the CourtBooker with configuration.

        Args:
            config (Optional[BookingConfig]): Configuration object. If None, loads from environment.
        """
        self.config = config if config else load_config()

        # Set instance variables for easy access
        self.username = self.config.username
        self.password = self.config.password
        self.login_url = self.config.login_url
        self.zip_code = self.config.zip_code
        self.club_name = self.config.club_name
        self.preferred_time = self.config.preferred_time
        self.duration = self.config.duration
        self.booking_ahead_days = self.config.booking_ahead_days

    def calculate_booking_date(self) -> str:
        """
        Calculate the booking date based on advance booking days.
        Formats the date to match the website's expected format (M/D/YYYY).

        Returns:
            str: Formatted date string without leading zeros
        """
        today = datetime.now()
        booking_date = today + timedelta(days=self.booking_ahead_days)
        date_string = booking_date.strftime("%m/%d/%Y")

        # Remove leading zeros from month
        if date_string[0] == '0':
            date_string = date_string[1:]

        # Remove leading zeros from day
        slash_index = date_string.find("/") + 1
        if date_string[slash_index] == '0':
            date_string = date_string[:slash_index] + date_string[slash_index + 1:]

        return date_string

    def _login(self, page: Page) -> None:
        """
        Perform login to CitySports website.

        Args:
            page (Page): Playwright page object
        """
        page.goto(self.login_url, wait_until='networkidle')
        print("✓ Loaded login page")

        page.wait_for_selector('#txtUser', state='visible')
        page.fill('#txtUser', self.username)
        page.fill('#txtPassword', self.password)
        page.click('#ctl00_MainContent_Login1_btnLogin')
        page.wait_for_load_state('networkidle')
        print("✓ Logged in successfully")

    def _navigate_to_reservations(self, page: Page) -> None:
        """
        Navigate to Racquetball/Squash reservation page.

        Args:
            page (Page): Playwright page object
        """
        page.click('text=Reservations')
        page.click('text=Racquetball/Squash')
        print("✓ Navigated to court reservations")

    def _select_club(self, page: Page) -> None:
        """
        Select the club by ZIP code.

        Args:
            page (Page): Playwright page object
        """
        page.click('#btnChangeClub')
        page.fill('#txtZipCode', self.zip_code)
        page.click('#btnFindclub')
        page.wait_for_timeout(2000)

        page.click(f'input[name="{self.club_name}"][id="arySelClub"]')
        print("✓ Selected club: SUNNYVALE - E. ARQUES AVE.")
        page.wait_for_timeout(3000)

    def _set_booking_details(self, page: Page) -> None:
        """
        Set date, time, and duration for the booking.

        Args:
            page (Page): Playwright page object
        """
        booking_date = self.calculate_booking_date()
        page.select_option('#ddlDates', booking_date)
        print(f"✓ Selected date: {booking_date}")

        page.select_option('#ddlDuration', self.duration)
        page.select_option('#cboSearByTimeList', self.preferred_time)
        print(f"✓ Selected time: {self.preferred_time} for {self.duration} minutes")

    def _submit_reservation(self, page: Page) -> bool:
        """
        Submit the reservation and verify success.

        Args:
            page (Page): Playwright page object

        Returns:
            bool: True if booking successful, False otherwise
        """
        page.click('#btnSaveReservation')
        page.wait_for_timeout(3000)

        if page.is_visible('text=Your reservation has been saved'):
            print("✅ SUCCESS! Court booked successfully!")
            return True
        else:
            print("❌ FAILED: Court may not be available")
            return False

    def _take_error_screenshot(self, page: Page) -> None:
        """
        Take a screenshot for debugging purposes.

        Args:
            page (Page): Playwright page object
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f'error_{timestamp}.png'
        page.screenshot(path=screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")

    def book_court(self) -> Tuple[bool, str]:
        """
        Main booking function that orchestrates the entire booking process.

        Returns:
            Tuple[bool, str]: (Success status, Message)
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            page = context.new_page()

            try:
                print(f"[{datetime.now()}] Starting court booking process...")

                self._login(page)
                self._navigate_to_reservations(page)
                self._select_club(page)
                self._set_booking_details(page)

                if self._submit_reservation(page):
                    return True, "Booking successful"
                else:
                    return False, "Booking failed - slot may be taken"

            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
                self._take_error_screenshot(page)
                return False, str(e)

            finally:
                browser.close()

    def run_with_retry(self, max_retries: Optional[int] = None,
                       retry_delay: Optional[int] = None) -> None:
        """
        Execute booking with retry logic.

        Args:
            max_retries (Optional[int]): Maximum number of retry attempts. Uses config default if None.
            retry_delay (Optional[int]): Seconds to wait between retries. Uses config default if None.
        """
        max_retries = max_retries if max_retries is not None else self.config.max_retries
        retry_delay = retry_delay if retry_delay is not None else self.config.retry_delay

        for attempt in range(1, max_retries + 1):
            print(f"\n{'='*50}")
            print(f"Attempt {attempt} of {max_retries}")
            print(f"{'='*50}")

            success, message = self.book_court()

            if success:
                print("\n🎉 Booking completed successfully!")
                # TODO: Send success email notification
                break
            else:
                if attempt < max_retries:
                    print(f"\n⏳ Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"\n❌ All {max_retries} attempts failed.")
                    # TODO: Send failure email notification
