# Database Setup Guide

## Supabase Schema Installation

This directory contains the SQL schema for the internship tracker Discord bot integration.

### Installation Steps

1. **Open Supabase SQL Editor**
   - Go to your Supabase project dashboard
   - Navigate to the SQL Editor (left sidebar)

2. **Run the Schema**
   - Copy the contents of `schema.sql`
   - Paste into the SQL Editor
   - Click "Run" to execute

3. **Verify Tables Created**
   ```sql
   SELECT table_name
   FROM information_schema.tables
   WHERE table_schema = 'public'
   AND table_name LIKE 'intern_%';
   ```

   You should see:
   - `intern_jobs`
   - `intern_posted_jobs`
   - `intern_users`
   - `intern_applications`

### Database Structure

#### Tables

**intern_jobs**
- Stores all internship listings from the scraper
- Primary key: `id` (from scraper, e.g., "jobspy_glassdoor_123")
- Tracks job details, relevance score, and metadata

**intern_posted_jobs**
- Tracks which jobs have been announced in Discord
- Prevents duplicate announcements
- Links to Discord message IDs for reference

**intern_users**
- Stores Discord user information
- Created automatically when user first interacts with bot

**intern_applications**
- Tracks user applications and their status
- Supports status: applied, interviewing, offer, rejected, withdrawn
- One application per user per job (enforced by unique constraint)

#### Views

**intern_user_stats**
- Aggregated statistics per user
- Used by `/stats` slash command
- Automatically computed from applications data

### Testing the Schema

After installation, test with sample data:

```sql
-- Insert a test job
INSERT INTO intern_jobs (id, title, company, location, url, scraped_date, relevance_score)
VALUES ('test_001', 'UI/UX Design Intern', 'Figma', 'Remote', 'https://figma.com/careers', CURRENT_DATE, 15);

-- Insert a test user
INSERT INTO intern_users (discord_id, username)
VALUES ('123456789', 'testuser');

-- Insert a test application
INSERT INTO intern_applications (user_discord_id, job_id, status)
VALUES ('123456789', 'test_001', 'applied');

-- Query user stats
SELECT * FROM intern_user_stats WHERE discord_id = '123456789';

-- Cleanup test data
DELETE FROM intern_applications WHERE user_discord_id = '123456789';
DELETE FROM intern_users WHERE discord_id = '123456789';
DELETE FROM intern_jobs WHERE id = 'test_001';
```

### Row-Level Security (RLS)

**Note:** This schema does not enable RLS by default since the Discord bot will use the service role key. If you want to enable RLS for additional security:

```sql
ALTER TABLE intern_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE intern_applications ENABLE ROW LEVEL SECURITY;

-- Users can only see their own applications
CREATE POLICY "Users can view own applications" ON intern_applications
    FOR SELECT USING (user_discord_id = auth.uid()::text);

CREATE POLICY "Users can insert own applications" ON intern_applications
    FOR INSERT WITH CHECK (user_discord_id = auth.uid()::text);
```

### Maintenance

**Clean up old jobs (optional):**
```sql
-- Delete jobs older than 90 days that have no applications
DELETE FROM intern_jobs
WHERE scraped_date < CURRENT_DATE - INTERVAL '90 days'
AND id NOT IN (SELECT DISTINCT job_id FROM intern_applications);
```
