"""
Generate markdown README with job listings
"""

import logging
from typing import List, Dict
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class MarkdownGenerator:
    """Generates markdown README with job listings"""

    def __init__(self):
        pass

    def generate_readme(self, jobs: List[Dict], stats: Dict = None) -> str:
        """
        Generate complete README markdown

        Args:
            jobs: List of filtered, deduplicated jobs
            stats: Optional statistics dictionary

        Returns:
            Markdown string
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

        # Calculate statistics
        total_jobs = len(jobs)
        companies = set(job['company'] for job in jobs)
        remote_jobs = [j for j in jobs if 'remote' in j.get('location', '').lower()]

        # Group jobs by company
        jobs_by_company = defaultdict(list)
        for job in jobs:
            jobs_by_company[job['company']].append(job)

        # Start markdown
        md = f"""# UI/UX Design Internships 2025

> Curated list of UI/UX design internships, updated daily via automated scraping.

**Last Updated:** {now}

## Quick Stats

| Metric | Count |
|--------|-------|
| Total Internships | {total_jobs} |
| Companies Hiring | {len(companies)} |
| Remote Opportunities | {len(remote_jobs)} |

---

## All Internships

| Company | Role | Location | Source | Apply |
|---------|------|----------|--------|-------|
"""

        # Add all jobs to table, sorted by date (newest first)
        sorted_jobs = sorted(jobs, key=lambda x: x.get('posted_date', ''), reverse=True)

        for job in sorted_jobs:
            company = job.get('company', 'Unknown')
            title = job.get('title', 'Untitled')
            location = job.get('location', 'N/A')
            source = job.get('source', 'Unknown')
            url = job.get('url', '#')

            # Truncate long titles
            if len(title) > 50:
                title = title[:47] + "..."

            # Truncate long locations
            if len(location) > 30:
                location = location[:27] + "..."

            md += f"| {company} | {title} | {location} | {source} | [Apply]({url}) |\n"

        # Add companies section
        md += "\n---\n\n"
        md += "## Companies Currently Hiring\n\n"

        for company in sorted(jobs_by_company.keys()):
            job_count = len(jobs_by_company[company])
            md += f"- **{company}** ({job_count} {'position' if job_count == 1 else 'positions'})\n"

        # Add footer
        md += """
---

## About This Repo

This repository is automatically updated daily using GitHub Actions. Jobs are aggregated from multiple sources:

### Active Sources (No API Key Required)
- **Greenhouse** - Direct company job boards (50+ tech companies)
- **Lever** - Direct company job boards
- **Ashby** - Direct company job boards (design-focused: Notion, OpenAI, Linear, Ramp)
- **RemoteOK** - Remote job aggregator
- **Y Combinator** - Hacker News job board (startup internships)

### Additional Sources (Require Free API Keys)
- **The Muse** - Internship-focused job board with design category ([Get API Key](https://www.themuse.com/developers/api/v2))
- **Adzuna** - Broad coverage job search aggregator ([Get API Key](https://developer.adzuna.com/))
- **Jooble** - Job aggregator with explicit internship category ([Get API Key](https://jooble.org/api/about))

See `.env.example` for setup instructions. Without API keys, the scraper still finds 5-15 internships. With API keys: 30-100+ internships.

All listings are filtered for UI/UX design internship relevance using keyword matching and scoring algorithms.

### Data Sources

Jobs are collected from public APIs and company career pages. This repo provides:
- Zero-cost automation via GitHub Actions
- Smart filtering for UI/UX internships specifically
- Deduplication across multiple sources
- Daily updates

### Contributing

Found a great company we should track? Submit a PR adding them to `data/companies.yml`!

### Disclaimer

This is an automated aggregator. Always verify details on the company's official career page before applying. Job listings may be outdated or contain errors.

### Attribution

Remote jobs powered by [RemoteOK](https://remoteok.com) - the largest remote job board.

---

**Built with Python & GitHub Actions** | [Report Issues](https://github.com/your-username/ui-ux-internships-2025/issues)
"""

        return md

    def generate_jobs_by_location(self, jobs: List[Dict]) -> str:
        """
        Generate markdown grouped by location

        Args:
            jobs: List of jobs

        Returns:
            Markdown string
        """
        md = "## Internships by Location\n\n"

        # Group by location
        by_location = defaultdict(list)
        for job in jobs:
            location = job.get('location', 'Unknown')
            by_location[location].append(job)

        # Sort locations (Remote first, then alphabetically)
        locations = sorted(by_location.keys(), key=lambda x: (
            0 if 'remote' in x.lower() else 1,
            x
        ))

        for location in locations:
            job_list = by_location[location]
            md += f"\n### {location} ({len(job_list)})\n\n"

            for job in sorted(job_list, key=lambda x: x['company']):
                md += f"- **{job['company']}** - {job['title']} | [Apply]({job['url']})\n"

        return md


if __name__ == "__main__":
    # Test the generator
    test_jobs = [
        {
            'company': 'Figma',
            'title': 'Product Design Intern',
            'location': 'San Francisco, CA',
            'url': 'https://figma.com/careers/12345',
            'source': 'Greenhouse'
        },
        {
            'company': 'Stripe',
            'title': 'UX Research Intern',
            'location': 'Remote',
            'url': 'https://stripe.com/jobs/12345',
            'source': 'Greenhouse'
        },
        {
            'company': 'Notion',
            'title': 'Design Intern',
            'location': 'San Francisco, CA / New York, NY',
            'url': 'https://notion.so/careers/12345',
            'source': 'Ashby'
        }
    ]

    generator = MarkdownGenerator()
    readme = generator.generate_readme(test_jobs)

    print(readme)
    print("\n" + "="*80 + "\n")

    location_section = generator.generate_jobs_by_location(test_jobs)
    print(location_section)
