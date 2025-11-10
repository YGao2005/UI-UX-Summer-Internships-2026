"""
Greenhouse scraper - No authentication required for public job boards
Used by: Airbnb, Spotify, Pinterest, Figma, Stripe, and many more
"""

import requests
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class GreenhouseScraper:
    """Scraper for Greenhouse ATS public API"""

    BASE_URL = "https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'UI-UX-Internship-Tracker/1.0 (Educational Project)'
        })

    def fetch_company_jobs(self, company_handle: str, company_name: str) -> List[Dict]:
        """
        Fetch all jobs from a company's Greenhouse board

        Args:
            company_handle: The company's Greenhouse handle (e.g., 'airbnb')
            company_name: The company's display name

        Returns:
            List of standardized job dictionaries
        """
        url = self.BASE_URL.format(company=company_handle)

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            jobs = data.get('jobs', [])

            logger.info(f"✓ Greenhouse: {company_name} - {len(jobs)} jobs found")

            # Convert to standardized format
            return [self._normalize_job(job, company_name) for job in jobs]

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"✗ Greenhouse: {company_name} - Not found (check handle)")
            else:
                logger.error(f"✗ Greenhouse: {company_name} - HTTP {e.response.status_code}")
            return []

        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Greenhouse: {company_name} - Request failed: {str(e)}")
            return []

    def _normalize_job(self, job: Dict, company_name: str) -> Dict:
        """Convert Greenhouse job format to standardized format"""

        # Extract location
        location = job.get('location', {}).get('name', 'Remote')

        # Extract departments
        departments = [dept.get('name', '') for dept in job.get('departments', [])]

        return {
            'id': f"greenhouse_{job.get('id')}",
            'title': job.get('title', ''),
            'company': company_name,
            'location': location,
            'url': job.get('absolute_url', ''),
            'description': job.get('content', ''),
            'posted_date': job.get('updated_at', datetime.now().isoformat()),
            'source': 'Greenhouse',
            'departments': departments,
            'raw_data': job
        }

    def fetch_multiple_companies(self, companies: List[Dict]) -> List[Dict]:
        """
        Fetch jobs from multiple companies

        Args:
            companies: List of dicts with 'name' and 'greenhouse' keys

        Returns:
            Combined list of all jobs from all companies
        """
        all_jobs = []

        greenhouse_companies = [c for c in companies if 'greenhouse' in c]
        logger.info(f"Fetching from {len(greenhouse_companies)} Greenhouse companies...")

        for company in greenhouse_companies:
            jobs = self.fetch_company_jobs(
                company_handle=company['greenhouse'],
                company_name=company['name']
            )
            all_jobs.extend(jobs)

        return all_jobs


if __name__ == "__main__":
    # Test the scraper
    logging.basicConfig(level=logging.INFO)

    scraper = GreenhouseScraper()

    # Test with a few companies
    test_companies = [
        {'name': 'Figma', 'greenhouse': 'figma'},
        {'name': 'Stripe', 'greenhouse': 'stripe'},
        {'name': 'Airbnb', 'greenhouse': 'airbnb'}
    ]

    jobs = scraper.fetch_multiple_companies(test_companies)
    print(f"\nTotal jobs found: {len(jobs)}")

    # Show a sample job
    if jobs:
        sample = jobs[0]
        print(f"\nSample job:")
        print(f"  Company: {sample['company']}")
        print(f"  Title: {sample['title']}")
        print(f"  Location: {sample['location']}")
        print(f"  URL: {sample['url']}")
