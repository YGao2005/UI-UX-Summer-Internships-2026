# UI/UX Design Internships Tracker 🎨

> Automated Discord bot + job scraper for UI/UX design internship opportunities

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3+-blue.svg)](https://discordpy.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Automatically scrapes UI/UX design internship opportunities from 10+ sources and posts them to Discord. Includes smart filtering, deduplication, and interactive commands.

## Features

- 🔍 **Multi-Source Scraping** - Aggregates from Greenhouse, Lever, Ashby, LinkedIn, Indeed, and more
- 🤖 **Discord Bot** - Interactive commands for browsing, filtering, and searching internships
- 🎯 **Smart Filtering** - Keyword matching specifically tuned for UI/UX design roles
- 🔄 **Deduplication** - Intelligent matching to avoid duplicate postings
- 💾 **Database Integration** - Supabase for persistent storage and tracking
- 📊 **Daily Updates** - Automated scraping via GitHub Actions or cron jobs
- 🎨 **Rich Embeds** - Beautiful Discord formatting with company logos and details

## Quick Start

### Prerequisites

- Python 3.11+
- Discord Bot Token ([Create one here](https://discord.com/developers/applications))
- Supabase Account ([Free tier](https://supabase.com))
- Optional: API keys for additional sources (Adzuna, Jooble, The Muse)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/internship-tracker-bot.git
cd internship-tracker-bot

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### Configuration

Set up your `.env` file:

```bash
# Discord
INTERNSHIP_BOT_TOKEN=your_discord_bot_token
INTERNSHIP_CHANNEL_ID=your_channel_id

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Optional: Enhanced scraping (free API keys)
ADZUNA_APP_ID=your_adzuna_id
ADZUNA_API_KEY=your_adzuna_key
JOOBLE_API_KEY=your_jooble_key
THEMUSE_API_KEY=your_themuse_key
```

### Running the Bot

```bash
# Run Discord bot only
python internship_bot.py

# Run scraper only (one-time)
python src/main.py

# Both (recommended for production)
python launcher.py
```

## Data Sources

### No API Key Required ✅
- **Greenhouse** - 50+ tech companies' career pages
- **Lever** - Direct company job boards
- **Ashby** - Design-focused companies (Notion, OpenAI, Linear, Ramp)
- **RemoteOK** - Remote job aggregator
- **Y Combinator** - Hacker News startup internships

### Optional (Free API Keys) 🔑
- **Adzuna** - Broad coverage aggregator ([Get Key](https://developer.adzuna.com/))
- **Jooble** - Internship-specific aggregator ([Get Key](https://jooble.org/api/about))
- **The Muse** - Internship-focused board ([Get Key](https://www.themuse.com/developers/api/v2))

**Coverage**: Without API keys: 5-15 internships/day | With API keys: 30-100+ internships/day

## Discord Commands

### Browse Internships
- `/today` - View internships posted today
- `/recent` - View last 20 internships
- `/company <name>` - Search by company name
- `/location <city>` - Filter by location

### Interactive Menus
- Select menus for browsing paginated results
- Quick apply links and salary information
- Company details and posting dates

## Scraper Architecture

```
src/
├── scrapers/          # Individual source scrapers
│   ├── greenhouse_scraper.py
│   ├── lever_scraper.py
│   ├── jobspy_scraper.py  # LinkedIn, Indeed, Glassdoor
│   └── ...
├── filters/           # Keyword matching and filtering
├── utils/            # Deduplication, Discord formatting
└── main.py           # Orchestration
```

### Adding New Sources

Create a new scraper in `src/scrapers/`:

```python
class YourScraper:
    async def scrape(self) -> List[dict]:
        jobs = []
        # Your scraping logic
        return jobs
```

Add to `src/main.py`:

```python
from scrapers.your_scraper import YourScraper
scrapers.append(YourScraper())
```

## Database Schema

```sql
CREATE TABLE internships (
  id UUID PRIMARY KEY,
  company TEXT,
  role TEXT,
  location TEXT,
  salary TEXT,
  url TEXT,
  source TEXT,
  posted_date DATE,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Keyword Filtering

Configurable in `data/keywords.yml`:

```yaml
ui_ux_keywords:
  - UI/UX
  - Product Design
  - User Experience
  - Interaction Design
  - Visual Design

exclude_keywords:
  - Full-time
  - Senior
  - Staff
```

## Deployment

### GitHub Actions (Automated Daily Scraping)

```yaml
# .github/workflows/scrape.yml
name: Daily Internship Scraping
on:
  schedule:
    - cron: '0 12 * * *'  # Daily at 12pm UTC
jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run scraper
        run: python src/main.py
```

### Heroku (Discord Bot)

```bash
# Procfile
worker: python internship_bot.py
```

Deploy:
```bash
heroku create your-app-name
git push heroku main
```

## Architecture Modes

This bot supports two deployment modes:

1. **Standalone**: Run independently as a single bot
2. **Multi-Bot Launcher**: Deploy alongside other bots via [discord-bots-launcher](https://github.com/yourusername/discord-bots-launcher) on a single Heroku dyno

## Contributing

Contributions welcome! Ideas:

- Add new scraping sources
- Improve keyword filtering algorithms
- Enhance Discord UX with buttons/modals
- Add email notifications
- Build a web dashboard

## License

MIT License - see [LICENSE](LICENSE) for details

## Disclaimer

Job listings are aggregated from public APIs and company pages. Always verify details on official career pages before applying.

## Attribution

- Remote jobs powered by [RemoteOK](https://remoteok.com)
- LinkedIn data via [JobSpy](https://github.com/Bunsly/JobSpy)

---

**Built for the design community** | [Report Issues](https://github.com/yourusername/internship-tracker-bot/issues) | [Feature Requests](https://github.com/yourusername/internship-tracker-bot/discussions)
