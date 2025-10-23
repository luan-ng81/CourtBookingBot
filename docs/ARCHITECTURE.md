# Court Booking Bot - Architecture Documentation

## System Overview

The Court Booking Bot is a Python-based automation system that books racquetball/squash courts at CitySports Fitness. It uses Playwright for browser automation and follows object-oriented design principles.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions (CI/CD)                   │
│  ┌────────────┐         ┌────────────┐                      │
│  │  Schedule  │────────▶│  Workflow  │                      │
│  │   (Cron)   │         │   Runner   │                      │
│  └────────────┘         └──────┬─────┘                      │
└─────────────────────────────────┼───────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   Court Booking Bot System                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    main() Entry Point                 │  │
│  └───────────────────────────┬──────────────────────────┘  │
│                              │                              │
│                              ▼                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              ConfigManager                            │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  - Load .env variables                         │  │  │
│  │  │  - Validate configuration                      │  │  │
│  │  │  - Create BookingConfig object                 │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └───────────────────────────┬──────────────────────────┘  │
│                              │                              │
│                              ▼                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              CourtBooker Class                        │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  Public Methods:                               │  │  │
│  │  │    - __init__(config)                          │  │  │
│  │  │    - calculate_booking_date()                  │  │  │
│  │  │    - book_court()                              │  │  │
│  │  │    - run_with_retry()                          │  │  │
│  │  │                                                │  │  │
│  │  │  Private Methods:                              │  │  │
│  │  │    - _login(page)                              │  │  │
│  │  │    - _navigate_to_reservations(page)           │  │  │
│  │  │    - _select_club(page)                        │  │  │
│  │  │    - _set_booking_details(page)                │  │  │
│  │  │    - _submit_reservation(page)                 │  │  │
│  │  │    - _take_error_screenshot(page)              │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └───────────────────────────┬──────────────────────────┘  │
│                              │                              │
│                              ▼                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Playwright Browser                       │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  - Launch Chromium                             │  │  │
│  │  │  - Create context with user agent              │  │  │
│  │  │  - Execute page interactions                   │  │  │
│  │  │  - Capture screenshots                         │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └───────────────────────────┬──────────────────────────┘  │
│                              │                              │
└──────────────────────────────┼──────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  CitySports Website  │
                    │  (Target System)     │
                    └──────────────────────┘
```

## Class Diagram (UML)

```
╔════════════════════════════════════════════════════════════╗
║                      BookingConfig                         ║
╠════════════════════════════════════════════════════════════╣
║ + username: str                                            ║
║ + password: str                                            ║
║ + email_to: str                                            ║
║ + email_from: str                                          ║
║ + email_password: str                                      ║
║ + zip_code: str                                            ║
║ + club_name: str                                           ║
║ + login_url: str                                           ║
║ + preferred_day: str                                       ║
║ + preferred_time: str                                      ║
║ + duration: str                                            ║
║ + booking_ahead_days: int                                  ║
║ + max_retries: int                                         ║
║ + retry_delay: int                                         ║
╠════════════════════════════════════════════════════════════╣
║ + __post_init__(): None                                    ║
║ - _validate(): None                                        ║
╚════════════════════════════════════════════════════════════╝
                           △
                           │ uses
                           │
╔════════════════════════════════════════════════════════════╗
║                      ConfigManager                         ║
╠════════════════════════════════════════════════════════════╣
║ - env_file: Optional[str]                                  ║
╠════════════════════════════════════════════════════════════╣
║ + __init__(env_file: Optional[str]): None                  ║
║ + get_config() -> BookingConfig: static                    ║
║ + get_env_variable(key, default) -> str: static            ║
║ + print_config_summary(config: BookingConfig): None        ║
╚════════════════════════════════════════════════════════════╝
                           △
                           │ creates
                           │
