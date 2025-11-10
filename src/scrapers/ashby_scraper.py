"""
Ashby scraper - No authentication required for public job boards
Used by: Notion, OpenAI, Anthropic, Scale AI, Ramp, Linear (modern design-focused companies!)
"""

import requests
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class AshbyScraper:
    """Scraper for Ashby ATS public API"""

    BASE_URL = "https://api.ashbyhq.com/posting-api/job-board/{company}"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'UI-UX-Internship-Tracker/1.0 (Educational Project)'
        })

    def fetch_company_jobs(self, company_handle: str, company_name: str) -> List[Dict]:
        """
        Fetch all jobs from a company's Ashby board

        Args:
            company_handle: The company's Ashby handle (e.g., 'notion')
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

            logger.info(f"✓ Ashby: {company_name} - {len(jobs)} jobs found")

            # Convert to standardized format
            return [self._normalize_job(job, company_name) for job in jobs]

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"✗ Ashby: {company_name} - Not found (check handle)")
            else:
                logger.error(f"✗ Ashby: {company_name} - HTTP {e.response.status_code}")
            return []

        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Ashby: {company_name} - Request failed: {str(e)}")
            return []

    def _normalize_job(self, job: Dict, company_name: str) -> Dict:
        """Convert Ashby job format to standardized format"""

        # Extract location (handle both string and dict formats)
        location_raw = job.get('location', 'Remote')
        if isinstance(location_raw, dict):
            location = location_raw.get('name', 'Remote')
        elif isinstance(location_raw, str):
            location = location_raw
        else:
            location = 'Remote'

        if not location:
            location = 'Remote'

        # Extract department/team (handle both string and dict formats)
        department_raw = job.get('department', '')
        if isinstance(department_raw, dict):
            department = department_raw.get('name', '')
        elif isinstance(department_raw, str):
            department = department_raw
        else:
            department = ''

        # Get job description
        description = job.get('descriptionHtml', '') or job.get('description', '')

        # Build job URL
        job_id = job.get('id', '')
        job_url = f"https://jobs.ashbyhq.com/{company_name.lower().replace(' ', '-')}/{job_id}"
        if 'jobUrl' in job:
            job_url = job['jobUrl']

        return {
            'id': f"ashby_{job.get('id')}",
            'title': job.get('title', ''),
            'company': company_name,
            'location': location,
            'url': job_url,
            'description': description,
            'posted_date': job.get('publishedDate', datetime.now().isoformat()),
            'source': 'Ashby',
            'department': department,
            'employment_type': job.get('employmentType', ''),
            'raw_data': job
        }

    def fetch_multiple_companies(self, companies: List[Dict]) -> List[Dict]:
        """
        Fetch jobs from multiple companies

        Args:
            companies: List of dicts with 'name' and 'ashby' keys

        Returns:
            Combined list of all jobs from all companies
        """
        all_jobs = []

        ashby_companies = [c for c in companies if 'ashby' in c]
        logger.info(f"Fetching from {len(ashby_companies)} Ashby companies...")

        for company in ashby_companies:
            jobs = self.fetch_company_jobs(
                company_handle=company['ashby'],
                company_name=company['name']
            )
            all_jobs.extend(jobs)

        return all_jobs


if __name__ == "__main__":
    # Test the scraper
    logging.basicConfig(level=logging.INFO)

    scraper = AshbyScraper()

    # Test with design-focused companies
    test_companies = [
        {'name': 'Notion', 'ashby': 'notion'},
        {'name': 'Linear', 'ashby': 'linear'},
        {'name': 'Anthropic', 'ashby': 'anthropic'}
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
