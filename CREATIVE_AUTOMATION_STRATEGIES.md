# Creative Automation Strategies for Finding More UI/UX Internships

**Investigation Date:** 2025-11-10
**Your Current Results:** 24 UI/UX design internships from 39 companies
**Goal:** 50-150+ internships via fully automated, hands-off approaches

---

## TL;DR - Quick Wins

**Implement these 5 things this week to potentially 2-3x your results:**

1. **Add JobSpy library** - Scrapes LinkedIn, Indeed, Glassdoor, ZipRecruiter (1-2 hours to integrate)
2. **Add Dribbble Jobs API** - Official API for design jobs (requires partner application)
3. **Scrape Hacker News "Who is Hiring"** - Open-source tools available (30 min to integrate)
4. **Add Workable scraper** - Many design companies use it (commercial tools available)
5. **Scrape JSON-LD structured data** from company career pages (2-3 days to build)

**Realistic expectations:** 50-80 internships with quick wins, 100-150+ with advanced implementations.

---

## Strategy Tiers: Quick → Medium → Advanced

### 🟢 Tier 1: Quick Wins (1-7 days implementation)

#### 1. JobSpy Library Integration ⭐ **HIGHEST IMPACT**

**What it is:**
- Open-source Python library that scrapes LinkedIn, Indeed, Glassdoor, Google Jobs, ZipRecruiter
- Returns structured job data (title, company, location, salary, description, posting date)
- Actively maintained (v1.1.79 released March 2025, 2.3k stars, 34 contributors)

**How it works:**
```python
from python_jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "glassdoor", "google", "zip_recruiter"],
    search_term="UI UX design intern",
    location="United States",
    distance=50,
    is_remote=True,
    job_type="internship",
    results_wanted=100
)
```

**Pros:**
- Works out of the box, minimal setup
- Scrapes 5 major job boards simultaneously
- Free and open-source (MIT license)
- Handles pagination, rate limiting (with proxies)
- Exports to CSV/Excel automatically

**Cons:**
- LinkedIn rate limits ~10 pages per IP (need proxy rotation)
- Indeed is least restrictive (no rate limits currently)
- May break if job boards change HTML structure
- Ethical/legal gray area (scraping vs. API)

**Expected results:** +30-50 internships

**Resources:**
- GitHub: https://github.com/speedyapply/JobSpy
- PyPI: `pip install python-jobspy`
- Tutorial: https://www.franciscomoretti.com/blog/automate-your-job-search

---

#### 2. Hacker News "Who is Hiring" Scraper

**What it is:**
- Monthly thread on Hacker News where companies post job openings
- Algolia API provides programmatic access
- Open-source parsers available to structure the data

**How it works:**
- Use Algolia search to find latest "Who is Hiring" thread
- Fetch comments via Hacker News API
- Parse unstructured text into structured job data
- Filter for design/UI/UX internships

**Existing tools:**
- GitHub: https://github.com/SamG06/Who-is-hiring-scraper (updates every 30 min)
- GitHub: https://github.com/gabfl/hn-whoishiring (FastAPI app with SQLite)
- Apify: https://apify.com/kutaui/hackernews-job-scraper (uses OpenAI to parse)
- HNHIRING.com: Pre-indexed 57,100 jobs going back to 2018

**Pros:**
- Startup-heavy (high-growth companies)
- Free, public API (news.ycombinator.com/api)
- Rich dataset (7+ years of history)
- No rate limiting on official API
- Many design/product roles

**Cons:**
- Only updates monthly
- Unstructured text format (requires parsing)
- May have 5-15 design internships per month (not hundreds)
- Startup-focused (may miss big tech companies)

**Expected results:** +5-15 internships per month

**Implementation time:** 2-4 hours (use existing open-source tools)

---

#### 3. Dribbble Jobs API ⭐ **DESIGN-SPECIFIC**

**What it is:**
- Official API for Dribbble job board (60k+ companies use Dribbble for hiring)
- 1.5k+ targeted clicks per job listing (highly engaged design audience)
- Jobs start at $299/30 days (indicates quality employers)

