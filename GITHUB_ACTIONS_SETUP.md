# GitHub Actions Setup Guide

This guide will help you set up automated court booking using GitHub Actions.

## Prerequisites

1. GitHub account
2. Repository pushed to GitHub
3. CitySports account credentials

## Step-by-Step Setup

### 1. Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Court booking automation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/CourtBookingBot.git
git push -u origin main
```

### 2. Add GitHub Secrets

Go to your repository on GitHub:

1. Click **Settings** tab
2. Click **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add the following secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `CITYSPORTS_USERNAME` | Your username | CitySports login username |
| `CITYSPORTS_PASSWORD` | Your password | CitySports login password |
| `EMAIL_TO` | your@email.com | Notification recipient (optional) |
| `EMAIL_FROM` | your@email.com | Notification sender (optional) |
| `EMAIL_PASSWORD` | App password | Gmail app password (optional) |

**IMPORTANT**: Never commit these values to your repository!

### 3. Configure Schedule

Edit `.github/workflows/booking-schedule.yml`:

```yaml
schedule:
  - cron: '1 0 * * *'  # Daily at 12:01 AM UTC
```

#### Cron Syntax Explained

```
  ┌───────────── minute (0 - 59)
  │ ┌───────────── hour (0 - 23)
  │ │ ┌───────────── day of month (1 - 31)
  │ │ │ ┌───────────── month (1 - 12)
  │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday = 0)
  │ │ │ │ │
  * * * * *
```

#### Example Schedules

```yaml
# Every day at 9:00 AM UTC
- cron: '0 9 * * *'

# Every Monday at 8:00 AM UTC
- cron: '0 8 * * 1'

# Every day at 6:00 AM and 6:00 PM UTC
- cron: '0 6,18 * * *'

# First day of every month at midnight UTC
- cron: '0 0 1 * *'
```

#### Convert Your Timezone to UTC

If your local time is PST (UTC-8):
- 8:00 AM PST = 4:00 PM UTC (16:00)
- Use: `'0 16 * * *'`

If your local time is EST (UTC-5):
- 8:00 AM EST = 1:00 PM UTC (13:00)
- Use: `'0 13 * * *'`

Use [crontab.guru](https://crontab.guru/) for help with cron expressions.

### 4. Test Manual Trigger

1. Go to **Actions** tab in your repository
2. Click **Court Booking Automation** workflow
3. Click **Run workflow** button
4. (Optional) Override settings:
   - Booking ahead days: `14`
   - Preferred time: `09:00 PM`
5. Click **Run workflow**

### 5. Monitor Workflow Runs

#### View Logs
1. Go to **Actions** tab
2. Click on a workflow run
3. Click on the job name
4. Expand steps to see detailed logs

#### Download Error Screenshots
If booking fails:
1. Go to failed workflow run
2. Scroll to bottom of page
3. Download **error-screenshots** artifact

### 6. Disable/Enable Automation

#### Temporarily Disable
1. Go to **Actions** tab
2. Click **Court Booking Automation**
3. Click **⋮** (three dots)
4. Click **Disable workflow**

#### Re-enable
1. Follow same steps
2. Click **Enable workflow**

## Workflow Features

### Automatic Retry
- Retries up to 5 times (configurable in `config.py`)
- 5-second delay between retries

### Error Handling
- Takes screenshots on failure
- Uploads screenshots as artifacts
- Logs detailed error messages

### Manual Override
Run with custom settings without changing code:
- Override booking ahead days
- Override preferred time

## Troubleshooting

### Workflow Not Running

**Check schedule syntax**
```yaml
# ❌ Wrong
schedule:
  cron: '0 9 * * *'

# ✅ Correct
schedule:
  - cron: '0 9 * * *'
```

**Check if workflow is disabled**
- Go to Actions tab and verify workflow is enabled

### Login Fails

1. Verify secrets are set correctly
2. Check if credentials work on the website
3. Review workflow logs for specific error

### Court Not Available

- Check if `BOOKING_AHEAD_DAYS` matches club policy
- Verify `PREFERRED_TIME` is valid
- Consider adding multiple time options

### Workflow Quota Exceeded

GitHub Actions free tier includes:
- 2,000 minutes/month for private repos
- Unlimited for public repos

Each run takes ~2-5 minutes.

## Advanced Configuration

### Multiple Booking Times

Create separate workflow files:

`.github/workflows/morning-booking.yml`:
```yaml
schedule:
  - cron: '0 8 * * *'
env:
  PREFERRED_TIME: '08:00 AM'
```

`.github/workflows/evening-booking.yml`:
```yaml
schedule:
  - cron: '0 20 * * *'
env:
  PREFERRED_TIME: '08:00 PM'
```

### Email Notifications (Future)

Add notification steps to workflow:
```yaml
- name: Send success email
  if: success()
  # Add email notification logic here
```

## Security Best Practices

1. ✅ Always use GitHub Secrets for credentials
2. ✅ Never commit `.env` file
3. ✅ Enable branch protection on main
4. ✅ Use least privilege access
5. ✅ Regularly rotate passwords
6. ✅ Review workflow run logs for sensitive data

## Cost Considerations

GitHub Actions is free for:
- **Public repositories**: Unlimited minutes
- **Private repositories**: 2,000 minutes/month

Estimated usage:
- ~3 minutes per run
- Running daily = ~90 minutes/month
- Well within free tier!

## Support

If you encounter issues:
1. Check workflow logs in Actions tab
2. Review error screenshots
3. Verify secrets are configured
4. Test manually with `python booking_bot.py`

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Cron Expression Generator](https://crontab.guru/)
- [Playwright Documentation](https://playwright.dev/)
