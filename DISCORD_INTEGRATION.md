# Discord Bot Integration

This document explains how the internship scraper integrates with the Discord bot for automatic announcements and application tracking.

## Overview

The internship scraper now uploads all scraped internships to a Supabase database, which is monitored by a Discord bot that:
- Posts daily announcements of new internships
- Allows users to track applications with button clicks
- Provides statistics and search functionality

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions                           │
│  (Runs daily at 4pm UTC)                                    │
│                                                             │
│  1. Run src/main.py (scrape internships)                   │
│  2. Run src/supabase_uploader.py (upload to database)      │
│  3. Commit README.md + jobs.json (for git history)         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Supabase Database      │
         │  • intern_jobs          │◀────┐
         │  • intern_posted_jobs   │     │
         │  • intern_applications  │     │
         │  • intern_users         │     │
         └────────────┬───────────┘     │
                      │                 │
                      ▼                 │
         ┌────────────────────────┐    │
         │   Discord Bot           │    │
         │  (Heroku Worker Dyno)   │────┘
         │                         │
         │  • Checks hourly        │
         │  • Posts new jobs       │
         │  • Tracks applications  │
         └─────────────────────────┘
```

## Components

### 1. Supabase Uploader (`src/supabase_uploader.py`)

**Purpose:** Upload scraped jobs to Supabase database

**When:** Runs after `main.py` completes in GitHub Actions

**What it does:**
- Reads `data/jobs.json`
- Upserts jobs to `intern_jobs` table
- Prints statistics

**Usage:**
```bash
python src/supabase_uploader.py
```

**Environment Variables:**
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Service role key

### 2. Database Schema (`database/schema.sql`)

**Tables:**
- `intern_jobs` - All internship listings
- `intern_posted_jobs` - Tracks which jobs posted to Discord
- `intern_users` - Discord users
- `intern_applications` - User application tracking
- `intern_user_stats` (view) - Aggregated statistics

**Setup:**
See `database/README.md` for installation instructions.

### 3. GitHub Actions Workflow (`.github/workflows/update_jobs.yml`)

**Modified to:**
1. Run scraper (existing)
2. **NEW:** Upload jobs to Supabase
3. Commit changes (existing)

**New step:**
```yaml
- name: Upload jobs to Supabase
  run: python src/supabase_uploader.py
  env:
    SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
    SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
```

### 4. Discord Bot (`/Users/yang/class monitoring script/internship_bot.py`)

**Features:**
- Hourly check for new internships
- Posts rich embeds with job details
- Interactive buttons ("✅ Mark Applied")
- Slash commands: `/internships`, `/applied`, `/stats`, `/search`

**Hosted:** Heroku worker dyno (shared with class monitor bot)

## Setup Instructions

### Prerequisites
1. ✅ Supabase account (free tier)
2. ✅ Discord bot created and invited to server
3. ✅ GitHub repository with Actions enabled

### Step 1: Set Up Database

1. Open Supabase SQL Editor
2. Run `database/schema.sql`
3. Verify tables created:
   ```sql
   SELECT table_name FROM information_schema.tables
   WHERE table_schema = 'public' AND table_name LIKE 'intern_%';
   ```

### Step 2: Configure GitHub Secrets

1. Go to GitHub repo → Settings → Secrets → Actions
2. Add secrets:
   - `SUPABASE_URL` - From Supabase project settings
   - `SUPABASE_KEY` - Service role key (not anon key!)

### Step 3: Update Local .env

Add to `.env`:
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key_here
```

### Step 4: Test Upload

```bash
# Run scraper
python src/main.py

# Upload to Supabase
python src/supabase_uploader.py
```

### Step 5: Deploy Discord Bot

See `/Users/yang/class monitoring script/SETUP_GUIDE.md` for bot deployment.

## Data Flow

### Daily Scraping Cycle

**4:00 PM UTC** - GitHub Actions triggers

1. **Scraper runs** (`main.py`)
   - Scrapes 11 sources
   - Filters for UI/UX internships
   - Deduplicates results
   - Saves to `data/jobs.json`

2. **Uploader runs** (`supabase_uploader.py`)
   - Reads `jobs.json`
   - Upserts to Supabase `intern_jobs`
   - Prints statistics

3. **Git commit**
   - Commits `README.md` and `jobs.json`
   - Pushes to GitHub

### Hourly Bot Cycle

**Every hour** - Discord bot checks

1. **Query new jobs**
   - Fetches jobs from `intern_jobs`
   - Filters out already posted (checks `intern_posted_jobs`)

2. **Post announcements**
   - Creates rich embeds for each job
   - Adds "✅ Mark Applied" button
   - Posts to configured Discord channel
   - Records message ID in `intern_posted_jobs`

3. **Handle interactions**
   - Users click "Mark Applied"
   - Bot records in `intern_applications`
   - User can view stats with `/stats`

## User Interactions

### Slash Commands

| Command | Description |
|---------|-------------|
| `/internships [limit]` | View recent internship postings |
| `/search <keyword>` | Search by company/role/location |
| `/applied` | View your application history |
| `/stats` | View your application statistics |

### Buttons

- **✅ Mark Applied** - Track that you applied to this job

### Statistics Tracked

- Total applications
- Applications this week/month
- Unique companies applied to
- Status breakdown (applied, interviewing, offer, rejected)
- Application timeline

## Maintenance

### Manual Upload

```bash
python src/supabase_uploader.py
```

### Check Database Stats

```sql
-- Total jobs
SELECT COUNT(*) FROM intern_jobs;

-- Jobs today
SELECT COUNT(*) FROM intern_jobs WHERE scraped_date = CURRENT_DATE;

-- Total applications
SELECT COUNT(*) FROM intern_applications;

-- User stats
SELECT * FROM intern_user_stats;
```

### Clean Old Data

```sql
-- Delete jobs older than 90 days with no applications
DELETE FROM intern_jobs
WHERE scraped_date < CURRENT_DATE - INTERVAL '90 days'
AND id NOT IN (SELECT DISTINCT job_id FROM intern_applications);
```

## Troubleshooting

### Upload Fails in GitHub Actions

1. Check GitHub Secrets are set correctly
2. Verify Supabase project is not paused
3. Check logs in Actions tab
4. Ensure service role key (not anon key)

### Bot Not Posting New Jobs

1. Verify jobs uploaded to Supabase: `SELECT * FROM intern_jobs ORDER BY scraped_date DESC LIMIT 10`
2. Check `INTERNSHIP_CHANNEL_ID` is set in bot environment
3. Verify bot has permissions in Discord channel
4. Check bot logs: `heroku logs --tail | grep Internship`

### Duplicate Job Postings

- Bot tracks posted jobs in `intern_posted_jobs`
- If database is cleared, bot will repost old jobs
- Solution: Don't clear `intern_posted_jobs` table

## Cost

| Service | Usage | Cost |
|---------|-------|------|
| Supabase | ~100 jobs/day, 4 tables | Free tier |
| GitHub Actions | 1 run/day, ~2 min | Free (public repo) |
| Storage | jobs.json ~200KB | Free (included in GitHub) |

**Total: $0/month**

## Future Enhancements

Potential improvements:
- [ ] Email notifications for new jobs matching criteria
- [ ] Resume/cover letter tracking per application
- [ ] Interview scheduling reminders
- [ ] Application deadline tracking
- [ ] Success rate analytics
- [ ] Job recommendation engine

---

For Discord bot setup and deployment, see:
`/Users/yang/class monitoring script/SETUP_GUIDE.md`
