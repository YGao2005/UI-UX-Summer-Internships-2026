# Comprehensive Free Job Board APIs & Data Sources (2025)

**Last Updated:** November 2025
**Purpose:** Finding UI/UX internships and entry-level positions

---

## Table of Contents
1. [Free Job APIs with Public Access](#free-job-apis-with-public-access)
2. [Public ATS (Application Tracking System) Endpoints](#public-ats-endpoints)
3. [RSS/Atom Feeds for Job Boards](#rss-atom-feeds)
4. [GitHub Jobs Alternatives](#github-jobs-alternatives)
5. [Regional & Specialized APIs](#regional-specialized-apis)
6. [Summary Comparison Table](#summary-comparison-table)
7. [Best Practices & Legal Considerations](#best-practices-legal-considerations)

---

## Free Job APIs with Public Access

### 1. Adzuna API
**Status:** ✅ Active & Free (2025)

- **Endpoint URL:** `https://api.adzuna.com/v1/api`
- **Authentication:** Requires `app_id` and `app_key` (free registration)
- **Rate Limits:**
  - Not officially documented for free tier
  - Default limits can be increased by contacting Adzuna
  - Commercial users have 14-day trial period
  - Biggest users do millions of requests per day (with approval)
- **Free Tier:** Yes - register at [developer.adzuna.com](https://developer.adzuna.com/)
- **Endpoints Available:**
  - Job search with filters
  - Historical salary trends
  - Salary distribution (histogram)
  - Regional vacancy data
  - Top company listings
  - Job categorization
- **Data Format:** JSON (recommended), XML (being phased out)
- **Best for Internships:** ⭐⭐⭐ Good - aggregates from multiple sources
- **Coverage:** Multiple countries including US, UK, Canada, Australia
- **Notable Restrictions:**
  - Must maintain API key confidentiality
  - Commercial use requires contacting Adzuna
  - Pagination limited to 50 results per page
- **Documentation:** https://developer.adzuna.com/

---

### 2. RemoteOK API
**Status:** ✅ Active & Free (2025)

- **Endpoint URL:** `https://remoteok.io/api`
- **Authentication:** None required
- **Rate Limits:** No official documentation, but respect reasonable usage
- **Free Tier:** Completely free
- **Data Coverage:** 80% of remote jobs on the web (30,000+ listings)
- **Data Format:** JSON, RSS, and HTML feeds available
- **Reliability:** 91% uptime, 134ms avg response time (as of 2025)
- **CORS:** Enabled
- **Best for Internships:** ⭐⭐⭐⭐ Excellent - includes remote internships
- **Notable Restrictions:**
  - Must mention RemoteOK as a source
  - Must link back to job listing URL on RemoteOK with DIRECT link (no redirects)
  - Legal requirement via terms of use
- **Documentation:** Minimal - self-documenting API
- **Additional Features:** Filter by remote status, visa sponsorship

---

### 3. Remotive API
**Status:** ✅ Active & Free (2025) - 24-hour delay on free tier

- **Endpoint URL:** `https://remotive.com/api/remote-jobs`
- **Authentication:** None for public API
- **Rate Limits:**
  - Maximum 4 times per day recommended
  - More than 2 requests per minute will be blocked
- **Free Tier:** Yes, with 24-hour delay on job postings
- **Paid API:** Available via hello@remotive.com for real-time access
- **Data Format:** JSON
- **Filtering Options:**
  - Category
  - Company name
  - Search terms (job title and description)
  - Result limits
- **Best for Internships:** ⭐⭐⭐ Good - remote internships available
- **Notable Restrictions:**
  - Must link back to Remotive URL
  - Must mention Remotive as a source
  - API access will be terminated without attribution
- **Documentation:** https://remotive.com/remote-jobs/api
- **GitHub:** https://github.com/remotive-com/remote-jobs-api

---

### 4. The Muse API
**Status:** ✅ Active & Free (2025)

- **Endpoint URL:** `https://www.themuse.com/api/public/jobs`
- **Authentication:** API key required (free registration)
- **Rate Limits:**
  - **Unregistered:** 500 requests/hour
  - **Registered:** 3,600 requests/hour
- **Free Tier:** Yes
- **Main Endpoints:**
  - GET `/api/public/jobs` - Job listings
  - GET `/api/public/companies` - Company profiles
  - GET `/api/public/coaches` - Career coaches
- **Data Format:** JSON only
- **Filtering Options:**
  - Company
  - Category
  - Level (including internships)
  - Location
  - Page (pagination)
- **Results:** 20 items per page
- **Best for Internships:** ⭐⭐⭐⭐⭐ Excellent - has specific "internship" level filter
- **Rate Limit Headers:**
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Limit`
  - `X-RateLimit-Reset`
- **Notable Restrictions:**
  - Must accept terms and conditions
  - Registration required for production use
- **Documentation:** https://www.themuse.com/developers/api/v2

---

### 5. USAJobs API (US Government Jobs)
**Status:** ✅ Active & Free (2025)

- **Endpoint URL:** `https://data.usajobs.gov/api/Search`
- **Authentication:** API key required (apply at developer.usajobs.gov)
- **Rate Limits:** Not explicitly documented
- **Free Tier:** Yes
- **Main Endpoints:**
  - `/api/Search` (requires auth)
  - `/api/HistoricJoa` (no auth required)
  - Multiple codelist endpoints (no auth required)
- **Data Format:** JSON
- **Pagination:** 250 jobs per page (default), up to 500 max
- **Best for Internships:** ⭐⭐⭐⭐ Very Good - includes federal internship programs (Pathways)
- **Coverage:** All US federal government jobs
- **Notable Restrictions:**
  - Cannot rent, lease, loan, sell, trade, or create derivative works
  - Data sharing requires written OPM approval
  - Must maintain API key confidentiality
  - Contact: access@usajobs.gov
- **Documentation:** https://developer.usajobs.gov/

---

### 6. Arbeitnow Free Job Board API
**Status:** ✅ Active & Free (2025)

- **Endpoint URL:** `https://www.arbeitnow.com/api/job-board-api`
- **Authentication:** None required - No API key needed
- **Rate Limits:** Not documented
- **Free Tier:** Completely free
- **Data Sources:** Aggregates from multiple ATS:
  - Greenhouse
  - SmartRecruiters
  - Join.com
  - Team Tailor
  - Recruitee
  - Comeet
  - Lever
  - Personio
- **Data Format:** JSON
- **Coverage:** Primarily Germany/Europe + Remote positions
- **Filtering Options:**
  - Remote status
  - Visa sponsorship
  - Location
- **Best for Internships:** ⭐⭐⭐ Good - European internships
- **Notable Restrictions:** Check Postman documentation for full details
- **Documentation:** Available via Postman
- **Website:** https://www.arbeitnow.com/

---

### 7. JSearch API (RapidAPI)
**Status:** ✅ Active & Free Tier Available (2025)

- **Endpoint URL:** Via RapidAPI platform
- **Authentication:** RapidAPI key required
- **Rate Limits:** Varies by RapidAPI tier
- **Free Tier:** Yes (limited requests)
- **Data Sources:** Real-time data from Google for Jobs
- **Coverage:** Aggregates from LinkedIn, Indeed, Glassdoor, and 16+ job sites
- **Data Format:** JSON
- **Best for Internships:** ⭐⭐⭐⭐ Very Good - searches across major platforms
- **Special Features:**
  - Real-time job listings
  - Salary data
  - Fast and reliable
- **Notable Restrictions:** Subject to RapidAPI terms
- **Documentation:** https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
- **Alternative:** Dedicated Internships API also available on RapidAPI

---

### 8. Findwork.dev API
**Status:** ✅ Active & Free (2025)

- **Endpoint URL:** Via findwork.dev
- **Authentication:** API token required (free account)
- **Rate Limits:** Not explicitly documented
- **Free Tier:** Completely free
- **Coverage:** Development and design jobs specifically
- **Data Sources:**
  - Hacker News
  - RemoteOK
  - WeWorkRemotely
  - Dribbble
- **Data Format:** JSON or XML
- **Filtering Options:**
  - Geography
  - Employment type
  - Full-text search
- **Best for Internships:** ⭐⭐⭐⭐ Very Good - tech/design focus matches UI/UX
- **Authentication:** Simple token-based HTTP authentication
- **Notable Restrictions:** Free but requires account
- **Documentation:** https://findwork.dev/developers
- **Sign up:** Create account at findwork.dev

---

### 9. Reed API (UK Jobs)
**Status:** ✅ Active & Free (2025)

- **Endpoint URL:** `https://www.reed.co.uk/api/`
- **Authentication:** API key required (free registration)
- **Rate Limits:**
  - **Jobseeker API:** 1,000 requests/day per API key
  - **Recruiter API:** 2,000 requests/hour (customizable)
- **Free Tier:** Yes
- **Coverage:** UK-focused job listings
- **Data Format:** JSON
- **Endpoints:**
  - Job search
  - Job details
  - Post jobs (Recruiter API)
  - Search candidates (Recruiter API)
- **Best for Internships:** ⭐⭐⭐ Good if targeting UK internships
- **Notable Restrictions:** UK-centric
- **Documentation:** https://www.reed.co.uk/developers

---

### 10. Jooble API
**Status:** ✅ Active & Free (2025)

- **Endpoint URL:** `POST https://jooble.org/api/{api_Key}`
- **Authentication:** API key required (register at jooble.org)
- **Rate Limits:** "Generous" but not explicitly documented
- **Free Tier:** Yes
- **Coverage:** International - multiple countries
- **Data Format:** JSON
- **Job Categories:**
  - On-site
  - Remote
  - Contract
  - Visa sponsorship
  - Volunteering
  - Internships
- **Parameters:**
  - keywords (required)
  - location (required)
  - radius (optional, in km)
  - salary (optional, minimum)
  - page (optional)
- **Best for Internships:** ⭐⭐⭐⭐ Very Good - explicit internship category
- **Notable Restrictions:** Subject to terms of use
- **Documentation:** https://jooble.org/api/about
- **Help Center:** https://help.jooble.org/

---

### 11. CareerJet API
**Status:** ✅ Active & Free (2025)

- **Endpoint URL:** `https://www.careerjet.com/partners/api/`
- **Authentication:** API key required (free registration)
- **Rate Limits:**
  - Limited to prevent misuse
  - Can be lifted after site review by CareerJet
- **Free Tier:** Yes
- **Data Format:** JSON and XML
- **Filtering Options:**
  - Keywords
  - Locations
  - Companies
  - Industries
  - Other criteria
- **Best for Internships:** ⭐⭐⭐ Good - international coverage
- **Coverage:** Multiple countries
- **Notable Restrictions:** Frequency limits unless lifted
- **Documentation:** https://www.careerjet.com/partners/api/

---

## Public ATS Endpoints

### 1. Greenhouse Job Board API
**Status:** ✅ Active & Free (2025)

- **Base URL:** `https://boards-api.greenhouse.io/v1/boards/{board_token}/`
- **Authentication:**
  - **GET endpoints:** None required
  - **POST endpoints:** Basic Auth with API key (for applications)
- **Rate Limits:** Not documented - appears unlimited for GET requests
- **Free Tier:** Yes, GET endpoints are completely public
- **How to Find board_token:**
  - From company job board URL: `https://boards.greenhouse.io/acme` → token is `acme`
- **Public Endpoints (No Auth):**
  - `GET /v1/boards/{board_token}/jobs` - List all jobs
  - `GET /v1/boards/{board_token}/jobs/{job_id}` - Job details
  - `GET /v1/boards/{board_token}/offices` - Office locations
  - `GET /v1/boards/{board_token}/departments` - Departments
  - Education endpoints (degrees, disciplines, schools)
- **Data Format:** JSON
- **JSONP:** Supported for cross-domain requests
- **Best for Internships:** ⭐⭐⭐⭐⭐ Excellent - many tech companies use Greenhouse
- **Notable Features:**
  - Cached and not rate-limited
  - Ideal for building custom career pages
  - No authentication needed for reading
- **Security Note:** Never expose API key client-side (for POST endpoints)
- **Documentation:** https://developers.greenhouse.io/job-board.html

**Example Companies Using Greenhouse:**
- Airbnb, Spotify, HubSpot, Pinterest, Lyft, DoorDash, many startups

---

### 2. Lever Job Board API
**Status:** ✅ Active & Free (2025)

- **Base URL:**
  - Global: `https://api.lever.co/v0/postings/`
  - EU: `https://api.eu.lever.co/v0/postings/`
- **Authentication:**
  - **GET endpoints:** None required
  - **POST endpoints:** API key required (2 requests/second limit)
- **Rate Limits:** 2 requests/second for POST (applications)
- **Free Tier:** Yes, GET endpoints are public
- **How to Access:**
  - Find company site name (usually company name without spaces)
  - Example: `https://api.lever.co/v0/postings/leverdemo`
- **Public Endpoints (No Auth):**
  - `GET /v0/postings/{site}` - List all published jobs
  - `GET /v0/postings/{site}/{posting_id}` - Job details
- **Query Parameters:**
  - `skip` - Pagination offset
  - `limit` - Results per page
  - `mode` - Response format (json, html, iframe)
- **Data Format:** JSON (recommended), HTML, iframe
- **Job Visibility:** Only published postings are public
- **Best for Internships:** ⭐⭐⭐⭐⭐ Excellent - popular with tech companies
- **Response Fields:**
  - `id`, `text` (title), `categories` (location, commitment, team, department)
  - `description`, `opening`, `lists` (requirements, benefits)
  - `hostedUrl`, `applyUrl`, `workplaceType`, `salaryRange`
- **Rate Limiting:** 429 status code when exceeded (for POST)
- **Documentation:** https://github.com/lever/postings-api

**Example Companies Using Lever:**
- Netflix, Eventbrite, Shopify, IDEO, many Y Combinator companies

---

### 3. Ashby Job Board API
**Status:** ✅ Active & Free (2025)

- **Base URL:** `https://api.ashbyhq.com/posting-api/job-board/{job_board_name}`
- **Authentication:** None required
- **Rate Limits:** Not documented
- **Free Tier:** Yes, completely public
- **Query Parameters:**
  - `includeCompensation` - true/false (optional)
- **How to Find job_board_name:**
  - From company's Ashby-hosted job board URL
- **Data Format:** JSON
- **Response Structure:**
  - `apiVersion` (currently "1")
  - `jobs` array with:
    - title, location, department
    - employment type
    - descriptions
    - URLs
    - compensation (if requested)
- **Best for Internships:** ⭐⭐⭐⭐ Very Good - newer ATS, growing adoption
- **Notable Features:**
  - Simple public API
  - No authentication needed
  - Compensation data available
- **Limitations:**
  - No filtering/searching via API
  - More advanced features require Ashby Developer API (customer only)
- **Documentation:** https://developers.ashbyhq.com/docs/public-job-posting-api

**Example Companies Using Ashby:**
- Notion, Ramp, OpenAI, Anthropic, Scale AI

---

### 4. Workday Job Listings
**Status:** ⚠️ Limited - No official public API (2025)

- **Public Access:** Via company-specific career pages only
- **API Endpoint:** No standardized public API
- **Authentication:** N/A
- **Best for Internships:** ⭐⭐ Fair - large enterprises use Workday
- **How to Access:**
  - Companies have individual career page URLs
  - Format varies: `{company}.wd1.myworkdayjobs.com`
  - Can be scraped but violates ToS
- **Alternative:** Use RSS feeds if provided by specific companies
- **Data Feeds:** Some companies offer job data feeds through Workday
- **Notable Restrictions:** No public API available
- **Integration:** Ashby offers bi-directional integration with Workday

**Note:** Workday is used by many Fortune 500 companies but doesn't provide a public API for job listings aggregation.

---

## RSS/Atom Feeds

### RSS Feed Patterns

**Status:** ⚠️ Declining but still available

Many job boards and career pages offer RSS feeds, though their usage has declined in favor of email alerts.

#### Common RSS Feed Formats:

1. **Job Board Standard:**
   - Format: RSS 2.0 (XML-based)
   - Auto-generated by many job board platforms
   - Usually found at: `/feed`, `/rss`, `/jobs.rss`, `/jobs/feed`

2. **Company Career Page Patterns:**
   - `{company-site}/careers/feed`
   - `{company-site}/jobs.rss`
   - `{company-site}/api/jobs.xml`

3. **Common Fields:**
   - Job title
   - Description
   - Location
   - Date posted
   - Apply URL
   - Category/department

#### Job Boards with RSS Feeds:

**Known to Have RSS:**
- **Stack Overflow Jobs** (deprecated as of 2022)
- **Indeed** - Limited, mostly company-specific
- **AngelList** - Some feeds available
- **RemoteOK** - `https://remoteok.io/remote-jobs.rss`
- **Authentic Jobs** - RSS available
- **We Work Remotely** - RSS available

**RSS Feed Aggregation Platforms:**
- JBoard.io
- SmartJobBoard
- Jobboard.io
- JBoard (automated RSS imports)

#### Best Practices for RSS Feeds:

1. **Backfilling:** Use RSS feeds to populate new job boards
2. **Monitoring:** Check feeds 2-4 times per day
3. **Parsing:** XML parsers for RSS 2.0 format
4. **Deduplication:** Track job IDs to avoid duplicates
5. **Respect ToS:** Many feeds require attribution

#### Limitations:

- Declining adoption (email preferred)
- Often incomplete data
- May have delays
- Limited filtering options
- Some feeds are discontinued without notice

**Best for Internships:** ⭐⭐ Fair - depends on specific feeds

---

## GitHub Jobs Alternatives

**GitHub Jobs Status:** ❌ Shut down in August 2021

### Community-Maintained Aggregators:

#### 1. JobSpy (Open Source)
- **GitHub:** https://github.com/speedyapply/JobSpy
- **License:** MIT (free to use)
- **Status:** ✅ Active (2025)
- **Supported Sources:**
  - LinkedIn
  - Indeed
  - Glassdoor
  - Google Jobs
  - ZipRecruiter
- **Language:** Python library
- **Best for Internships:** ⭐⭐⭐⭐ Very Good - scrapes major sites
- **Type:** Scraper library (check ToS of target sites)

#### 2. Remote OK
- **URL:** https://remoteok.com/
- **Status:** ✅ Active
- **Type:** Aggregator + API
- **Focus:** Remote positions (including internships)
- **API:** Public and free

#### 3. WeWorkRemotely
- **URL:** https://weworkremotely.com/
- **Status:** ✅ Active
- **Type:** Job board
- **Focus:** Remote work
- **API:** Limited/unofficial

#### 4. Authentic Jobs
- **URL:** https://authenticjobs.com/
- **Status:** ✅ Active
- **Type:** Job board
- **Focus:** Design, development, creative
- **Best for Internships:** ⭐⭐⭐⭐ Very Good for UI/UX

#### 5. Jobspresso
- **URL:** https://jobspresso.co/
- **Status:** ✅ Active
- **Type:** Remote job aggregator
- **Focus:** Tech, marketing, customer support

#### 6. Remote Index
- **URL:** https://remoteindex.co/
- **Status:** ✅ Active
- **Type:** Aggregator
- **Focus:** Tech remote jobs

#### 7. SlashJobs
- **URL:** https://slashjobs.com/
- **Status:** ✅ Active
- **Type:** Remote dev jobs aggregator
- **Features:** AND/OR/NOT filters, no signup required

#### 8. tokenjobs.io
- **URL:** https://tokenjobs.io/
- **Status:** ✅ Active
- **Type:** Web3 job aggregator
- **Focus:** Crypto/blockchain jobs

---

## Regional & Specialized APIs

### UK-Specific:

**Reed API** (covered above)
- 1,000 requests/day
- UK jobs only

**Lightcast UK Jobs API**
- Paid service
- Comprehensive UK labor market data

### Europe-Specific:

**Arbeitnow** (covered above)
- Germany/Europe focus
- Free, no auth required

### Web3/Blockchain:

**tokenjobs.io**
- Filter by keywords, locations, languages, contract types

### Design/Creative:

**Authentic Jobs**
- Design, development, creative roles
- RSS feeds available

**Dribbble Jobs**
- Aggregated by Findwork.dev

### Developer-Specific:

**Findwork.dev** (covered above)
- Development and design focus
- Aggregates from Hacker News, RemoteOK, etc.

**Hacker News "Who's Hiring?"**
- Monthly threads
- Can be scraped (check ToS)

---

## Summary Comparison Table

| API Name | Auth Required | Rate Limit | Free Tier | Internships | Coverage | Status |
|----------|--------------|------------|-----------|-------------|----------|---------|
| **Adzuna** | API Key | Not documented | ✅ Yes | ⭐⭐⭐ | Multi-country | ✅ Active |
| **RemoteOK** | None | Reasonable use | ✅ Yes | ⭐⭐⭐⭐ | Global remote | ✅ Active |
| **Remotive** | None (free) | 4x/day max | ✅ Yes (24h delay) | ⭐⭐⭐ | Global remote | ✅ Active |
| **The Muse** | API Key | 500-3600/hr | ✅ Yes | ⭐⭐⭐⭐⭐ | US-focused | ✅ Active |
| **USAJobs** | API Key | Not documented | ✅ Yes | ⭐⭐⭐⭐ | US Gov only | ✅ Active |
| **Arbeitnow** | None | Not documented | ✅ Yes | ⭐⭐⭐ | EU-focused | ✅ Active |
| **JSearch** | RapidAPI Key | Tier-based | ✅ Yes (limited) | ⭐⭐⭐⭐ | Multi-source | ✅ Active |
| **Findwork** | API Token | Not documented | ✅ Yes | ⭐⭐⭐⭐ | Dev/Design | ✅ Active |
| **Reed** | API Key | 1000/day | ✅ Yes | ⭐⭐⭐ | UK only | ✅ Active |
| **Jooble** | API Key | "Generous" | ✅ Yes | ⭐⭐⭐⭐ | Multi-country | ✅ Active |
| **CareerJet** | API Key | Can be lifted | ✅ Yes | ⭐⭐⭐ | Multi-country | ✅ Active |
| **Greenhouse** | None (GET) | Unlimited | ✅ Yes | ⭐⭐⭐⭐⭐ | Per-company | ✅ Active |
| **Lever** | None (GET) | Unlimited (GET) | ✅ Yes | ⭐⭐⭐⭐⭐ | Per-company | ✅ Active |
| **Ashby** | None | Not documented | ✅ Yes | ⭐⭐⭐⭐ | Per-company | ✅ Active |
| **Workday** | N/A | N/A | ❌ No API | ⭐⭐ | Per-company | ⚠️ Limited |

---

## Best Practices & Legal Considerations

### 1. Authentication & API Keys

**Security:**
- Never expose API keys in client-side code
- Use environment variables
- Rotate keys periodically
- Use proxy servers for form submissions

**Registration:**
- Most APIs require free registration
- Provide accurate contact information
- Read and accept terms of service

### 2. Rate Limiting

**Best Practices:**
- Implement exponential backoff
- Cache responses when possible
- Respect documented rate limits
- Monitor rate limit headers
- Don't exceed 2 requests/second for non-specified APIs

**Common Headers:**
```
X-RateLimit-Limit: 3600
X-RateLimit-Remaining: 3599
X-RateLimit-Reset: 1635724800
Retry-After: 60
```

### 3. Attribution Requirements

**Required Attribution:**
- **RemoteOK:** Must mention and link back (DIRECT link, no redirects)
- **Remotive:** Must mention and link back (access terminated without)
- **Adzuna:** Check terms for commercial use
- **The Muse:** Accept terms and conditions

**Recommended Format:**
```
Job listings powered by [API Name]
Link: [Direct link to original posting]
```

### 4. Data Usage & Storage

**Allowed:**
- Caching for reasonable periods (24-48 hours)
- Displaying job listings
- Search and filtering
- User applications

**Prohibited (typically):**
- Reselling job data
- Creating derivative databases for sale
- Removing attribution
- Excessive scraping
- Violating rate limits

### 5. Legal Considerations

**Web Scraping:**
- LinkedIn scraping violates ToS (legal gray area: HiQ vs. LinkedIn case)
- Public data scraping is legal in many jurisdictions
- Always check robots.txt
- Respect ToS even if legally allowed

**GDPR Compliance:**
- Job listings may contain personal data
- Ensure proper data handling
- Provide privacy policies
- Allow data deletion requests

**Terms of Service:**
- Read carefully before integration
- Commercial use may require approval
- Some APIs prohibit certain industries
- Contact providers for clarification

### 6. Technical Best Practices

**Error Handling:**
```python
# Example: Handle rate limits
def api_request_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 429:  # Too Many Requests
                retry_after = int(response.headers.get('Retry-After', 60))
                time.sleep(retry_after)
                continue
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

**Pagination:**
```python
# Example: Handle pagination
def get_all_jobs(api_url, max_pages=10):
    jobs = []
    page = 1
    while page <= max_pages:
        response = requests.get(f"{api_url}?page={page}")
        data = response.json()
        if not data.get('results'):
            break
        jobs.extend(data['results'])
        page += 1
        time.sleep(1)  # Rate limiting
    return jobs
```

**Caching:**
```python
# Example: Simple cache with expiration
import time
from functools import lru_cache

@lru_cache(maxsize=128)
def fetch_jobs_cached(api_url, cache_key):
    # Cache key includes timestamp for TTL
    return fetch_jobs(api_url)

# Use with timestamp for 1-hour cache
cache_key = int(time.time() / 3600)
jobs = fetch_jobs_cached(api_url, cache_key)
```

### 7. Monitoring & Maintenance

**Track Metrics:**
- API response times
- Error rates (4xx, 5xx)
- Rate limit consumption
- Data freshness
- Job posting duplicates

**Alerts:**
- API downtime
- Rate limit warnings (>80% consumed)
- Unusual error rates
- Terms of Service changes

**Regular Maintenance:**
- Update API keys before expiration
- Review API changelogs
- Test endpoints monthly
- Update documentation
- Remove deprecated endpoints

### 8. Cost Optimization

**Free Tier Strategies:**
- Combine multiple free APIs
- Cache aggressively (within ToS)
- Use ATS APIs for specific companies
- Implement smart polling (only when needed)
- Share API keys across projects (if allowed)

**Scaling:**
- Start with free tiers
- Monitor usage patterns
- Upgrade selectively to paid tiers
- Use webhooks instead of polling (if available)
- Implement job deduplication

---

## Recommended Strategy for UI/UX Internship Scraper

### Primary APIs (High Priority):

1. **The Muse API** ⭐⭐⭐⭐⭐
   - Explicit internship filter
   - 3,600 requests/hour (free)
   - Good for UI/UX roles

2. **Greenhouse Public API** ⭐⭐⭐⭐⭐
   - Target specific tech companies
   - Unlimited reads
   - Many design-focused companies

3. **Lever Public API** ⭐⭐⭐⭐⭐
   - Target specific tech companies
   - Unlimited reads
   - Popular with startups

4. **Findwork.dev API** ⭐⭐⭐⭐
   - Design/dev focus
   - Aggregates from multiple sources
   - Free

### Secondary APIs (Medium Priority):

5. **RemoteOK API** ⭐⭐⭐⭐
   - Remote UI/UX internships
   - No auth required
   - Good coverage

6. **JSearch (RapidAPI)** ⭐⭐⭐⭐
   - Aggregates major sites
   - Real-time data
   - Free tier available

7. **Jooble API** ⭐⭐⭐⭐
   - International coverage
   - Internship category
   - Generous limits

### Supplementary APIs (Low Priority):

8. **Adzuna API**
   - Additional coverage
   - Multiple countries

9. **USAJobs API**
   - Federal internship programs (Pathways)
   - Good for diversity

10. **Ashby Public API**
    - Modern tech companies
    - Growing adoption

### Implementation Approach:

```python
# Example: Multi-API aggregator
apis = [
    {'name': 'The Muse', 'priority': 1, 'rate_limit': 3600},
    {'name': 'Greenhouse', 'priority': 1, 'rate_limit': None},
    {'name': 'Lever', 'priority': 1, 'rate_limit': None},
    {'name': 'Findwork', 'priority': 1, 'rate_limit': None},
    {'name': 'RemoteOK', 'priority': 2, 'rate_limit': None},
    {'name': 'JSearch', 'priority': 2, 'rate_limit': 'tier-based'},
]

def aggregate_internships(keywords=['ui', 'ux', 'design', 'product']):
    all_jobs = []

    for api in apis:
        try:
            jobs = fetch_from_api(api, keywords, job_type='internship')
            all_jobs.extend(jobs)
            time.sleep(1)  # Rate limiting
        except Exception as e:
            log_error(api['name'], e)
            continue

    # Deduplicate by job title + company
    unique_jobs = deduplicate(all_jobs)
    return unique_jobs
```

### Target Companies for ATS APIs:

**Top UI/UX Companies Using Greenhouse:**
- Airbnb, Spotify, Pinterest, HubSpot, Lyft, DoorDash

**Top UI/UX Companies Using Lever:**
- Netflix, Eventbrite, Shopify, IDEO, Stripe

**Top UI/UX Companies Using Ashby:**
- Notion, Ramp, OpenAI, Anthropic, Scale AI

**How to Find board_token/site_name:**
1. Visit company careers page
2. Look for URL pattern:
   - Greenhouse: `boards.greenhouse.io/{board_token}`
   - Lever: `jobs.lever.co/{site_name}`
   - Ashby: `jobs.ashbyhq.com/{job_board_name}`

---

## Additional Resources

### API Documentation Links:
- [Adzuna Docs](https://developer.adzuna.com/)
- [Greenhouse Job Board API](https://developers.greenhouse.io/job-board.html)
- [Lever Postings API](https://github.com/lever/postings-api)
- [Ashby Public API](https://developers.ashbyhq.com/docs/public-job-posting-api)
- [The Muse API](https://www.themuse.com/developers/api/v2)
- [USAJobs API](https://developer.usajobs.gov/)
- [Reed API](https://www.reed.co.uk/developers)
- [Jooble API](https://jooble.org/api/about)

### Community Resources:
- [Public APIs Directory - Jobs Category](https://publicapis.io/)
- [awesome-remote-job (GitHub)](https://github.com/lukasz-madon/awesome-remote-job)
- [JobSpy (GitHub)](https://github.com/speedyapply/JobSpy)
- [RapidAPI Jobs Collection](https://rapidapi.com/collection/job-search-apis)

### Legal Resources:
- HiQ vs. LinkedIn (web scraping case law)
- GDPR compliance for job data
- Terms of Service templates

---

## Changelog

**November 2025:**
- Initial comprehensive research
- Verified all APIs active and free
- Documented rate limits where available
- Added ATS public endpoints
- Included GitHub Jobs alternatives
- RSS feed patterns documented

**Notes:**
- Rate limits subject to change - verify with official docs
- Free tiers may be modified by providers
- Always check current Terms of Service
- Contact providers for commercial/high-volume use

---

**Maintained by:** UI/UX Internship Scraper Project
**Contact:** Update as needed
**Last Verified:** November 2025

---

## Quick Start Checklist

- [ ] Register for The Muse API key
- [ ] Register for Adzuna API key
- [ ] Register for USAJobs API key
- [ ] Sign up for Findwork.dev account
- [ ] Get RapidAPI key for JSearch
- [ ] Test RemoteOK API (no auth)
- [ ] Test Remotive API (no auth)
- [ ] Test Arbeitnow API (no auth)
- [ ] Identify target companies using Greenhouse
- [ ] Identify target companies using Lever
- [ ] Identify target companies using Ashby
- [ ] Set up error logging
- [ ] Implement rate limiting
- [ ] Create caching strategy
- [ ] Add attribution to job listings
- [ ] Set up monitoring alerts
- [ ] Review all Terms of Service
- [ ] Implement data deduplication
- [ ] Test pagination handling
- [ ] Create backup API strategy

**Good luck with your UI/UX internship scraper!**
