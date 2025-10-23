import os
from dotenv import load_dotenv

load_dotenv()

# Credentials (will use GitHub Secrets in production)
USERNAME = os.getenv('CITYSPORTS_USERNAME', '')
PASSWORD = os.getenv('CITYSPORTS_PASSWORD', '')
EMAIL_TO = os.getenv('EMAIL_TO', '')
EMAIL_FROM = os.getenv('EMAIL_FROM', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')

# Booking Configuration
ZIP_CODE = '94085'
CLUB_NAME = 'ctl00$MainContent$gvClub$ctl02$arySelClub' #SUNNYVALE - E. ARQUES AVE.
LOGIN_URL = 'https://www.citysportsfitness.com/Pages/login.aspx'

# Booking Preferences
PREFERRED_DAY = 'Monday'  # Day of week to book
PREFERRED_TIME = '08:00 PM'  # 8:00 PM in 12hr format
DURATION = '120'           # Minutes: 30, 60, 90, or 120
BOOKING_AHEAD_DAYS = 13    # Days in advance to book

# Retry Configuration
MAX_RETRIES = 5
RETRY_DELAY = 5  # seconds between retries