"""
Jooble scraper - Job aggregator with explicit internship category
Free tier: Rate limits TBD (requires API key)
"""

import os
import requests
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class JoobleScraper:
    """Scraper for Jooble API"""

    BASE_URL = "https://api.jooble.org/api"

    def __init__(self, api_key: str = None):
        """
        Initialize scraper with API key

        Args:
            api_key: Jooble API key. If None, reads from JOOBLE_API_KEY env var
        """
        self.api_key = api_key or os.getenv('JOOBLE_API_KEY')
        if not self.api_key:
            logger.warning("Jooble API key not provided - skipping this source")

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'UI-UX-Internship-Tracker/1.0 (Educational Project)',
            'Content-Type': 'application/json'
        })

    def fetch_jobs(self, keywords: str = 'UI UX design intern', page: int = 1) -> List[Dict]:
        """
        Fetch jobs from Jooble

        Args:
            keywords: Search keywords
            page: Page number (starts at 1)

        Returns:
            List of standardized job dictionaries
        """
        if not self.api_key:
            logger.info("⊘ Jooble: Skipping (no API key)")
            return []

        # Jooble API endpoint includes the API key in the URL
        url = f"{self.BASE_URL}/{self.api_key}"

        # Jooble uses POST with JSON body for search
        payload = {
            "keywords": keywords,
            "page": str(page)
        }

        try:
            response = self.session.post(url, json=payload, timeout=10)
            response.raise_for_status()

            data = response.json()
            jobs = data.get('jobs', [])

            logger.info(f"✓ Jooble: {len(jobs)} jobs found for '{keywords}'")

            # Convert to standardized format
            return [self._normalize_job(job) for job in jobs]

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.error(f"✗ Jooble: Unauthorized - check API key")
            else:
                logger.error(f"✗ Jooble: HTTP {e.response.status_code}")
            return []

        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Jooble: Request failed: {str(e)}")
            return []

    def _normalize_job(self, job: Dict) -> Dict:
        """Convert Jooble job format to standardized format"""

        # Extract company
        company = job.get('company', 'Unknown')

        # Extract location
        location = job.get('location', 'Remote')
        if not location:
            location = 'Remote'

        # Extract date (Jooble provides updated date)
        updated = job.get('updated', datetime.now().isoformat())

        # Job URL
        job_url = job.get('link', '')

        # Salary info (if available)
        salary = job.get('salary', '')

        # Source info
        source_info = job.get('source', '')

        return {
            'id': f"jooble_{job.get('id', hash(job_url))}",
            'title': job.get('title', ''),
            'company': company,
            'location': location,
            'url': job_url,
            'description': job.get('snippet', ''),  # Jooble provides snippet, not full description
            'posted_date': updated,
            'source': 'Jooble',
            'salary': salary,
            'source_site': source_info,
            'raw_data': job
        }


if __name__ == "__main__":
    # Test the scraper
    logging.basicConfig(level=logging.INFO)

    # Test with API key from environment
    scraper = JoobleScraper()

    if scraper.api_key:
        # Fetch UI/UX design internships
        jobs = scraper.fetch_jobs(keywords='UI UX design intern')
        print(f"\nTotal jobs found: {len(jobs)}")

        # Show a few sample jobs
        for job in jobs[:3]:
            print(f"\n  Company: {job['company']}")
            print(f"  Title: {job['title']}")
            print(f"  Location: {job['location']}")
            print(f"  URL: {job['url'][:80]}..." if len(job['url']) > 80 else f"  URL: {job['url']}")
    else:
        print("Set JOOBLE_API_KEY environment variable to test")
