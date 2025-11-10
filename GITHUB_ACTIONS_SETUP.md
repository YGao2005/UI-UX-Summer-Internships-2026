# GitHub Actions Setup Guide

This guide helps you configure GitHub Actions to automatically run the job scraper daily at 4pm UTC.

## Current Status

✅ **Workflow configured**: Runs daily at 4pm UTC (noon EST, 9am PST)
✅ **Branch configured**: Pushes to `master` branch
✅ **Auto-commit enabled**: Commits README.md and data/jobs.json when jobs are updated

## Schedule

The workflow runs automatically:
- **Daily**: 4:00 PM UTC
- **Manual trigger**: Can be triggered from GitHub Actions tab
- **On push**: Runs when you push to master branch (for testing)

## Workflow Features

When the workflow runs, it will:
1. Install Python 3.11 and all dependencies
2. Run all 11 job scrapers (including JobSpy, Hacker News, RSS feeds)
3. Filter and deduplicate results
4. Update README.md and data/jobs.json if new jobs are found
5. Commit changes with job count (e.g., "Update job listings - 92 internships")
6. Display summary with total internships found

## Optional: GitHub Secrets (for more results)

The workflow works **without any secrets**, but you'll get **30-40% more jobs** if you add these optional API keys.

### Without API Keys
- **Sources**: 8 scrapers (Greenhouse, Lever, Ashby, RemoteOK, JobSpy, Hacker News, Y Combinator, RSS)
- **Expected results**: 60-80 internships

### With API Keys
- **Sources**: 11 scrapers (adds The Muse, Adzuna, Jooble)
- **Expected results**: 90-120+ internships

### How to Add GitHub Secrets

1. **Go to your repository settings**:
   - Navigate to `https://github.com/YGao2005/UI-UX-Summer-Internships-2026/settings/secrets/actions`
   - Or: Settings → Secrets and variables → Actions → New repository secret

2. **Add each API key as a separate secret**:

#### The Muse API Key
- **Secret name**: `THEMUSE_API_KEY`
- **Get key**: https://www.themuse.com/developers/api/v2
- **Tier**: Free (3,600 requests/hour)

#### Adzuna API (2 secrets)
- **Secret name 1**: `ADZUNA_APP_ID`
- **Secret name 2**: `ADZUNA_APP_KEY`
- **Get keys**: https://developer.adzuna.com/
- **Tier**: Free (1,000 calls/month)

#### Jooble API Key
- **Secret name**: `JOOBLE_API_KEY`
- **Get key**: https://jooble.org/api/about
- **Tier**: Free (check documentation for limits)

### Example: Adding a Secret

```
1. Click "New repository secret"
2. Name: THEMUSE_API_KEY
3. Value: paste your actual API key here
4. Click "Add secret"
```

## Troubleshooting

### Workflow ran but README wasn't updated

**Possible causes**:
1. **No new jobs found** - The workflow only commits if jobs changed
2. **API keys missing** - Some scrapers may have failed silently
3. **Rate limits** - API calls may have been throttled

**Solution**: Check the workflow logs:
1. Go to the "Actions" tab in your repository
2. Click on the latest "Update Job Listings" run
3. Look for errors in the "Run scraper" step
4. Common issues:
   - Missing API keys (not critical - scraper continues without them)
   - Network timeouts (temporary - will work on next run)
   - Rate limits (wait for next scheduled run)

### Manual trigger not working

**Solution**:
1. Go to "Actions" tab
2. Click "Update Job Listings" workflow
3. Click "Run workflow" button (top right)
4. Select "master" branch
5. Click "Run workflow"

### Want to change the schedule?

Edit `.github/workflows/update_jobs.yml`:

```yaml
schedule:
  - cron: '0 16 * * *'  # 4pm UTC
```

Cron format: `minute hour day month day-of-week`

Examples:
- `0 12 * * *` - Noon UTC daily
- `0 */6 * * *` - Every 6 hours
- `0 9 * * 1` - 9am UTC every Monday

## Viewing Workflow Results

After each run, you can see:
- **Job count**: In the commit message (e.g., "Update job listings - 92 internships")
- **Summary**: In the workflow summary (Actions tab → click run → Summary)
- **Logs**: Full scraper output with statistics per source

## Next Steps

1. ✅ Workflow is configured and ready
2. ⚠️ (Optional) Add API keys to GitHub Secrets for more results
3. ✅ Wait for first scheduled run at 4pm UTC, or trigger manually
4. ✅ Check that README.md and data/jobs.json are auto-updated

---

**Need help?** Check the workflow logs in the Actions tab or open an issue.
