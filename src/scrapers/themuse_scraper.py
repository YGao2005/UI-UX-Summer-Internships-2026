"""
The Muse scraper - Best for internships with explicit category filter
Free tier: 3,600 requests/hour (requires API key)
"""

import os
import requests
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class TheMuseScraper:
    """Scraper for The Muse API"""

    BASE_URL = "https://www.themuse.com/api/public/jobs"

    def __init__(self, api_key: str = None):
        """
        Initialize scraper with API key

        Args:
            api_key: The Muse API key. If None, reads from THEMUSE_API_KEY env var
        """
        self.api_key = api_key or os.getenv('THEMUSE_API_KEY')
        if not self.api_key:
            logger.warning("The Muse API key not provided - skipping this source")

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'UI-UX-Internship-Tracker/1.0 (Educational Project)'
        })

    def fetch_jobs(self, category: str = 'Design', level: str = 'Internship', page_size: int = 20) -> List[Dict]:
        """
        Fetch jobs from The Muse

        Args:
            category: Job category (e.g., 'Design', 'UX', 'Product')
            level: Experience level ('Internship', 'Entry Level', etc.)
            page_size: Number of results per page (max 20)

        Returns:
            List of standardized job dictionaries
        """
        if not self.api_key:
            logger.info("⊘ The Muse: Skipping (no API key)")
            return []

        params = {
            'category': category,
            'level': level,
            'page': 0,
            'descending': 'true',
            'api_key': self.api_key
        }

        all_jobs = []
        max_pages = 5  # Limit to 5 pages (100 jobs) to avoid excessive API calls

        try:
            for page in range(max_pages):
                params['page'] = page

                response = self.session.get(self.BASE_URL, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                results = data.get('results', [])

                if not results:
                    break  # No more results

                all_jobs.extend(results)

                # Check if there are more pages
                page_count = data.get('page_count', 0)
                if page >= page_count - 1:
                    break

            logger.info(f"✓ The Muse: {len(all_jobs)} {category} {level} jobs found")

            # Convert to standardized format
            return [self._normalize_job(job) for job in all_jobs]

        except requests.exceptions.RequestException as e:
            logger.error(f"✗ The Muse: Request failed: {str(e)}")
            return []

    def _normalize_job(self, job: Dict) -> Dict:
        """Convert The Muse job format to standardized format"""

        # Extract company info
        company_info = job.get('company', {})
        company_name = company_info.get('name', 'Unknown')

        # Extract locations
        locations = job.get('locations', [])
        if locations:
            location = ', '.join([loc.get('name', '') for loc in locations])
        else:
            location = 'Remote'

        # Extract publication date
        publication_date = job.get('publication_date', datetime.now().isoformat())

        # Build job URL
        job_url = job.get('refs', {}).get('landing_page', '')

        # Extract categories
        categories = [cat.get('name', '') for cat in job.get('categories', [])]

        # Extract levels
        levels = [lvl.get('name', '') for lvl in job.get('levels', [])]

        return {
            'id': f"themuse_{job.get('id')}",
            'title': job.get('name', ''),
            'company': company_name,
            'location': location,
            'url': job_url,
            'description': job.get('contents', ''),
            'posted_date': publication_date,
            'source': 'TheMuse',
            'categories': categories,
            'levels': levels,
            'raw_data': job
        }


if __name__ == "__main__":
    # Test the scraper
    logging.basicConfig(level=logging.INFO)

    # Test with API key from environment
    scraper = TheMuseScraper()

    if scraper.api_key:
        # Fetch design internships
        jobs = scraper.fetch_jobs(category='Design', level='Internship')
        print(f"\nTotal design internships found: {len(jobs)}")

        # Show a few sample jobs
        for job in jobs[:3]:
            print(f"\n  Company: {job['company']}")
            print(f"  Title: {job['title']}")
            print(f"  Location: {job['location']}")
            print(f"  URL: {job['url']}")
    else:
        print("Set THEMUSE_API_KEY environment variable to test")
