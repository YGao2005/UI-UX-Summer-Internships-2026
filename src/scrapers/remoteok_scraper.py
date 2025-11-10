"""
RemoteOK scraper - No authentication required, completely free
30,000+ remote jobs, updated frequently

IMPORTANT: RemoteOK requires attribution. Add a link back to remoteok.com
"""

import requests
import logging
from typing import List, Dict, Optional
from datetime import datetime
import time

logger = logging.getLogger(__name__)


class RemoteOKScraper:
    """Scraper for RemoteOK public API"""

    API_URL = "https://remoteok.com/api"

    def __init__(self):
        self.session = requests.Session()
        # RemoteOK asks for descriptive user agents
        self.session.headers.update({
            'User-Agent': 'UI-UX-Internship-Tracker/1.0 (Educational Project; Contact: your-email@example.com)'
        })

    def fetch_jobs(self, search_tag: str = 'design') -> List[Dict]:
        """
        Fetch jobs from RemoteOK

        Args:
            search_tag: Optional tag to filter jobs (e.g., 'design', 'ui', 'ux')

        Returns:
            List of standardized job dictionaries

        Note:
            RemoteOK API returns all jobs. First item in response is metadata (legal text),
            so we skip it.
        """
        try:
            response = self.session.get(self.API_URL, timeout=15)
            response.raise_for_status()

            all_jobs = response.json()

            # First item is always metadata/legal notice, skip it
            if all_jobs and isinstance(all_jobs[0], dict) and 'legal' in str(all_jobs[0]):
                all_jobs = all_jobs[1:]

            logger.info(f"✓ RemoteOK: {len(all_jobs)} total jobs fetched")

            # Filter by tags if specified
            if search_tag:
                filtered_jobs = [
                    job for job in all_jobs
                    if search_tag.lower() in [tag.lower() for tag in job.get('tags', [])]
                ]
                logger.info(f"  → {len(filtered_jobs)} jobs match tag '{search_tag}'")
                all_jobs = filtered_jobs

            # Convert to standardized format
            return [self._normalize_job(job) for job in all_jobs]

        except requests.exceptions.RequestException as e:
            logger.error(f"✗ RemoteOK: Request failed: {str(e)}")
            return []

    def _normalize_job(self, job: Dict) -> Dict:
        """Convert RemoteOK job format to standardized format"""

        # RemoteOK uses epoch timestamps (handle both int and string)
        posted_timestamp = job.get('date', time.time())
        try:
            if isinstance(posted_timestamp, str):
                # Try to parse as ISO date string first
                try:
                    posted_date = posted_timestamp
                except:
                    # If that fails, try as timestamp
                    posted_date = datetime.fromtimestamp(float(posted_timestamp)).isoformat()
            else:
                posted_date = datetime.fromtimestamp(posted_timestamp).isoformat()
        except (ValueError, TypeError):
            # Fallback to current time if parsing fails
            posted_date = datetime.now().isoformat()

        # Extract location
        location = job.get('location', 'Remote')
        if not location or location == 'false':
            location = 'Remote'

        # Build description from available fields
        description_parts = []
        if job.get('description'):
            description_parts.append(job['description'])
        if job.get('company_logo'):
            description_parts.append(f"Logo: {job['company_logo']}")

        description = '\n\n'.join(filter(None, description_parts))

        # Get tags
        tags = job.get('tags', [])

        return {
            'id': f"remoteok_{job.get('id', job.get('slug', ''))}",
            'title': job.get('position', ''),
            'company': job.get('company', 'Unknown'),
            'location': location,
            'url': job.get('url', f"https://remoteok.com/remote-jobs/{job.get('slug', '')}"),
            'description': description,
            'posted_date': posted_date,
            'source': 'RemoteOK',
            'tags': tags,
            'salary_min': job.get('salary_min'),
            'salary_max': job.get('salary_max'),
            'raw_data': job
        }


if __name__ == "__main__":
    # Test the scraper
    logging.basicConfig(level=logging.INFO)

    scraper = RemoteOKScraper()

    # Fetch design jobs
    jobs = scraper.fetch_jobs(search_tag='design')
    print(f"\nTotal design jobs found: {len(jobs)}")

    # Show a few sample jobs
    for job in jobs[:3]:
        print(f"\n  Company: {job['company']}")
        print(f"  Title: {job['title']}")
        print(f"  Tags: {', '.join(job['tags'])}")
        print(f"  URL: {job['url']}")

    # Test fetching UI/UX specific
    print("\n" + "="*50)
    print("Testing with 'ui' tag:")
    ui_jobs = scraper.fetch_jobs(search_tag='ui')
    print(f"Total UI jobs found: {len(ui_jobs)}")
