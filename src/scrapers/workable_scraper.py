"""
Workable scraper - No authentication required for public job boards
Used by many companies including Revolut, Delivery Hero, and others
Public API: https://apply.workable.com/api/v1/widget/accounts/{company}
"""

import requests
import logging
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class WorkableScraper:
    """Scraper for Workable ATS public API"""

    BASE_URL = "https://apply.workable.com/api/v1/widget/accounts/{company}"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'UI-UX-Internship-Tracker/1.0 (Educational Project)',
            'Accept': 'application/json'
        })

    def fetch_company_jobs(self, company_handle: str, company_name: str) -> List[Dict]:
        """
        Fetch all jobs from a company's Workable board

        Args:
            company_handle: The company's Workable handle (e.g., 'revolut')
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

            logger.info(f"✓ Workable: {company_name} - {len(jobs)} jobs found")

            # Convert to standardized format
            return [self._normalize_job(job, company_name) for job in jobs]

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"✗ Workable: {company_name} - Not found (check handle)")
            else:
                logger.error(f"✗ Workable: {company_name} - HTTP {e.response.status_code}")
            return []

        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Workable: {company_name} - Request failed: {str(e)}")
            return []

    def _normalize_job(self, job: Dict, company_name: str) -> Dict:
        """Convert Workable job format to standardized format"""

        # Extract location
        location = job.get('city', '')
        if not location:
            location = job.get('country', 'Remote')

        # Combine city and country if both exist
        if job.get('city') and job.get('country'):
            location = f"{job['city']}, {job['country']}"

        # Extract department
        department = job.get('department', '')

        # Build job URL
        job_url = job.get('url', '')
        if not job_url and job.get('shortcode'):
            job_url = f"https://apply.workable.com/{job.get('account_name')}/j/{job['shortcode']}/"

        return {
            'id': f"workable_{job.get('shortcode', abs(hash(job_url)))}",
            'title': job.get('title', ''),
            'company': company_name,
            'location': location,
            'url': job_url,
            'description': job.get('description', ''),
            'posted_date': job.get('created_at', datetime.now().isoformat()),
            'source': 'Workable',
            'department': department,
            'employment_type': job.get('employment_type'),
            'raw_data': job
        }

    def fetch_multiple_companies(self, companies: List[Dict]) -> List[Dict]:
        """
        Fetch jobs from multiple companies

        Args:
            companies: List of dicts with 'name' and 'workable' keys

        Returns:
            Combined list of all jobs from all companies
        """
        all_jobs = []

        workable_companies = [c for c in companies if 'workable' in c]
        logger.info(f"Fetching from {len(workable_companies)} Workable companies...")

        for company in workable_companies:
            jobs = self.fetch_company_jobs(
                company_handle=company['workable'],
                company_name=company['name']
            )
            all_jobs.extend(jobs)

        return all_jobs


if __name__ == "__main__":
    # Test the scraper
    logging.basicConfig(level=logging.INFO)

    scraper = WorkableScraper()

    # Test with a company known to use Workable
    test_companies = [
        {'name': 'Revolut', 'workable': 'revolut'},
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