**API details:**
- Requires partner application (contact Dribbble)
- Endpoints: GET /jobs/:id, POST /jobs, PUT /jobs/:id
- Rate limit: 60 requests per period
- Returns: title, organization_name, location, category, role_type, description, apply URL

**Pros:**
- Design-focused job board (perfect for UI/UX)
- Official API (legal, stable, supported)
- High-quality employers (pay $299 for 30-day listing)
- Structured data (no scraping/parsing needed)

**Cons:**
- Requires partnership approval (not instant access)
- No search/filter endpoint documented (may need to fetch all jobs)
- Rate limited (60 requests/period)
- May not have many internships (mostly full-time design roles)

**Expected results:** +5-20 design internships (if approved for API access)

**Implementation time:** 1-2 hours (after API approval, which may take days/weeks)

**Action:** Apply for Dribbble API partnership at https://developer.dribbble.com/

---

#### 4. Remote Job Board RSS Feeds

**What it is:**
- Many remote job boards provide RSS/XML feeds
- Can be scraped/parsed automatically daily
- Focus on design/tech roles

**Available RSS feeds:**
- **We Work Remotely:** https://weworkremotely.com/remote-jobs.rss
- **Remotive:** https://remotive.com/remote-jobs/rss-feed
- **Himalayas:** https://himalayas.app/rss (requires attribution link)
- **Jobicy:** https://jobicy.com/jobs-rss-feed (API + RSS available)

**How it works:**
```python
import feedparser

feed = feedparser.parse('https://weworkremotely.com/remote-jobs.rss')
for entry in feed.entries:
    # Filter for design/UX/internship keywords
    if 'design' in entry.title.lower() or 'ux' in entry.title.lower():
        # Process job listing
```

**Pros:**
- Simple to implement (feedparser library)
- No rate limiting (RSS is meant for aggregation)
- Legal and encouraged by platforms
- Structured data (title, description, link, pubDate)
- Free

**Cons:**
- Not internship-specific (need heavy filtering)
- Many full-time remote roles (few internships)
- Lower volume for design roles specifically

**Expected results:** +3-10 remote design internships

**Implementation time:** 1-2 hours

---

#### 5. Add More Greenhouse/Ashby/Lever Companies

**What you're already doing well:**
- 35 Greenhouse companies, 4 Ashby companies
- Scraping 5,659 jobs total

**What you're missing:**
- There are 7,000+ companies using Greenhouse
- 1,000+ companies using Ashby
- 1,000+ companies using Lever

**How to find more:**
- Search for "design agency greenhouse careers" to find company handles
- Check competitor companies (if Figma uses Greenhouse, similar companies might too)
- Browse Greenhouse's customer showcase: https://www.greenhouse.com/customers
- Ashby customer page: https://www.ashbyhq.com/customers

**Design-forward companies to add:**
| Company | ATS | Handle |
|---------|-----|--------|
| Framer | Unknown | Research needed |
| Miro | Unknown | Research needed |
| Pitch | Ashby (likely) | Research needed |
| Coda | Greenhouse (likely) | Research needed |
| Retool | Greenhouse | retool |
| Canva | SmartRecruiters | (need scraper) |

**Expected results:** +10-20 internships by doubling your company list

**Implementation time:** 2-3 hours of research, 30 min to update companies.yml

---

### 🟡 Tier 2: Medium Effort (1-2 weeks implementation)

#### 6. Workable ATS Scraper ⭐ **HIGH IMPACT**

**What it is:**
- Workable is used by 27,000+ companies globally
- Many design agencies and mid-size tech companies use it
- Easier to scrape than Workday (simpler HTML structure)

**Commercial tools available:**
- Apify: https://apify.com/novus/workable-jobs-scraper (7-day free trial)
- Apify: https://apify.com/bytepulselabs/workable-job-scraper
- Fantastic.jobs: $200-4000/month for job feeds

**Open-source approach:**
- Workable job boards follow pattern: `company.workable.com`
- Jobs endpoint: `https://apply.workable.com/api/v3/accounts/{company}/jobs`
- Returns JSON (easy to parse)

