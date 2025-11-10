# API Setup Complete

## Changes Made

### 1. GitHub Actions Workflow Updated
- ✅ Uncommented `ADZUNA_APP_ID` and `ADZUNA_APP_KEY`
- ✅ Added `THEMUSE_API_KEY` environment variable
- File: `.github/workflows/update_jobs.yml`

### 2. New Scrapers Added

#### The Muse Scraper
- **File**: `src/scrapers/themuse_scraper.py`
- **API Key**: `THEMUSE_API_KEY` (from GitHub Secrets)
- **Free Tier**: 3,600 requests/hour
- **Features**:
  - Explicit internship category filter
  - Best for design internships
  - Fetches up to 100 jobs (5 pages)

#### Adzuna Scraper
- **File**: `src/scrapers/adzuna_scraper.py`
- **API Keys**: `ADZUNA_APP_ID` + `ADZUNA_APP_KEY` (from GitHub Secrets)
- **Free Tier**: 1,000 calls/month (≈33/day)
- **Features**:
  - Broad coverage across multiple job boards
  - Fetches up to 100 jobs (2 pages) per run
  - Includes salary data when available

### 3. Main Script Updated
- **File**: `src/main.py`
- Added imports for new scrapers
- Initialized The Muse and Adzuna scrapers
- Updated scraping pipeline to include 6 sources (was 4)
  - [1/6] Greenhouse
  - [2/6] Lever
  - [3/6] Ashby
  - [4/6] RemoteOK
  - [5/6] **The Muse** (NEW)
  - [6/6] **Adzuna** (NEW)

### 4. Documentation Updated
- **File**: `src/utils/markdown_generator.py`
- Updated README footer to mention all 6 data sources
- Added descriptions for The Muse and Adzuna

## Current Data Sources

| Source | Auth Required | Rate Limit | Status |
|--------|---------------|------------|--------|
| Greenhouse | ❌ No | Unlimited | ✅ Working |
| Lever | ❌ No | Unlimited | ⚠️ Needs handle fixes |
| Ashby | ❌ No | Unlimited | ✅ Working |
| RemoteOK | ❌ No | Reasonable use | ✅ Working |
| The Muse | ✅ API Key | 3,600/hour | ✅ Ready |
| Adzuna | ✅ App ID + Key | 1,000/month | ✅ Ready |

## Next Steps

### 1. Test Locally (Optional)

If you want to test The Muse and Adzuna locally:

```bash
# Set environment variables
export THEMUSE_API_KEY="your-key-here"
export ADZUNA_APP_ID="your-app-id"
export ADZUNA_APP_KEY="your-app-key"

# Run scraper
python src/main.py
```

**Expected results:**
- The Muse: ~20-50 design internships
- Adzuna: ~50-100 UI/UX internship listings
- Total: Should find significantly more internships than before

### 2. Push to GitHub

```bash
git add .
git commit -m "Add The Muse and Adzuna API scrapers"
git push origin main
```

### 3. Verify Secrets Are Set

Make sure you've added these in GitHub:
- Repository → Settings → Secrets and variables → Actions
- ✅ `THEMUSE_API_KEY`
- ✅ `ADZUNA_APP_ID`
- ✅ `ADZUNA_APP_KEY`

### 4. Test GitHub Action

1. Go to Actions tab
2. Click "Update Job Listings"
3. Click "Run workflow"
4. Watch the logs to see all 6 sources scraping

**Expected output:**
```
[1/6] Scraping Greenhouse... ✓ Found 3000+ jobs
[2/6] Scraping Lever... (may find 0 if handles need fixing)
[3/6] Scraping Ashby... ✓ Found 700+ jobs
[4/6] Scraping RemoteOK... ✓ Found 20-30 design jobs
[5/6] Scraping The Muse... ✓ Found 20-50 design internships
[6/6] Scraping Adzuna... ✓ Found 50-100 jobs
```

## API Key Management

### Security Notes
- ✅ API keys are stored as GitHub Secrets (encrypted)
- ✅ Never committed to repository
- ✅ Only accessible to GitHub Actions
- ✅ Can be rotated anytime in Settings

### Rate Limit Monitoring

**The Muse:**
- 3,600 requests/hour = plenty for daily runs
- Current usage: ~5 requests/day (1 per category page)
- **No concerns**

**Adzuna:**
- 1,000 calls/month ≈ 33/day
- Current usage: 2 calls/day (2 pages per run)
- Running daily: 2 × 30 = 60 calls/month
- **Well within limits** ✅

### If Rate Limits Are Hit

**The Muse:**
- Reduce `max_pages` in `themuse_scraper.py` (line 47)
- Currently: 5 pages = 100 jobs (plenty)

**Adzuna:**
- Reduce `max_pages` in `adzuna_scraper.py` (line 51)
- Currently: 2 pages = 100 jobs
- Can reduce to 1 page = 50 jobs if needed

## Performance Expectations

**Before (4 sources):**
- ~4,300 total jobs scraped
- ~7-10 relevant UI/UX internships

**After (6 sources):**
- ~5,000+ total jobs scraped
- **~30-50 relevant UI/UX internships** (expected)
- Better coverage of:
  - Smaller companies (The Muse)
  - International positions (Adzuna)
  - Explicit internship categories

## Troubleshooting

### "The Muse: Skipping (no API key)"
- Check GitHub Secrets: `THEMUSE_API_KEY` is set correctly
- Verify no typos in secret name
- Try running manually with "Run workflow" button

### "Adzuna: Skipping (no API credentials)"
- Check both secrets are set:
  - `ADZUNA_APP_ID`
  - `ADZUNA_APP_KEY`
- Both must be present for Adzuna to work

### API Errors (403/401)
- API key may be invalid or expired
- Check your API dashboard:
  - The Muse: https://www.themuse.com/developers
  - Adzuna: https://developer.adzuna.com/
- Regenerate keys if needed

## Cost

Still **$0/month**! All APIs are on free tiers.

---

**Status: READY TO DEPLOY** 🚀

Once you push to GitHub and the workflow runs, you'll have a comprehensive UI/UX internship tracker pulling from 6 different sources!
