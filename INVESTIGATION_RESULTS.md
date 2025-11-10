# Investigation Results - Source Fixes & Improvements

**Date:** 2025-11-09
**Status:** ✅ Significant Improvements Made

---

## 🎯 Original Issues

1. Only finding 23 internships (expected 30-50+)
2. Only 2 sources working (Greenhouse + Ashby)
3. Jobs not sorted by date

## ✅ What We Fixed

### 1. Date Sorting ✓ FIXED
- **File:** `src/utils/markdown_generator.py` line 66
- **Change:** Now sorts by `posted_date` descending (newest first)
- **Result:** Most recent jobs appear at the top

### 2. Company Handle Corrections ✓ FIXED

**Greenhouse Companies - Added/Fixed:**
- ✅ DoorDash: Fixed handle `doordash` → `doordashusa`
- ✅ IDEO: Moved from Lever → Greenhouse (9 jobs)
- ✅ MongoDB: Moved from Lever → Greenhouse (363 jobs)
- ✅ Twitch: Moved from Lever → Greenhouse (60 jobs)
- ✅ SurveyMonkey: Moved from Lever → Greenhouse (37 jobs)
- ✅ Anthropic: Moved from Ashby → Greenhouse (283 jobs)

**Removed Invalid Companies:**
- Removed 15+ companies with custom ATS systems
- Including: Spotify, Netflix, Canva, Adobe, Microsoft, Apple, Google, Meta, etc.
- These companies don't have public APIs we can access

### 3. Environment Variable Support ✓ ADDED
- Added `python-dotenv` for local `.env` file support
- Created `.env.example` template
- The Muse and Adzuna now work locally with API keys

## 📊 Results Comparison

### Before Fixes:
```
Total Jobs Scraped: 4,360
├── Greenhouse: 3,613 jobs (many 404 errors)
├── Lever: 0 jobs (all 404s)
├── Ashby: 701 jobs
├── RemoteOK: 28 jobs (filtered out)
├── The Muse: 0 jobs
└── Adzuna: 18 jobs

Filtering: 4,360 → 27 relevant → 23 unique internships
```

### After Fixes:
```
Total Jobs Scraped: 5,659 (+1,299 jobs, +30%)
├── Greenhouse: 4,911 jobs ✓ (+1,298, FIXED)
├── Lever: 0 jobs (intentionally removed)
├── Ashby: 701 jobs ✓ (same)
├── RemoteOK: 28 jobs (filtered - not internships)
├── The Muse: 0 jobs (API working, no current listings)
└── Adzuna: 19 jobs ✓ (+1)

Filtering: 5,659 → 29 relevant → 24 unique internships
```

**Improvement:** +1,299 total jobs scraped, +1 additional unique internship

## 🔍 Current Source Status

### Working Sources (✓)

**Greenhouse (35 companies, 4,911 jobs):**
- Figma, Airbnb, Pinterest, Stripe, Dropbox
- DoorDash, Lyft, Coinbase, Discord, Reddit
- Roblox, Asana, Duolingo, Instacart, HubSpot
- Robinhood, Databricks, GitLab, Airtable, Grammarly
- Vercel, Webflow, IDEO, MongoDB, Twitch
- SurveyMonkey, Anthropic

**Ashby (4 companies, 701 jobs):**
- Notion, OpenAI, Ramp, Linear

**Adzuna (API key required, 19 jobs):**
- Working with API key

**The Muse (API key required, 0 jobs):**
- API working but no design internships currently posted

### Not Working Sources (✗)

**RemoteOK:**
- Finds 28 design jobs
- None are internships (all full-time remote)
- Getting filtered out correctly

**Scale AI (Ashby):**
- Jobs page exists but API doesn't return JSON
- Requires JavaScript or has different API structure
- **Action Needed:** Remove from companies.yml or investigate further

**Lever Companies:**
- Intentionally removed (all moved to other systems or custom ATS)

## 🎯 Remaining Opportunities

### 1. Scale AI Investigation
- Jobs page works: https://jobs.ashbyhq.com/scale
- API endpoint returns empty: https://api.ashbyhq.com/posting-api/job-board/scale
- May require: JavaScript rendering, different API endpoint, or authentication

### 2. RemoteOK Strategy
**Current:**
- Searches tag='design'
- Finds design jobs but they're not internships

**Options:**
- A) Keep current (correct - we only want internships)
- B) Try different tags: 'intern', 'entry-level', 'junior'
- C) Broaden keyword search in description

### 3. More Sources Needed
**Waiting for Gemini Deep Research to find:**
- University job platforms (Handshake, WayUp)
- Design-specific boards (Dribbble, Behance)
- Additional free APIs
- More Greenhouse/Ashby/Lever companies

## 📈 Performance Metrics

**API Call Efficiency:**
```
Source          Companies  Calls/Day  Jobs Found  Internships
─────────────────────────────────────────────────────────────
Greenhouse      35         35         4,911       ~18
Ashby           4          4          701         ~1
RemoteOK        N/A        1          28          0
The Muse        N/A        5          0           0
Adzuna          N/A        2          19          ~5
─────────────────────────────────────────────────────────────
TOTAL           39         47         5,659       24
```

**Rate Limit Status:**
- ✅ Greenhouse: No limits, all working
- ✅ Ashby: No limits, all working
- ✅ RemoteOK: No limits, reasonable use
- ✅ The Muse: 3,600/hour, using 5/day (0.14%)
- ✅ Adzuna: 1,000/month, using 60/month (6%)

## 🚀 Next Steps

### Immediate (While Gemini Researches):
1. ✅ Fixed all major company handles
2. ✅ Improved from 4,360 → 5,659 total jobs
3. ✅ Date sorting working
4. ✅ API keys integrated

### Awaiting Gemini Results:
1. New job APIs to integrate
2. Additional companies using Greenhouse/Ashby/Lever
3. Design-specific job boards
4. University/internship-focused platforms

### Future Improvements:
1. Add Workday scraper (Adobe, others use it)
2. Add SmartRecruiters scraper (Canva uses it)
3. Add iCIMS scraper (Atlassian uses it)
4. Gentle scraping of Y Combinator, AngelList

## 📝 Files Modified

1. `data/companies.yml` - Cleaned up and corrected
2. `src/utils/markdown_generator.py` - Date sorting fixed
3. `requirements.txt` - Added python-dotenv
4. `src/main.py` - Added .env loading
5. `.env.example` - Created template

## 🎉 Summary

**Success Metrics:**
- ✓ 30% increase in total jobs scraped
- ✓ All Greenhouse companies working correctly
- ✓ Date sorting implemented
- ✓ API key support added
- ✓ Removed non-functional sources

**Current Capacity:**
- Tracking 39 companies across 2 ATS platforms
- Scraping 5,659 jobs daily
- Finding 24 relevant UI/UX internships

**Next Goal:**
- Find 10-20 additional sources via Gemini research
- Target: 50-100 total internships daily

---

**Status:** Ready for additional sources from Gemini Deep Research