**How to find Workable companies:**
```bash
# Google search: "site:workable.com design agency"
# Or check companies you know use Workable
```

**Example companies using Workable:**
- Many design agencies
- Mid-size tech startups
- European tech companies

**Pros:**
- Widely used (27,000+ companies)
- JSON API (no HTML parsing)
- No authentication required for public job listings
- Design agencies love Workable (affordable for smaller companies)

**Cons:**
- Need to build company list manually
- No central directory of all Workable companies
- Rate limiting may apply per company
- Requires some development work

**Expected results:** +20-40 internships (if you build a good company list)

**Implementation time:** 1 week (build scraper + research companies)

---

#### 7. JSON-LD Structured Data Scraper ⭐ **FUTURE-PROOF**

**What it is:**
- Many company career pages embed JobPosting structured data (schema.org)
- Google requires this for jobs to appear in Google for Jobs search results
- Standardized format makes scraping reliable

**How it works:**
```python
from bs4 import BeautifulSoup
import json

# Fetch career page
html = requests.get('https://company.com/careers').text
soup = BeautifulSoup(html, 'html.parser')

# Find JSON-LD script tags
for script in soup.find_all('script', type='application/ld+json'):
    data = json.loads(script.string)
    if data.get('@type') == 'JobPosting':
        # Extract job details
        title = data.get('title')
        company = data.get('hiringOrganization', {}).get('name')
        location = data.get('jobLocation', {}).get('address')
        # ... etc
```

**Which companies use this:**
- Any company wanting to appear in Google Jobs
- Increasingly common (Google encourages it)
- Custom ATS systems often generate this automatically

**Pros:**
- Standardized format (schema.org JobPosting)
- Works on custom career pages (Apple, Google, Microsoft, etc.)
- Future-proof (Google encourages adoption)
- Legal (scraping public structured data)
- Can access companies not using Greenhouse/Ashby/Lever

**Cons:**
- Need to know company career page URLs
- Not all companies use it (yet)
- Requires building company list
- Some technical development needed

