# Discord Notification Setup Guide

This guide will help you set up Discord notifications for your internship tracker bot.

## Features

Your Discord bot now sends:

1. **Daily Reminders** - Sent every time the scraper runs, regardless of new jobs
   - Mentions @everyone to notify all server members
   - Shows total internships available in the database
   - Shows number of jobs **posted today by companies** (based on `posted_date` field in Supabase)
   - Motivational message to keep applying!
   - Color changes: Blue embed when new jobs are posted, Orange when no new jobs

2. **Error Notifications** - If the scraper encounters errors
   - Sends error details to Discord
   - Helps you stay informed about scraper health

## Setup Instructions

### 1. Create a Discord Webhook

1. Open your Discord server
2. Go to **Server Settings** → **Integrations** → **Webhooks**
3. Click **New Webhook** (or **Create Webhook**)
4. Give it a name (e.g., "Internship Tracker")
5. Choose the channel where you want notifications (e.g., #internships)
6. Click **Copy Webhook URL**

### 2. Configure Your Local Environment

1. Open the `.env` file in your project root
2. Find the line `DISCORD_WEBHOOK_URL=`
3. Paste your webhook URL after the equals sign:
   ```
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/123456789/abcdefg...
   ```
4. Save the file

### 3. Configure GitHub Actions (for automated daily runs)

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `DISCORD_WEBHOOK_URL`
5. Value: Paste your Discord webhook URL
6. Click **Add secret**

## Testing

Test your Discord notifications locally:

```bash
# Set your webhook URL in .env first
python3 -c "
from src.utils.discord_notifier import DiscordNotifier
notifier = DiscordNotifier()
notifier.send_daily_reminder(total_jobs=92, jobs_today=5)
"
```

Or run the full scraper:

```bash
python3 src/main.py
```

At the end of the run, you should see a Discord notification in your chosen channel!

## Message Examples

### When New Jobs Are Posted Today
```
@everyone Daily Internship Reminder

5 internships posted today by companies!

Remember to check and apply to today's fresh opportunities!

┌─────────────────────────────────┐
│ Internship Tracker Statistics  │
│         (Blue embed)            │
├─────────────────────────────────┤
│ 📊 Total Available: 92          │
│ 🆕 Posted Today: 5 new          │
└─────────────────────────────────┘
```

### When No New Jobs Are Posted Today
```
@everyone Daily Internship Reminder

No new internships posted by companies today, but keep applying to existing opportunities!

Stay consistent and keep pushing!

┌─────────────────────────────────┐
│ Internship Tracker Statistics  │
│        (Orange embed)           │
├─────────────────────────────────┤
│ 📊 Total Available: 92          │
│ 🆕 Posted Today: None today     │
└─────────────────────────────────┘
```

**Note:** "Posted Today" refers to internships that companies posted today (based on the `posted_date` field), not jobs that were scraped today. This gives you the most relevant, fresh opportunities!

## Customization

You can customize the notification behavior by editing `src/utils/discord_notifier.py`:

- Change the message text
- Modify the embed colors
- Add more fields to the statistics
- Change the @everyone mention to a specific role

## Troubleshooting

**No notifications received?**
- Check that your webhook URL is correct in `.env`
- Make sure the bot has permission to post in the channel
- Check the logs for any error messages

**Rate limiting?**
- Discord webhooks have rate limits (5 requests per 2 seconds)
- The current implementation sends 1 notification per run, so this shouldn't be an issue

**Want to disable notifications temporarily?**
- Comment out the `DISCORD_WEBHOOK_URL` line in `.env`:
  ```
  # DISCORD_WEBHOOK_URL=https://...
  ```
- The scraper will still run but skip Discord notifications

## Future Enhancements

Possible improvements you could add:

- Track "new jobs today" by comparing with previous runs
- Send different notifications based on time of day
- Notify only when specific companies post jobs
- Add reaction buttons for users to mark jobs as applied
- Send weekly summary reports

Enjoy your automated internship notifications!
