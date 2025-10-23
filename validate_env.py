#!/usr/bin/env python3
"""
Environment validation script for Court Booking Bot.
Checks that all required environment variables are set before running the bot.
"""

import os
import sys


def validate_environment():
    """Validate that all required environment variables are set."""

    required_vars = {
        'CITYSPORTS_USERNAME': 'CitySports login username',
        'CITYSPORTS_PASSWORD': 'CitySports login password',
        'EMAIL_TO': 'Recipient email address for notifications',
        'EMAIL_FROM': 'Sender email address',
        'EMAIL_PASSWORD': 'Email account password for sending notifications',
    }

    optional_vars = {
        'BOOKING_AHEAD_DAYS': 'Days ahead to book (default: 13)',
        'PREFERRED_TIME': 'Preferred booking time (default: 08:00 PM)',
    }

    print("=" * 60)
    print("Environment Variables Validation")
    print("=" * 60)
    print()

    missing_vars = []

    # Check required variables
    print("Checking required variables:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Show first 3 chars and mask the rest for security
            masked_value = value[:3] + '*' * (len(value) - 3) if len(value) > 3 else '***'
            print(f"  ✓ {var}: {masked_value} ({description})")
        else:
            print(f"  ✗ {var}: NOT SET ({description})")
            missing_vars.append(var)

    print()

    # Check optional variables
    print("Checking optional variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"  ✓ {var}: {value} ({description})")
        else:
            print(f"  ℹ {var}: Not set, will use default ({description})")

    print()
    print("=" * 60)

    # Report results
    if missing_vars:
        print(f"❌ VALIDATION FAILED: {len(missing_vars)} required variable(s) missing")
        print()
        print("Missing variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print()
        print("Please set these environment variables or GitHub Secrets.")
        print("=" * 60)
        return False
    else:
        print("✅ VALIDATION PASSED: All required variables are set")
        print("=" * 60)
        return True


if __name__ == "__main__":
    success = validate_environment()
    sys.exit(0 if success else 1)
