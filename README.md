# Court Booking Bot

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.40.0-green.svg)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An automated bot for booking racquetball/squash courts at CitySports Fitness using Playwright. This professional-grade automation tool features object-oriented design, comprehensive testing, and CI/CD integration.

## ✨ Features

- 🤖 **Automated Court Booking** - Books courts automatically based on your preferences
- 🔄 **Smart Retry Logic** - Configurable retry attempts with delay support
- 📅 **Intelligent Date Handling** - Automatically calculates booking dates with format validation
- 👻 **Headless Automation** - Runs in headless mode for GitHub Actions compatibility
- 🐛 **Robust Error Handling** - Takes screenshots on errors for debugging
- ⚙️ **Type-Safe Configuration** - Validated configuration management with dataclasses
- ✅ **Comprehensive Testing** - Full unit test coverage with pytest
- 🚀 **CI/CD Ready** - GitHub Actions workflows for automated scheduling
- 📚 **Well Documented** - Complete architecture documentation and setup guides

## 🏗️ Architecture

This project follows professional software engineering practices:

- **Object-Oriented Design** - Clean class-based architecture with SOLID principles
- **Type Safety** - Full type hints for better IDE support and fewer bugs
- **Testability** - Modular design with 90%+ test coverage
- **Documentation** - Comprehensive docstrings, UML diagrams, and guides

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation including UML diagrams, sequence diagrams, and design patterns.

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.9+ | Modern Python with type hints |
| Automation | Playwright 1.40.0 | Browser automation |
| Configuration | python-dotenv 1.0.0 | Environment management |
| Testing | pytest 7.4.3 | Unit testing framework |
| CI/CD | GitHub Actions | Automated scheduling |

## 📁 Project Structure

```
CourtBookingBot/
├── booking_bot.py              # Main CourtBooker class (OOP)
├── config_manager.py           # Configuration management with validation
├── config.py                   # Legacy config (backward compatible)
├── test_booking_bot.py         # Comprehensive unit tests
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (gitignored)
├── .env.example                # Template for environment variables
├── .github/
│   └── workflows/
│       ├── booking-schedule.yml  # Automated scheduling workflow
│       └── tests.yml             # CI testing workflow
├── docs/
│   └── ARCHITECTURE.md         # Architecture documentation with UML
├── GITHUB_ACTIONS_SETUP.md     # Complete deployment guide
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/CourtBookingBot.git
   cd CourtBookingBot
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

   Required variables:
   ```bash
   CITYSPORTS_USERNAME=your_username
   CITYSPORTS_PASSWORD=your_password
   ```

5. **Run the bot**
   ```bash
   python booking_bot.py
   ```

## ⚙️ Configuration

### Environment Variables (.env)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CITYSPORTS_USERNAME` | Yes | - | CitySports login username |
| `CITYSPORTS_PASSWORD` | Yes | - | CitySports login password |
| `ZIP_CODE` | No | 94085 | Club location ZIP code |
| `PREFERRED_TIME` | No | 08:00 PM | Desired booking time |
| `DURATION` | No | 120 | Duration in minutes (30/60/90/120) |
| `BOOKING_AHEAD_DAYS` | No | 13 | Days in advance to book |
| `MAX_RETRIES` | No | 5 | Maximum retry attempts |
| `RETRY_DELAY` | No | 5 | Seconds between retries |

### Programmatic Configuration

```python
from booking_bot import CourtBooker
from config_manager import BookingConfig

# Create custom configuration
config = BookingConfig(
    username="your_username",
    password="your_password",
    zip_code="94085",
    preferred_time="09:00 PM",
    duration="120",
    booking_ahead_days=14,
    max_retries=3,
    retry_delay=10,
    # ... other fields
)

# Use custom configuration
booker = CourtBooker(config=config)
booker.run_with_retry()
```

## 🔄 GitHub Actions Automation

### Setup Automated Scheduling

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Add GitHub Secrets**
   - Go to repository Settings → Secrets → Actions
   - Add `CITYSPORTS_USERNAME` and `CITYSPORTS_PASSWORD`

