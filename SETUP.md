# UI/UX Internship Scraper - Setup Guide

This is an automated job scraper that collects UI/UX design internships from multiple sources and updates a GitHub repository daily.

## Features

- Completely free (uses GitHub Actions)
- Scrapes from 4+ sources without authentication
- Smart filtering with keyword scoring
- Automatic deduplication
- Daily updates via GitHub Actions
- Clean markdown output

## Quick Start

### 1. Local Setup

```bash
# Clone the repository
git clone https://github.com/your-username/ui-ux-internships-2025.git
cd ui-ux-internships-2025

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the scraper
python src/main.py
```

### 2. GitHub Setup

1. **Fork or create a new repository** on GitHub

2. **Push this code** to your repository:
```bash
git init
git add .
git commit -m "Initial commit: UI/UX internship scraper"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ui-ux-internships-2025.git
git push -u origin main
```

3. **Enable GitHub Actions**:
   - Go to your repo → Settings → Actions → General
   - Under "Workflow permissions", select "Read and write permissions"
   - Click "Save"

4. **Test the workflow**:
   - Go to Actions tab
   - Click "Update Job Listings"
   - Click "Run workflow"

### 3. Customization

#### Add/Remove Companies

Edit `data/companies.yml`:

```yaml
companies:
  - name: "Your Company"
    greenhouse: "company-handle"  # or lever/ashby
```

To find company handles:
- **Greenhouse**: Visit `company.com/careers` → View source → Search for "greenhouse"
- **Lever**: Visit `company.com/careers` → Check URL pattern
- **Ashby**: Visit `company.com/careers` → Check URL pattern

#### Adjust Filtering

Edit `data/keywords.yml` to customize:
- Title keywords (what to include/exclude)
- Description keywords (tools and skills)
- Minimum relevance score threshold

## Data Sources

### No Authentication Required

1. **Greenhouse** - Direct company APIs
   - Used by: Figma, Stripe, Airbnb, Spotify
   - Rate limit: Unlimited for public boards

2. **Lever** - Direct company APIs
   - Used by: Netflix, Shopify, IDEO
   - Rate limit: Unlimited for public boards

3. **Ashby** - Direct company APIs
   - Used by: Notion, OpenAI, Anthropic, Linear
   - Rate limit: Unlimited for public boards

4. **RemoteOK** - Remote job aggregator
   - 30,000+ jobs updated frequently
   - Rate limit: Reasonable use
   - **Requires attribution** (automatically included in README)

## Project Structure

```
ui-ux-internships-2025/
├── .github/workflows/
│   └── update_jobs.yml          # GitHub Actions automation
├── src/
│   ├── scrapers/
│   │   ├── greenhouse_scraper.py
│   │   ├── lever_scraper.py
│   │   ├── ashby_scraper.py
│   │   └── remoteok_scraper.py
│   ├── filters/
│   │   └── keyword_filter.py    # Smart filtering logic
│   ├── utils/
│   │   ├── deduplicator.py      # Remove duplicates
│   │   └── markdown_generator.py
│   └── main.py                  # Main orchestrator
├── data/
│   ├── companies.yml            # Companies to track
│   ├── keywords.yml             # Filter configuration
│   └── jobs.json               # Cached job data
├── README.md                    # Auto-generated job list
└── requirements.txt
```

## How It Works

### Daily Automation Flow

1. **GitHub Actions triggers** at midnight UTC
2. **Scrapes jobs** from all sources (~200 API calls)
3. **Filters** for UI/UX internships using keyword scoring
4. **Deduplicates** jobs across sources
5. **Generates README** with formatted job table
6. **Commits changes** if new jobs found

### Filtering Algorithm

Jobs are scored based on:
- **Title keywords** (+3 points each for relevant, -10 for excluded)
- **Description keywords** (+1 point each for tools/skills)
- **Minimum threshold**: 3 points to be included

Example:
- "UX Design Intern" with "Figma" in description = 3 + 1 = 4 points ✓
- "Graphic Design Intern" = 0 points ✗

## Troubleshooting

### Scraper isn't running

1. Check GitHub Actions permissions (Settings → Actions)
2. View logs in Actions tab for error messages
3. Ensure `requirements.txt` dependencies are correct

### No jobs found

1. Verify company handles in `data/companies.yml`
2. Test scrapers individually:
   ```bash
   python src/scrapers/greenhouse_scraper.py
   ```
3. Check if filtering is too strict in `data/keywords.yml`

### Rate limiting

The free sources should never hit rate limits with daily scraping. If you add more frequent updates:
- RemoteOK: Add delays between requests
- Company APIs: Spread requests over time

## Adding More Sources (Future)

### With API Keys (Optional)

Edit `requirements.txt` and `src/main.py` to add:

1. **The Muse API** (3,600 req/hour free)
2. **Adzuna API** (1,000 req/month free)
3. **JSearch via RapidAPI** (aggregates LinkedIn/Indeed)

## Legal & Ethical

- All sources are public APIs or job boards
- Rate limiting is implemented
- Attribution provided (RemoteOK)
- No personal data collected
- Disclaimer in README

## Contributing

1. Fork the repository
2. Add companies to `data/companies.yml`
3. Submit a pull request

## Cost

**$0/month** - Everything runs on free tiers:
- GitHub Actions: 2,000 minutes/month free
- All APIs: No authentication or free tier
- Hosting: GitHub Pages (optional)

## License

MIT License - Feel free to use and modify!

---

**Questions?** Open an issue on GitHub!