╔════════════════════════════════════════════════════════════╗
║                       CourtBooker                          ║
╠════════════════════════════════════════════════════════════╣
║ + config: BookingConfig                                    ║
║ + username: str                                            ║
║ + password: str                                            ║
║ + login_url: str                                           ║
║ + zip_code: str                                            ║
║ + club_name: str                                           ║
║ + preferred_time: str                                      ║
║ + duration: str                                            ║
║ + booking_ahead_days: int                                  ║
╠════════════════════════════════════════════════════════════╣
║ + __init__(config: Optional[BookingConfig]): None          ║
║ + calculate_booking_date() -> str                          ║
║ + book_court() -> Tuple[bool, str]                         ║
║ + run_with_retry(max_retries, retry_delay): None           ║
║ - _login(page: Page): None                                 ║
║ - _navigate_to_reservations(page: Page): None              ║
║ - _select_club(page: Page): None                           ║
║ - _set_booking_details(page: Page): None                   ║
║ - _submit_reservation(page: Page) -> bool                  ║
║ - _take_error_screenshot(page: Page): None                 ║
╚════════════════════════════════════════════════════════════╝
```

## Sequence Diagram

```
User/GitHub Actions    CourtBooker         ConfigManager       Playwright      CitySports
       │                    │                    │                 │               │
       │  run_with_retry()  │                    │                 │               │
       ├───────────────────▶│                    │                 │               │
       │                    │   get_config()     │                 │               │
       │                    ├───────────────────▶│                 │               │
       │                    │◀───────────────────┤                 │               │
       │                    │  BookingConfig     │                 │               │
       │                    │                    │                 │               │
       │                    │  book_court()      │                 │               │
       │                    ├────────────────────┼────────────────▶│               │
       │                    │                    │  launch browser │               │
       │                    │                    │                 │               │
       │                    │  _login(page)      │                 │               │
       │                    ├────────────────────┼─────────────────┼──────────────▶│
       │                    │                    │                 │  authenticate │
       │                    │◀───────────────────┼─────────────────┼───────────────┤
       │                    │                    │                 │               │
       │                    │  _navigate_to_reservations(page)     │               │
       │                    ├────────────────────┼─────────────────┼──────────────▶│
       │                    │◀───────────────────┼─────────────────┼───────────────┤
       │                    │                    │                 │               │
       │                    │  _select_club(page)                  │               │
       │                    ├────────────────────┼─────────────────┼──────────────▶│
       │                    │◀───────────────────┼─────────────────┼───────────────┤
       │                    │                    │                 │               │
       │                    │  _set_booking_details(page)          │               │
       │                    ├────────────────────┼─────────────────┼──────────────▶│
       │                    │◀───────────────────┼─────────────────┼───────────────┤
       │                    │                    │                 │               │
       │                    │  _submit_reservation(page)           │               │
       │                    ├────────────────────┼─────────────────┼──────────────▶│
       │                    │◀───────────────────┼─────────────────┼───────────────┤
       │                    │    success/fail    │                 │   confirmation│
       │                    │                    │                 │               │
       │◀───────────────────┤                    │                 │               │
       │   (True, "Success")│                    │                 │               │