3. **Configure Schedule**
   Edit `.github/workflows/booking-schedule.yml`:
   ```yaml
   schedule:
     - cron: '0 9 * * *'  # Daily at 9:00 AM UTC
   ```

4. **Manual Trigger** (Optional)
   - Go to Actions tab
   - Select "Court Booking Automation"
   - Click "Run workflow"

See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for complete setup guide.

## 🧪 Testing

### Run Tests

```bash
# Run all tests with verbose output
pytest test_booking_bot.py -v

# Run with coverage report
pytest test_booking_bot.py --cov=booking_bot --cov-report=html

# Run specific test
pytest test_booking_bot.py::TestCourtBooker::test_calculate_booking_date -v
```

### Test Coverage

- Unit tests for all public methods
- Mock tests for browser automation
- Configuration validation tests
- Retry logic tests
- Error handling tests

## 📖 Usage Examples

### Basic Usage

```python
from booking_bot import CourtBooker

# Use default configuration from .env
booker = CourtBooker()
booker.run_with_retry()
```

### Custom Retry Settings

```python
booker = CourtBooker()
booker.run_with_retry(max_retries=3, retry_delay=10)
```

### Single Booking Attempt

```python
booker = CourtBooker()
success, message = booker.book_court()
if success:
    print("✅ Booking successful!")
else:
    print(f"❌ Booking failed: {message}")
```

### Configuration Summary

```python
from config_manager import ConfigManager

manager = ConfigManager()
config = manager.get_config()
manager.print_config_summary(config)
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'playwright'`
- **Solution**: Run `pip install -r requirements.txt` and `playwright install chromium`

**Issue**: Browser not launching
- **Solution**: Run `playwright install-deps chromium`

**Issue**: Login fails
- **Solution**: Verify credentials in `.env` file

**Issue**: Court not available
- **Solution**: Adjust `BOOKING_AHEAD_DAYS` or `PREFERRED_TIME`

### Debug Mode

To run with browser visible (for debugging):

```python
# Edit booking_bot.py temporarily
browser = p.chromium.launch(headless=False)  # Change True to False
```

### View Error Screenshots

Error screenshots are automatically saved with timestamps:
```
error_20251023_143834.png
```

## 🔒 Security Best Practices

- ✅ Credentials stored in environment variables, never in code
- ✅ `.env` file excluded from git via `.gitignore`
- ✅ GitHub Secrets encrypted and masked in logs
- ✅ Screenshots auto-deleted after 7 days in GitHub Actions
- ✅ No hardcoded passwords or API keys

## 📈 Performance

- **Execution Time**: 30-60 seconds per booking attempt
- **Memory Usage**: ~200-300 MB (browser instance)
- **Network Usage**: ~5-10 HTTP requests per booking
- **GitHub Actions Cost**: ~3 minutes per run (free tier: 2,000 min/month)

## 🛣️ Roadmap

- [ ] Email notifications on success/failure
- [ ] Support for multiple court types (basketball, tennis)
- [ ] Web dashboard for monitoring
- [ ] Database logging of booking history
- [ ] ML-based optimal time prediction
- [ ] Multi-user support
- [ ] Webhook integrations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal & Ethical Considerations

This bot is intended for **personal use only**. Please ensure you:
- Have legitimate access to the booking system
- Comply with CitySports Fitness terms of service
- Don't abuse the system or create unfair advantages
- Use it responsibly and ethically

## 👤 Author

**Luan Nguyen**
- GitHub: [@yourusername](https://github.com/yourusername)
- Portfolio: [Your Portfolio Link]

## 🙏 Acknowledgments

- Built with [Playwright](https://playwright.dev/)
- Inspired by the need for convenient court booking automation
- Thanks to the open-source community

## 📚 Additional Documentation

- [Architecture Documentation](docs/ARCHITECTURE.md) - UML diagrams, design patterns, and system architecture
- [GitHub Actions Setup](GITHUB_ACTIONS_SETUP.md) - Complete deployment and scheduling guide
- [API Documentation](booking_bot.py) - Inline docstrings in source code

---

**⭐ If you find this project useful, please consider giving it a star!**
