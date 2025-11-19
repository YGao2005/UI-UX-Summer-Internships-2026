"""
Lever scraper - No authentication required for public job boards
Used by: Netflix, Shopify, IDEO, Stripe (some divisions), and many more
"""

import requests
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class LeverScraper:
    """Scraper for Lever ATS public API"""

    BASE_URL = "https://api.lever.co/v0/postings/{company}"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'UI-UX-Internship-Tracker/1.0 (Educational Project)'
        })

    def fetch_company_jobs(self, company_handle: str, company_name: str) -> List[Dict]:
        """
        Fetch all jobs from a company's Lever board

        Args:
            company_handle: The company's Lever handle (e.g., 'shopify')
            company_name: The company's display name

        Returns:
            List of standardized job dictionaries
        """
        url = self.BASE_URL.format(company=company_handle)

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            jobs = response.json()

            logger.info(f"✓ Lever: {company_name} - {len(jobs)} jobs found")

            # Convert to standardized format
            return [self._normalize_job(job, company_name) for job in jobs]

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"✗ Lever: {company_name} - Not found (check handle)")
            else:
                logger.error(f"✗ Lever: {company_name} - HTTP {e.response.status_code}")
            return []

        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Lever: {company_name} - Request failed: {str(e)}")
            return []

    def _normalize_job(self, job: Dict, company_name: str) -> Dict:
        """Convert Lever job format to standardized format"""

        # Extract location
        location = job.get('categories', {}).get('location', 'Remote')
        if not location:
            location = 'Remote'

        # Extract team/department
        team = job.get('categories', {}).get('team', '')
        commitment = job.get('categories', {}).get('commitment', '')

        # Combine description fields
        description_html = job.get('description', '')
        additional_html = job.get('additional', '')
        full_description = f"{description_html}\n\n{additional_html}"

        return {
            'id': f"lever_{job.get('id')}",
            'title': job.get('text', ''),
            'company': company_name,
            'location': location,
            'url': job.get('hostedUrl', ''),
            'description': full_description,
            'posted_date': job.get('createdAt', datetime.now().isoformat()),
            'source': 'Lever',
            'team': team,
            'commitment': commitment,
            'raw_data': job
        }

    def fetch_multiple_companies(self, companies: List[Dict]) -> List[Dict]:
        """
        Fetch jobs from multiple companies

        Args:
            companies: List of dicts with 'name' and 'lever' keys

        Returns:
            Combined list of all jobs from all companies
        """
        all_jobs = []

        lever_companies = [c for c in companies if 'lever' in c]
        logger.info(f"Fetching from {len(lever_companies)} Lever companies...")

        for company in lever_companies:
            jobs = self.fetch_company_jobs(
                company_handle=company['lever'],
                company_name=company['name']
            )
            all_jobs.extend(jobs)

        return all_jobs


if __name__ == "__main__":
    # Test the scraper
    logging.basicConfig(level=logging.INFO)

    scraper = LeverScraper()

    # Test with a few companies
    test_companies = [
        {'name': 'Shopify', 'lever': 'shopify'},
        {'name': 'IDEO', 'lever': 'ideo'},
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
