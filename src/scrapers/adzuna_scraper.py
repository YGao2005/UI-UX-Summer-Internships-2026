"""
Adzuna scraper - Broad coverage job aggregator
Free tier: 1,000 calls/month (requires app ID and key)
"""

import os
import requests
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class AdzunaScraper:
    """Scraper for Adzuna API"""

    BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/{page}"

    def __init__(self, app_id: str = None, app_key: str = None):
        """
        Initialize scraper with Adzuna credentials

        Args:
            app_id: Adzuna app ID. If None, reads from ADZUNA_APP_ID env var
            app_key: Adzuna app key. If None, reads from ADZUNA_APP_KEY env var
        """
        self.app_id = app_id or os.getenv('ADZUNA_APP_ID')
        self.app_key = app_key or os.getenv('ADZUNA_APP_KEY')

        if not self.app_id or not self.app_key:
            logger.warning("Adzuna credentials not provided - skipping this source")

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'UI-UX-Internship-Tracker/1.0 (Educational Project)'
        })

    def fetch_jobs(self, query: str = 'UI UX design intern', results_per_page: int = 50) -> List[Dict]:
        """
        Fetch jobs from Adzuna

        Args:
            query: Search query
            results_per_page: Number of results per page (max 50)

        Returns:
            List of standardized job dictionaries
        """
        if not self.app_id or not self.app_key:
            logger.info("⊘ Adzuna: Skipping (no API credentials)")
            return []

        params = {
            'app_id': self.app_id,
            'app_key': self.app_key,
            'what': query,
            'results_per_page': min(results_per_page, 50),
            'content-type': 'application/json'
        }

        all_jobs = []
        max_pages = 2  # Limit to 2 pages (100 jobs) to conserve API quota

        try:
            for page in range(1, max_pages + 1):
                url = self.BASE_URL.format(page=page)

                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                results = data.get('results', [])

                if not results:
                    break  # No more results

                all_jobs.extend(results)

                # Check if we've reached the end
                count = data.get('count', 0)
                if len(all_jobs) >= count:
                    break

            logger.info(f"✓ Adzuna: {len(all_jobs)} jobs found for '{query}'")

            # Convert to standardized format
            return [self._normalize_job(job) for job in all_jobs]

        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Adzuna: Request failed: {str(e)}")
            return []

    def _normalize_job(self, job: Dict) -> Dict:
        """Convert Adzuna job format to standardized format"""

        # Extract company
        company = job.get('company', {}).get('display_name', 'Unknown')

        # Extract location
        location_raw = job.get('location', {})
        location_parts = []
        if location_raw.get('area'):
            location_parts.extend(location_raw['area'])
        if location_parts:
            location = ', '.join(location_parts)
        else:
            location = 'Remote'

        # Extract date (Adzuna uses ISO format)
        created = job.get('created', datetime.now().isoformat())

        # Build redirect URL (Adzuna uses redirects)
        job_url = job.get('redirect_url', '')

        # Extract salary info
        salary_min = job.get('salary_min')
        salary_max = job.get('salary_max')

        return {
            'id': f"adzuna_{job.get('id')}",
            'title': job.get('title', ''),
            'company': company,
            'location': location,
            'url': job_url,
            'description': job.get('description', ''),
            'posted_date': created,
            'source': 'Adzuna',
            'salary_min': salary_min,
            'salary_max': salary_max,
            'contract_type': job.get('contract_type'),
            'raw_data': job
        }


if __name__ == "__main__":
    # Test the scraper
    logging.basicConfig(level=logging.INFO)

    # Test with credentials from environment
    scraper = AdzunaScraper()

    if scraper.app_id and scraper.app_key:
        # Fetch UI/UX design internships
        jobs = scraper.fetch_jobs(query='UI UX design intern')
        print(f"\nTotal jobs found: {len(jobs)}")

        # Show a few sample jobs
        for job in jobs[:3]:
            print(f"\n  Company: {job['company']}")
            print(f"  Title: {job['title']}")
            print(f"  Location: {job['location']}")
            print(f"  URL: {job['url'][:80]}...")
    else:
        print("Set ADZUNA_APP_ID and ADZUNA_APP_KEY environment variables to test")
