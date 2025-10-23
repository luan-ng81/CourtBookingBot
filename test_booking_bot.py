"""
Unit tests for Court Booking Bot
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from court_booking import CourtBooker


class TestCourtBooker(unittest.TestCase):
    """Test suite for CourtBooker class"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.booker = CourtBooker()

    def tearDown(self):
        """Clean up after each test method"""
        self.booker = None

    def test_initialization(self):
        """Test that CourtBooker initializes with correct attributes"""
        self.assertIsNotNone(self.booker.username)
        self.assertIsNotNone(self.booker.password)
        self.assertIsNotNone(self.booker.login_url)
        self.assertEqual(self.booker.zip_code, '94085')
        self.assertEqual(self.booker.duration, '120')

    def test_calculate_booking_date_format(self):
        """Test that booking date is formatted correctly (no leading zeros)"""
        booking_date = self.booker.calculate_booking_date()

        # Should not start with 0
        self.assertNotEqual(booking_date[0], '0')

        # Should contain exactly 2 slashes
        self.assertEqual(booking_date.count('/'), 2)

        # Should match pattern M/D/YYYY or MM/DD/YYYY
        parts = booking_date.split('/')
        self.assertEqual(len(parts), 3)
        self.assertTrue(1 <= int(parts[0]) <= 12)  # Month
        self.assertTrue(1 <= int(parts[1]) <= 31)  # Day
        self.assertEqual(len(parts[2]), 4)  # Year

    def test_calculate_booking_date_advance_days(self):
        """Test that booking date is calculated correctly based on advance days"""
        expected_date = datetime.now() + timedelta(days=self.booker.booking_ahead_days)
        calculated_date = self.booker.calculate_booking_date()

        # Parse the calculated date
        parts = calculated_date.split('/')
        calculated_datetime = datetime(
            year=int(parts[2]),
            month=int(parts[0]),
            day=int(parts[1])
        )

        # Should match expected date (day precision)
        self.assertEqual(calculated_datetime.date(), expected_date.date())

    def test_calculate_booking_date_removes_leading_zeros(self):
        """Test that leading zeros are removed from month and day"""
        # Test with mocked date that would have leading zeros
        with patch('court_booking.booker.datetime') as mock_datetime:
            # Mock January 5th (would be 01/05/YYYY)
            mock_now = datetime(2025, 1, 1)
            mock_datetime.now.return_value = mock_now

            # If booking ahead is 4 days, result should be 1/5/2025
            self.booker.booking_ahead_days = 4
            booking_date = self.booker.calculate_booking_date()

            # Should not have leading zeros
            self.assertFalse(booking_date.startswith('0'))
            month_day = booking_date.split('/')[1]
            self.assertFalse(month_day.startswith('0'))

    @patch('court_booking.booker.sync_playwright')
    def test_login_called_with_correct_credentials(self, mock_playwright):
        """Test that login method uses correct credentials"""
        # Set up mocks
        mock_page = MagicMock()
        mock_context = MagicMock()
        mock_browser = MagicMock()
        mock_p = MagicMock()

        mock_p.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_page.is_visible.return_value = True
        mock_playwright.return_value.__enter__.return_value = mock_p

        # Run booking
        self.booker.book_court()

        # Verify login credentials were used
        mock_page.fill.assert_any_call('#txtUser', self.booker.username)
        mock_page.fill.assert_any_call('#txtPassword', self.booker.password)

    @patch('court_booking.booker.sync_playwright')
    def test_book_court_success(self, mock_playwright):
        """Test successful booking flow"""
        # Set up mocks
        mock_page = MagicMock()
        mock_context = MagicMock()
        mock_browser = MagicMock()
        mock_p = MagicMock()

        mock_p.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_page.is_visible.return_value = True  # Success message visible
        mock_playwright.return_value.__enter__.return_value = mock_p

        # Run booking
        success, message = self.booker.book_court()

        # Assert success
        self.assertTrue(success)
        self.assertEqual(message, "Booking successful")

        # Verify browser was closed
        mock_browser.close.assert_called_once()

    @patch('court_booking.booker.sync_playwright')
    def test_book_court_failure(self, mock_playwright):
        """Test failed booking flow"""
        # Set up mocks
        mock_page = MagicMock()
        mock_context = MagicMock()
        mock_browser = MagicMock()
        mock_p = MagicMock()

        mock_p.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_page.is_visible.return_value = False  # Success message NOT visible
        mock_playwright.return_value.__enter__.return_value = mock_p

        # Run booking
        success, message = self.booker.book_court()

        # Assert failure
        self.assertFalse(success)
        self.assertEqual(message, "Booking failed - slot may be taken")

    @patch('court_booking.booker.sync_playwright')
    def test_book_court_exception_handling(self, mock_playwright):
        """Test that exceptions are properly handled"""
        # Set up mocks to raise exception
        mock_page = MagicMock()
        mock_context = MagicMock()
        mock_browser = MagicMock()
        mock_p = MagicMock()

        mock_p.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_page.goto.side_effect = Exception("Network error")
        mock_playwright.return_value.__enter__.return_value = mock_p

        # Run booking
        success, message = self.booker.book_court()

        # Assert failure with error message
        self.assertFalse(success)
        self.assertIn("Network error", message)

        # Verify screenshot was attempted
        mock_page.screenshot.assert_called_once()

    @patch('court_booking.booker.sync_playwright')
    def test_browser_closes_on_exception(self, mock_playwright):
        """Test that browser closes even when exception occurs"""
        # Set up mocks
        mock_page = MagicMock()
        mock_context = MagicMock()
        mock_browser = MagicMock()
        mock_p = MagicMock()

        mock_p.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_page.goto.side_effect = Exception("Test error")
        mock_playwright.return_value.__enter__.return_value = mock_p

        # Run booking
        self.booker.book_court()

        # Verify browser was closed despite exception
        mock_browser.close.assert_called_once()

    @patch('court_booking.booker.time.sleep')
    @patch.object(CourtBooker, 'book_court')
    def test_run_with_retry_success_first_attempt(self, mock_book_court, mock_sleep):
        """Test retry logic with success on first attempt"""
        mock_book_court.return_value = (True, "Booking successful")

        self.booker.run_with_retry(max_retries=3, retry_delay=1)

        # Should only call once
        self.assertEqual(mock_book_court.call_count, 1)
        # Should not sleep
        mock_sleep.assert_not_called()

    @patch('court_booking.booker.time.sleep')
    @patch.object(CourtBooker, 'book_court')
    def test_run_with_retry_success_second_attempt(self, mock_book_court, mock_sleep):
        """Test retry logic with success on second attempt"""
        mock_book_court.side_effect = [
            (False, "Failed"),
            (True, "Booking successful")
        ]

        self.booker.run_with_retry(max_retries=3, retry_delay=1)

        # Should call twice
        self.assertEqual(mock_book_court.call_count, 2)
        # Should sleep once
        self.assertEqual(mock_sleep.call_count, 1)
        mock_sleep.assert_called_with(1)

    @patch('court_booking.booker.time.sleep')
    @patch.object(CourtBooker, 'book_court')
    def test_run_with_retry_all_attempts_fail(self, mock_book_court, mock_sleep):
        """Test retry logic when all attempts fail"""
        mock_book_court.return_value = (False, "Failed")

        self.booker.run_with_retry(max_retries=3, retry_delay=1)

        # Should call 3 times
        self.assertEqual(mock_book_court.call_count, 3)
        # Should sleep 2 times (not after last attempt)
        self.assertEqual(mock_sleep.call_count, 2)

    def test_private_methods_exist(self):
        """Test that all private methods are defined"""
        self.assertTrue(hasattr(self.booker, '_login'))
        self.assertTrue(hasattr(self.booker, '_navigate_to_reservations'))
        self.assertTrue(hasattr(self.booker, '_select_club'))
        self.assertTrue(hasattr(self.booker, '_set_booking_details'))
        self.assertTrue(hasattr(self.booker, '_submit_reservation'))
        self.assertTrue(hasattr(self.booker, '_take_error_screenshot'))


class TestCourtBookerIntegration(unittest.TestCase):
    """Integration tests for CourtBooker"""

    def test_full_initialization_with_config(self):
        """Test that CourtBooker properly loads all config values"""
        booker = CourtBooker()

        # Verify all attributes are set
        self.assertIsInstance(booker.username, str)
        self.assertIsInstance(booker.password, str)
        self.assertIsInstance(booker.login_url, str)
        self.assertIsInstance(booker.zip_code, str)
        self.assertIsInstance(booker.club_name, str)
        self.assertIsInstance(booker.preferred_time, str)
        self.assertIsInstance(booker.duration, str)
        self.assertIsInstance(booker.booking_ahead_days, int)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