```

## Component Description

### 1. ConfigManager
**Responsibility**: Configuration management and validation

**Key Features**:
- Loads environment variables from `.env` file
- Validates configuration values
- Provides default values for optional settings
- Creates immutable `BookingConfig` data objects

**Dependencies**: `python-dotenv`

### 2. BookingConfig (Data Class)
**Responsibility**: Store validated configuration

**Key Features**:
- Immutable configuration container
- Built-in validation on initialization
- Type hints for all fields
- Clear separation of concerns (credentials, booking settings, retry logic)

### 3. CourtBooker
**Responsibility**: Core booking automation logic

**Key Features**:
- Browser automation orchestration
- Step-by-step booking workflow
- Error handling and retry logic
- Screenshot capture for debugging

**Design Patterns**:
- **Template Method**: `book_court()` orchestrates private methods
- **Dependency Injection**: Accepts `BookingConfig` in constructor
- **Single Responsibility**: Each method handles one specific task

**Dependencies**: `playwright`

### 4. Playwright Integration
**Responsibility**: Browser automation

**Key Features**:
- Headless browser execution
- Page interaction (clicking, typing, selecting)
- Wait strategies for dynamic content
- Screenshot capture

## Data Flow

1. **Initialization**
   ```
   Environment Variables → ConfigManager → BookingConfig → CourtBooker
   ```

2. **Booking Process**
   ```
   CourtBooker.run_with_retry()
     ↓
   CourtBooker.book_court()
     ↓
   Playwright Browser
     ↓
   CitySports Website
     ↓
   Success/Failure Response
   ```

3. **Error Handling**
   ```
   Exception Caught
     ↓
   Screenshot Captured
     ↓
   Return (False, error_message)
     ↓
   Retry Logic (if attempts remaining)
   ```

## Design Principles Applied

### 1. **Single Responsibility Principle (SRP)**
- Each class has one clear purpose
- Each method does one thing well

### 2. **Open/Closed Principle (OCP)**
- Easy to extend with new booking strategies
- Configuration changes don't require code changes

### 3. **Dependency Inversion Principle (DIP)**
- CourtBooker depends on BookingConfig abstraction
- Easy to mock for testing

### 4. **Don't Repeat Yourself (DRY)**
- Configuration logic centralized
- Reusable private methods

### 5. **Separation of Concerns**
- Configuration (ConfigManager)
- Business Logic (CourtBooker)
- Automation (Playwright)
- Testing (test_booking_bot.py)

## Testing Strategy

### Unit Tests
- Test individual methods in isolation
- Mock external dependencies (Playwright, browser)
- Verify configuration validation
- Test date calculation logic

### Integration Tests
- Test full workflow with mock browser
- Verify configuration loading
- Test retry logic

### Manual Testing
- Run locally with `python booking_bot.py`
- Verify against actual website
- Test error scenarios

## Deployment Strategy

### Local Execution
```bash
python booking_bot.py
```

### GitHub Actions (Scheduled)
- Runs on schedule (cron)
- Uses GitHub Secrets for credentials
- Uploads error screenshots as artifacts
- Provides manual trigger option

## Security Considerations

1. **Credentials**: Stored in environment variables, never in code
2. **GitHub Secrets**: Encrypted at rest, masked in logs
3. **Screenshots**: May contain sensitive data, automatically deleted after 7 days
4. **Browser**: Runs in isolated container

## Performance Characteristics

- **Execution Time**: 30-60 seconds per booking attempt
- **Memory Usage**: ~200-300 MB (browser instance)
- **Network**: ~5-10 HTTP requests per booking
- **Retry Overhead**: 5 seconds between attempts

## Future Enhancements

1. **Email Notifications**: Send alerts on success/failure
2. **Multiple Court Types**: Support basketball, tennis, etc.
3. **Web UI**: Dashboard for configuration and monitoring
4. **Database Logging**: Track booking history
5. **ML Optimization**: Learn best booking times
6. **Multi-user Support**: Book for multiple accounts
7. **Webhook Integration**: Notify external systems

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.9+ |
| Browser Automation | Playwright | 1.40.0 |
| Configuration | python-dotenv | 1.0.0 |
| Testing | pytest | 7.4.3 |
| CI/CD | GitHub Actions | Latest |
| Type Checking | Type Hints | Python 3.5+ |

## File Structure

```
CourtBookingBot/
├── booking_bot.py           # Main CourtBooker class
├── config_manager.py        # Configuration management
├── config.py                # Legacy config (backward compatible)
├── test_booking_bot.py      # Unit tests
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (gitignored)
├── .env.example             # Template for .env
├── .github/
│   └── workflows/
│       ├── booking-schedule.yml  # Scheduled booking
│       └── tests.yml             # CI tests
├── docs/
│   └── ARCHITECTURE.md      # This file
├── GITHUB_ACTIONS_SETUP.md  # Deployment guide
├── LICENSE                  # MIT License
└── README.md                # Project documentation
```

## Conclusion

This architecture provides a solid foundation for automated court booking while maintaining:
- ✅ Clean code principles
- ✅ Testability
- ✅ Maintainability
- ✅ Scalability
- ✅ Security
- ✅ Documentation

The system is production-ready and suitable for portfolio demonstration.