**Expected results:** +30-50 internships (from companies you can't currently access)

**Implementation time:** 2-3 days (build scraper + test on 50-100 companies)

**Tutorial:** https://datawookie.dev/blog/2025/02/scraping-linked-ld-json-data/

---

#### 8. Google Jobs Scraper

**What it is:**
- Google aggregates jobs from across the web into Google for Jobs
- Can scrape Google's search results for "UI UX design intern"
- Bypasses need to scrape individual company sites

**Available tools:**
- ScraperAPI: https://www.scraperapi.com/solutions/structured-data/google-jobs-scraper/
- ScrapingBee: https://www.scrapingbee.com/scrapers/google-jobs-scraper-api/
- SerpAPI: https://serpapi.com/google-jobs-api (paid, $50-250/month)
- Apify: https://apify.com/orgupdate/google-jobs-scraper (7-day free trial)

**How it works:**
- Search Google for "UI UX design intern United States"
- Google aggregates from 1000s of sources automatically
- Scrape Google's structured results
- Handles anti-bot detection, CAPTCHA, IP rotation

**Pros:**
- Google already aggregates from everywhere
- One source = access to thousands of job boards
- Structured data (title, company, location, salary, description)
- Handles de-duplication for you

**Cons:**
- Commercial tools required (free trials available)
- Google actively blocks scrapers (need anti-bot services)
- Ethical/legal considerations
- $50-250/month for reliable access (SerpAPI)

**Expected results:** +50-100 internships (Google aggregates from everywhere)

**Implementation time:** 1-2 days (integrate commercial API)

---

#### 9. Built In Job Boards (City-Specific Tech Jobs)

**What it is:**
- Built In runs tech job boards for major cities
- Built In NYC, SF, Chicago, Austin, Boston, Seattle, LA, etc.
- Startup and scale-up focused

**Available boards:**
- https://www.builtinnyc.com/jobs
- https://www.builtinsf.com/jobs
- https://www.builtinchicago.org/jobs
- https://www.builtinaustin.com/jobs
- https://www.builtinboston.com/jobs
- https://www.builtinseattle.com/jobs

**Approach:**
- No official API (as of Nov 2025)
- Need to scrape job listings from each city's site
- Filter for design/UX internships

**Pros:**
- Tech/startup focused
- City-specific (can target high-design cities like SF, NYC)
- Free to scrape
- Design-forward companies use Built In

**Cons:**
- Need to build custom scraper
- No API (HTML scraping required)
- May have anti-bot protections
- Might overlap with other sources

**Expected results:** +10-20 internships across all cities

**Implementation time:** 2-3 days (build scraper for Built In job pages)

---

### 🔴 Tier 3: Advanced Solutions (2-4 weeks implementation)

#### 10. Workday Scraper ⭐ **UNLOCK BIG TECH**

**What it is:**
- Workday is used by Adobe, Airbnb, IBM, Oracle, VMware, many Fortune 500s
- Hardest to scrape (JavaScript-heavy, anti-bot protections)
- Unlocks companies you currently cannot access

**Available tools:**
- Apify: https://apify.com/shahidirfan/workday-job-scraper ($49-249/month)
- Apify: https://apify.com/gooyer.co/myworkdayjobs ($20-200/month)
- GitHub: https://github.com/chuchro3/WebCrawler (open-source, Selenium-based)

**How it works:**
- Workday uses dynamic JavaScript rendering
- Requires headless browser (Selenium, Puppeteer, Playwright)
- Jobs loaded via AJAX/fetch requests
- Need to reverse engineer API endpoints

**Companies using Workday (design-relevant):**
- Adobe (design software giant)
- Airbnb (design-forward)
- VMware, Oracle, IBM, HP
- Many large enterprises

**Pros:**
- Access to Fortune 500 companies
- High-quality, well-paying internships
- Unlocks companies Pitt CSC gets (Adobe, Airbnb, etc.)
- Thousands of companies use Workday

**Cons:**
- Technically challenging (JavaScript rendering required)
- Workday actively blocks scrapers
- Need residential proxies ($50-200/month)
- Legal gray area
- High maintenance (breaks when Workday updates)
- Commercial tools $50-250/month

**Expected results:** +30-60 high-quality internships

**Implementation time:** 2-4 weeks (or use commercial tool for $50-250/month)

**Risk level:** High (anti-bot detection, legal concerns)

---

#### 11. LinkedIn Jobs Scraper

**What it is:**
- LinkedIn has millions of job postings
- Most comprehensive job database globally
- Heavily restricted (most aggressive anti-bot measures)

**Challenges:**
- Rate limits after ~10 pages per IP
- Requires proxy rotation (residential proxies $50-200/month)
- Requires login (risk of account ban)
- LinkedIn actively fights scraping

**Available tools:**
- Bright Data: https://brightdata.com/products/web-scraper/linkedin/jobs (enterprise pricing)
- ScraperAPI: https://www.scraperapi.com/web-scraping/linkedin/jobs/ ($49-249/month)
- Apify: https://apify.com/bebity/linkedin-jobs-scraper ($49+/month)
- JobSpy library: Built-in LinkedIn support (free but rate limited)

**Pros:**
- Most comprehensive job database
- Design/UX/Product roles well-represented
- Internship filter available
- Salary data often included

**Cons:**
- Expensive (commercial tools $50-250/month)
- Rate limiting (need proxies)
- Account risk (can get banned)
- Maintenance intensive
- Ethical/legal concerns

**Expected results:** +50-100 internships (if done right)

**Implementation time:** 1-2 weeks with commercial tool, 3-4 weeks DIY

**Recommendation:** Use JobSpy library first (free), then consider commercial if needed

---

#### 12. SmartRecruiters / iCIMS / Taleo Scrapers

**What it is:**
- SmartRecruiters: Used by Canva, Bosch, IKEA, McDonald's (6,000+ companies)
- iCIMS: Used by Amazon (sometimes), Atlassian, many enterprises
- Taleo: Oracle's ATS, used by Boeing, Dell, HP, Intel

**Access:**
- SmartRecruiters: Job Board API available (requires partner status)
  - Third-party: Fantastic.jobs ($200-4000/month)
- iCIMS: API requires customer/partner access
- Taleo: API requires customer access

**Scraping tools:**
- Fantastic.jobs: Aggregates SmartRecruiters, iCIMS, others ($200-4000/month)
- Apify may have individual scrapers

**Pros:**
- Access to large enterprises
- High-quality, paid internships
- Thousands of companies use these platforms

**Cons:**
- No free API access
- Commercial tools expensive ($200-4000/month)
- Building scrapers is complex (anti-bot measures)
- Maintenance intensive

**Expected results:** +40-80 internships (if you can access the data)

**Recommendation:** Wait until you've exhausted free options, then consider Fantastic.jobs if budget allows

---

## 🎯 Recommended Implementation Roadmap

### Phase 1: Quick Wins (Week 1-2) - Target: 50-80 internships

**Priority tasks:**
1. ✅ Integrate JobSpy library (2 hours)
   - Add Indeed, Glassdoor, ZipRecruiter, LinkedIn scraping
   - Use free version, add proxies later if needed
   - Expected: +30-50 internships

2. ✅ Add Hacker News scraper (2 hours)
   - Use existing GitHub tool: https://github.com/SamG06/Who-is-hiring-scraper
   - Run monthly on GitHub Actions
   - Expected: +5-15 internships/month

3. ✅ Add RSS feeds (2 hours)
   - We Work Remotely, Remotive, Himalayas, Jobicy
   - Use feedparser library
   - Expected: +5-10 internships

4. ✅ Apply for Dribbble API (30 min)
   - Contact Dribbble for partnership
   - While waiting, continue with other tasks
   - Expected: +5-20 internships (if approved)

5. ✅ Research 20-30 more Greenhouse/Ashby companies (3 hours)
   - Check Greenhouse customer showcase
   - Add design agencies, mid-size tech companies
   - Expected: +10-20 internships

**Total time investment:** ~10-12 hours
**Expected results:** 50-80 total internships (up from 24)

---

### Phase 2: Medium Effort (Week 3-4) - Target: 100-150 internships

**Priority tasks:**
1. ✅ Build Workable scraper (1 week)
   - OR use Apify commercial tool (7-day free trial)
   - Research 50-100 Workable companies
   - Expected: +20-40 internships

2. ✅ Build JSON-LD structured data scraper (3 days)
   - Scrape career pages for schema.org JobPosting
   - Target companies with custom ATS (Apple, Google, Microsoft, Meta)
   - Expected: +30-50 internships

3. ✅ Try Google Jobs scraper (2 days)
   - Use Apify free trial or SerpAPI ($50/month)
   - Test with "UI UX design intern United States"
   - Expected: +50-100 internships (may have overlap)

**Total time investment:** ~2-3 weeks
**Expected results:** 100-150+ total internships

---

### Phase 3: Advanced (Month 2+) - Target: 200+ internships

**Priority tasks:**
1. ⚠️ Consider Workday scraper (2-4 weeks OR $50-250/month)
   - Use commercial tool (Apify) to avoid development complexity
   - Or build custom with Selenium/Playwright
   - Expected: +30-60 high-quality internships

2. ⚠️ Upgrade LinkedIn scraping (2 weeks OR $50-250/month)
   - Add proxy rotation to JobSpy
   - OR use commercial tool (ScraperAPI, Bright Data)
   - Expected: +50-100 internships

3. ⚠️ Built In job boards (2-3 days)
   - Scrape 8-10 city-specific boards
   - Expected: +10-20 internships

**Total investment:** ~1 month OR $100-500/month for commercial tools
**Expected results:** 200+ total internships

---

## 💰 Cost Analysis: DIY vs. Commercial

### Free Tier (Your Current Approach)
**Monthly cost:** $0 (GitHub Actions free tier)
**Results:** 24 internships
**Effort:** Initial setup + minimal maintenance

### Enhanced Free Tier (Phase 1)
**Monthly cost:** $0
**Results:** 50-80 internships
**Effort:** ~10-12 hours initial setup, 1 hour/week maintenance
**Tools:** JobSpy, HN scraper, RSS feeds, more Greenhouse companies

### Hybrid Approach (Phase 2)
**Monthly cost:** $0-50
**Results:** 100-150 internships
**Effort:** ~2-3 weeks initial setup, 2-3 hours/week maintenance
**Tools:** Free tools + Apify free trials + SerpAPI basic ($50/month)

### Commercial Approach (Phase 3)
**Monthly cost:** $100-500
**Results:** 200+ internships
**Effort:** ~1 week initial setup, 1-2 hours/week maintenance
**Tools:** Apify Workday scraper ($50-250/month) + LinkedIn scraper ($50-250/month)

**Cost per internship:**
- Current: $0 / 24 = $0
- Enhanced Free: $0 / 60 = $0
- Hybrid: $50 / 125 = $0.40/internship
- Commercial: $300 / 200 = $1.50/internship

**Recommendation:** Start with Enhanced Free (Phase 1), only go commercial if you need 200+

---

## 🛠️ Technical Implementation Guide

### Quick Start: Adding JobSpy (30 minutes)

**Step 1: Install**
```bash
pip install python-jobspy
```

**Step 2: Create new scraper**
```python
# src/scrapers/jobspy_scraper.py

from python_jobspy import scrape_jobs
import logging

logger = logging.getLogger(__name__)

class JobSpyScraper:
    """Scraper using JobSpy library for LinkedIn, Indeed, Glassdoor, etc."""

    def fetch_jobs(self, search_term="UI UX design intern", location="United States"):
        """Fetch jobs from multiple sources using JobSpy"""
        try:
            jobs = scrape_jobs(
                site_name=["indeed", "glassdoor", "zip_recruiter"],  # Skip LinkedIn for now (rate limits)
                search_term=search_term,
                location=location,
                distance=50,
                is_remote=True,
                job_type="internship",
                results_wanted=100,  # Per site
            )

            # Convert to your standard format
            standardized_jobs = []
            for _, job in jobs.iterrows():
                standardized_jobs.append({
                    'title': job['title'],
                    'company': job['company'],
                    'location': job['location'],
                    'url': job['job_url'],
                    'description': job['description'],
                    'posted_date': job['date_posted'],
                    'source': f"JobSpy ({job['site']})",
                    'salary': f"{job['min_amount']}-{job['max_amount']} {job['currency']}" if job['min_amount'] else None
                })

            logger.info(f"JobSpy found {len(standardized_jobs)} jobs")
            return standardized_jobs

        except Exception as e:
            logger.error(f"JobSpy error: {e}")
            return []
```

**Step 3: Add to main.py**
```python
from scrapers.jobspy_scraper import JobSpyScraper

# In __init__:
self.jobspy = JobSpyScraper()

# In scrape_all_sources:
logger.info("\n[9/9] Scraping with JobSpy...")
jobspy_jobs = self.jobspy.fetch_jobs(search_term='UI UX design intern')
logger.info(f"  → Found {len(jobspy_jobs)} jobs from JobSpy")
all_jobs.extend(jobspy_jobs)
```

**Expected results:** +30-50 internships in first run

---

### Quick Start: Adding Hacker News (20 minutes)

**Step 1: Install dependencies**
```bash
pip install requests
```

**Step 2: Create scraper**
```python
# src/scrapers/hackernews_scraper.py

import requests
import re
from datetime import datetime

class HackerNewsScraper:
    """Scrape 'Who is Hiring' threads from Hacker News"""

    ALGOLIA_API = "http://hn.algolia.com/api/v1/search"

    def fetch_jobs(self):
        """Fetch latest 'Who is Hiring' thread"""
        # Find latest thread
        params = {
            'query': 'Ask HN: Who is hiring?',
            'tags': 'story',
        }
        response = requests.get(self.ALGOLIA_API, params=params).json()

        if not response['hits']:
            return []

        # Get comments from thread
        thread_id = response['hits'][0]['objectID']
        thread_url = f"http://hn.algolia.com/api/v1/items/{thread_id}"
        thread_data = requests.get(thread_url).json()

        jobs = []
        for comment in thread_data.get('children', []):
            text = comment.get('text', '')

            # Filter for design/UX keywords
            if any(kw in text.lower() for kw in ['design', 'ux', 'ui', 'product design']):
                # Filter for internship
                if any(kw in text.lower() for kw in ['intern', 'internship']):
                    jobs.append({
                        'title': self._extract_title(text),
                        'company': self._extract_company(text),
                        'location': self._extract_location(text),
                        'url': f"https://news.ycombinator.com/item?id={comment['id']}",
                        'description': text[:500],  # First 500 chars
                        'posted_date': datetime.fromtimestamp(comment['created_at']).isoformat(),
                        'source': 'Hacker News'
                    })

        return jobs

    def _extract_title(self, text):
        # Simple heuristic: first line often contains title
        lines = text.split('\n')
        return lines[0][:100] if lines else "Internship"

    # ... add _extract_company, _extract_location methods
```

**Expected results:** +5-15 design internships per monthly thread

---

### Quick Start: Adding RSS Feeds (15 minutes)

**Step 1: Install**
```bash
pip install feedparser
```

**Step 2: Create scraper**
```python
# src/scrapers/rss_scraper.py

import feedparser
from datetime import datetime

class RSSJobScraper:
    """Scrape remote job RSS feeds"""

    FEEDS = [
        'https://weworkremotely.com/remote-jobs.rss',
        'https://remotive.com/remote-jobs/rss-feed',
        'https://himalayas.app/rss',
    ]

    def fetch_jobs(self):
        """Fetch all RSS feeds"""
        all_jobs = []

        for feed_url in self.FEEDS:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries:
                # Filter for design/UX
                if any(kw in entry.title.lower() for kw in ['design', 'ux', 'ui', 'product']):
                    # Filter for intern
                    if 'intern' in entry.title.lower() or 'intern' in entry.get('description', '').lower():
                        all_jobs.append({
                            'title': entry.title,
                            'company': entry.get('author', 'Unknown'),
                            'location': 'Remote',
                            'url': entry.link,
                            'description': entry.get('description', '')[:500],
                            'posted_date': entry.get('published', datetime.now().isoformat()),
                            'source': f"RSS ({feed_url.split('/')[2]})"
                        })

        return all_jobs
```

**Expected results:** +5-10 remote design internships

---

## 📊 Expected Results Summary

| Strategy | Implementation Time | Monthly Cost | Expected Internships | Difficulty |
|----------|-------------------|--------------|---------------------|------------|
| Current approach | - | $0 | 24 | ✅ Easy |
| + JobSpy | 2 hours | $0 | +30-50 | ✅ Easy |
| + Hacker News | 2 hours | $0 | +5-15 | ✅ Easy |
| + RSS feeds | 2 hours | $0 | +5-10 | ✅ Easy |
| + More Greenhouse companies | 3 hours | $0 | +10-20 | ✅ Easy |
| + Dribbble API | 1 hour + wait | $0 | +5-20 | ⚠️ Requires approval |
| **Phase 1 Total** | **~10 hours** | **$0** | **80-140** | ✅ **Easy** |
| + Workable scraper | 1 week | $0-50 | +20-40 | 🟡 Medium |
| + JSON-LD scraper | 3 days | $0 | +30-50 | 🟡 Medium |
| + Google Jobs scraper | 2 days | $50 | +50-100 | 🟡 Medium |
| **Phase 2 Total** | **2-3 weeks** | **$50** | **180-330** | 🟡 **Medium** |
| + Workday scraper | 2-4 weeks | $50-250 | +30-60 | 🔴 Hard |
| + LinkedIn (advanced) | 2 weeks | $50-250 | +50-100 | 🔴 Hard |
| + Built In boards | 3 days | $0 | +10-20 | 🟡 Medium |
| **Phase 3 Total** | **1 month** | **$100-500** | **270-510** | 🔴 **Hard** |

**Recommended path:** Phase 1 (get to 80-140 internships with ~10 hours work) → Evaluate if Phase 2 needed

---

## ⚖️ Legal & Ethical Considerations

### ✅ Legal and Encouraged
- Public APIs (Greenhouse, Ashby, Lever, Dribbble, Hacker News)
- RSS feeds (explicitly meant for aggregation)
- JSON-LD structured data (public, standardized)
- Your current approach (all good!)

### ⚠️ Gray Area (Proceed with Caution)
- Web scraping public job listings (JobSpy, Google Jobs, etc.)
  - Generally legal if data is publicly accessible
  - Respect robots.txt
  - Use reasonable rate limiting
  - Don't bypass authentication
  - Check terms of service

### 🔴 Risky (Consider Alternatives)
- LinkedIn scraping (aggressive anti-bot, account ban risk)
- Scraping sites that explicitly forbid it in ToS
- Bypassing CAPTCHA or login walls
- High-volume scraping without rate limiting

### Best Practices
1. Always respect robots.txt
2. Use reasonable delays (1-2 seconds between requests)
3. Identify your bot (user agent string)
4. Cache results (don't re-scrape unnecessarily)
5. Prefer APIs over scraping when available
6. Don't resell scraped data commercially
7. Attribute sources appropriately

**Disclaimer:** I'm not a lawyer. This is general guidance. Consult legal counsel if concerned.

---

## 🎯 Final Recommendations

### For Maximum Results with Minimal Effort:

**Week 1:** Implement Quick Wins
1. Add JobSpy library (2 hours) → +30-50 internships
2. Add Hacker News scraper (2 hours) → +5-15 internships
3. Add RSS feeds (2 hours) → +5-10 internships
4. Research 20 more Greenhouse companies (3 hours) → +10-20 internships
5. Apply for Dribbble API access (30 min) → +5-20 internships (if approved)

**Total time:** ~10 hours
**Total cost:** $0
**Expected results:** 80-140 internships (3-5x improvement)

**Week 2-3:** Evaluate if you need more
- If 80-140 is enough → Done! Just maintain
- If you want 150+ → Proceed to Phase 2 (Workable, JSON-LD, Google Jobs)

**Month 2+:** Only if you need 200+
- Consider commercial tools (Workday, LinkedIn scrapers)
- Budget $100-500/month
- Or build custom scrapers (significant time investment)

---

## 📚 Resources & Links

### Libraries & Tools
- **JobSpy:** https://github.com/speedyapply/JobSpy
- **Hacker News API:** https://github.com/HackerNews/API
- **HN Job Scraper:** https://github.com/SamG06/Who-is-hiring-scraper
- **Feedparser (RSS):** https://pypi.org/project/feedparser/
- **BeautifulSoup (JSON-LD):** https://www.crummy.com/software/BeautifulSoup/

### Commercial Tools
- **Apify (various scrapers):** https://apify.com/
- **SerpAPI (Google Jobs):** https://serpapi.com/google-jobs-api
- **ScraperAPI:** https://www.scraperapi.com/
- **Bright Data:** https://brightdata.com/
- **Fantastic.jobs (ATS feeds):** https://fantastic.jobs/

### APIs
- **Greenhouse:** https://developers.greenhouse.io/
- **Ashby:** https://developers.ashbyhq.com/
- **Lever:** https://hire.lever.co/developer/documentation
- **Dribbble:** https://developer.dribbble.com/v2/jobs/
- **Workable:** https://developers.workable.com/

### Tutorials
- **JobSpy Tutorial:** https://www.franciscomoretti.com/blog/automate-your-job-search
- **JSON-LD Scraping:** https://datawookie.dev/blog/2025/02/scraping-linked-ld-json-data/
- **Google Jobs Scraping:** https://scrapfly.io/blog/posts/guide-to-google-jobs-api-and-alternatives

---

**Last Updated:** 2025-11-10
**Next Steps:** Start with Phase 1 Quick Wins (JobSpy + HN + RSS + More Companies)
