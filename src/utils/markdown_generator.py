"""
Generate markdown README with job listings
"""

import logging
from typing import List, Dict
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import defaultdict

logger = logging.getLogger(__name__)


class MarkdownGenerator:
    """Generates markdown README with job listings"""

    def __init__(self):
        pass

    @staticmethod
    def format_salary(job: Dict) -> str:
        """
        Format salary information for display

        Args:
            job: Job dictionary with salary information

        Returns:
            Formatted salary string or "-" if not available
        """
        # Check for formatted salary string (from JobSpy)
        salary = job.get('salary')
        if salary and isinstance(salary, str) and salary.strip():
            # Remove " USD" suffix to save space
            salary = salary.replace(' USD', '').replace(' usd', '')
            # Add /hr suffix if it looks like hourly rate (under $100)
            if '$' in salary and '-' in salary:
                try:
                    # Extract the max value to determine if hourly
                    max_val = salary.split('-')[-1].strip().replace('$', '').replace(',', '')
                    if float(max_val) < 100:
                        salary += '/hr'
                except (ValueError, IndexError):
                    pass
            return salary

        # Check for separate min/max fields (from Adzuna, RemoteOK)
        salary_min = job.get('salary_min')
        salary_max = job.get('salary_max')

        if salary_min or salary_max:
            # If both are the same, just show one value
            if salary_min == salary_max and salary_min:
                amount = int(salary_min)
                # Detect if annual (>$1000) or hourly (<$100)
                if amount > 1000:
                    return f"${amount:,}/yr"
                else:
                    return f"${amount}/hr"

            # Different min/max - show range
            parts = []
            if salary_min:
                parts.append(f"${int(salary_min):,}")
            if salary_max:
                parts.append(f"${int(salary_max):,}")

            if parts:
                range_str = ' - '.join(parts)
                # Detect if this looks like annual salary
                try:
                    max_val = int(salary_max) if salary_max else int(salary_min)
                    if max_val > 1000:
                        return f"{range_str}/yr"
                    else:
                        return f"{range_str}/hr"
                except (ValueError, TypeError):
                    return range_str

        return '-'

    @staticmethod
    def format_relative_date(posted_date: str) -> str:
        """
        Convert ISO date string to relative time format

        Args:
            posted_date: ISO format date string (e.g., '2025-11-05')

        Returns:
            Relative time string (e.g., '5d ago', '2w ago', '3mo ago')
        """
        if not posted_date:
            return 'Unknown'

        try:
            # Parse the posted date (handle various formats)
            if 'T' in posted_date:
                # ISO format with time: '2025-11-05T12:00:00'
                posted = datetime.fromisoformat(posted_date.replace('Z', '+00:00'))
                # Convert to naive datetime for comparison
                if posted.tzinfo is not None:
                    posted = posted.replace(tzinfo=None)
            else:
                # Date only: '2025-11-05'
                posted = datetime.strptime(posted_date[:10], '%Y-%m-%d')

            # Calculate time difference
            now = datetime.now()
            diff = now - posted

            # Handle future dates (edge case)
            if diff.days < 0:
                return 'Just posted'

            # Format based on time difference
            if diff.days == 0:
                return 'Today'
            elif diff.days == 1:
                return '1d ago'
            elif diff.days < 7:
                return f'{diff.days}d ago'
            elif diff.days < 30:
                weeks = diff.days // 7
                return f'{weeks}w ago'
            elif diff.days < 365:
                months = diff.days // 30
                return f'{months}mo ago'
            else:
                years = diff.days // 365
                return f'{years}y ago'

        except (ValueError, AttributeError) as e:
            logger.warning(f"Failed to parse date '{posted_date}': {e}")
            return 'Unknown'

    def generate_readme(self, jobs: List[Dict], stats: Dict = None) -> str:
        """
        Generate complete README markdown

        Args:
            jobs: List of filtered, deduplicated jobs
            stats: Optional statistics dictionary

        Returns:
            Markdown string
        """
        now_pt = datetime.now(ZoneInfo("America/Los_Angeles"))
        now = now_pt.strftime("%Y-%m-%d %I:%M %p PT")

        # Calculate statistics
        total_jobs = len(jobs)
        companies = set(job['company'] for job in jobs)
        remote_jobs = [j for j in jobs if 'remote' in j.get('location', '').lower()]

        # Calculate "new this week" count (jobs posted in last 7 days)
        new_this_week = 0
        for job in jobs:
            posted_date = job.get('posted_date', '')
            if posted_date:
                try:
                    if 'T' in posted_date:
                        posted = datetime.fromisoformat(posted_date.replace('Z', '+00:00'))
                        # Convert to naive datetime for comparison
                        if posted.tzinfo is not None:
                            posted = posted.replace(tzinfo=None)
                    else:
                        posted = datetime.strptime(posted_date[:10], '%Y-%m-%d')

                    days_ago = (datetime.now() - posted).days
                    if days_ago <= 7:
                        new_this_week += 1
                except (ValueError, AttributeError):
                    pass

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
| New This Week | {new_this_week} |
| Companies Hiring | {len(companies)} |
| Remote Opportunities | {len(remote_jobs)} |

---

## All Internships

| Company | Role | Location | Salary | Posted | Source | Apply |
|---------|------|----------|--------|--------|--------|-------|
"""

        # Add all jobs to table, sorted by date (newest first)
        sorted_jobs = sorted(jobs, key=lambda x: x.get('posted_date', ''), reverse=True)

        for job in sorted_jobs:
            company = job.get('company', 'Unknown')
            title = job.get('title', 'Untitled')
            location = job.get('location', 'N/A')
            posted_date = job.get('posted_date', '')
            source = job.get('source', 'Unknown')
            url = job.get('url', '#')

            # Format the relative date and salary
            relative_date = self.format_relative_date(posted_date)
            salary = self.format_salary(job)

            # Truncate long titles
            if len(title) > 50:
                title = title[:47] + "..."

            # Truncate long locations
            if len(location) > 30:
                location = location[:27] + "..."

            md += f"| {company} | {title} | {location} | {salary} | {relative_date} | {source} | [Apply]({url}) |\n"

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
