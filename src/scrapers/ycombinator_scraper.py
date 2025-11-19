"""
Y Combinator (Hacker News) Jobs scraper
Simple HTML parsing for startup internship postings
Respects robots.txt (Crawl-delay: 30)
"""

import requests
import logging
from typing import List, Dict
from datetime import datetime
from bs4 import BeautifulSoup
import time

logger = logging.getLogger(__name__)


class YCombinatorScraper:
    """Scraper for Y Combinator / Hacker News job postings"""

    BASE_URL = "https://news.ycombinator.com/jobs"

    # Respect robots.txt crawl-delay: 30 seconds
    CRAWL_DELAY = 30

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'UI-UX-Internship-Tracker/1.0 (Educational Project; Respecting robots.txt)'
        })
        self.last_request_time = 0

    def _respect_crawl_delay(self):
        """
        Ensure we respect the 30-second crawl delay from robots.txt
        """
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.CRAWL_DELAY:
            sleep_time = self.CRAWL_DELAY - time_since_last_request
            logger.debug(f"Respecting crawl-delay: sleeping {sleep_time:.1f}s")
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def fetch_jobs(self) -> List[Dict]:
        """
        Fetch jobs from Y Combinator job board

        Returns:
            List of standardized job dictionaries (filtered for internships)
        """
        self._respect_crawl_delay()

        try:
            response = self.session.get(self.BASE_URL, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all job postings (tr elements with class "athing submission")
            job_rows = soup.find_all('tr', class_='athing submission')

            logger.info(f"✓ YC Jobs: {len(job_rows)} total jobs found")

            all_jobs = []
            for row in job_rows:
                job = self._parse_job_row(row)
                if job:
                    all_jobs.append(job)

            # Filter for internships only
            internships = [job for job in all_jobs if self._is_internship(job)]

            logger.info(f"  → {len(internships)} internship positions")

            return internships

        except requests.exceptions.RequestException as e:
            logger.error(f"✗ YC Jobs: Request failed: {str(e)}")
            return []

    def _parse_job_row(self, row) -> Dict:
        """
        Parse a single job row from the HN jobs page

        Args:
            row: BeautifulSoup element for the job row

        Returns:
            Dict with job information, or None if parsing fails
        """
        try:
            # Get the job ID
            job_id = row.get('id', '')

            # Find the title link
            titleline = row.find('span', class_='titleline')
            if not titleline:
                return None

            link = titleline.find('a')
            if not link:
                return None

            title = link.get_text(strip=True)
            url = link.get('href', '')

            # Handle relative URLs (item?id=...)
            if url.startswith('item?'):
                url = f"https://news.ycombinator.com/{url}"

            # Try to extract company name from title (YC companies often in format "Company (YC SXX)")
            company = "Unknown"
            if '(YC ' in title:
                # Extract company name before (YC ...)
                parts = title.split('(YC ')
                if parts:
                    company = parts[0].strip().split(' is ')[0].split(' Is ')[0]

            # Find the next row which contains the age
            next_row = row.find_next_sibling('tr')
            age_span = next_row.find('span', class_='age') if next_row else None
            posted_date = datetime.now().isoformat()

            if age_span:
                # Extract timestamp if available
                timestamp = age_span.get('title', '')
                if timestamp:
                    # Format: "2025-11-08T12:00:50 1762603250"
                    date_parts = timestamp.split(' ')
                    if date_parts:
                        posted_date = date_parts[0]

            return {
                'id': f"yc_{job_id}",
                'title': title,
                'company': company,
                'location': 'Varies',  # YC jobs don't always specify location in listing
                'url': url,
                'description': title,  # HN jobs don't have descriptions on listing page
                'posted_date': posted_date,
                'source': 'YCombinator',
                'raw_data': {
                    'job_id': job_id,
                    'title': title,
                    'url': url
                }
            }

        except Exception as e:
            logger.debug(f"Failed to parse job row: {str(e)}")
            return None

    def _is_internship(self, job: Dict) -> bool:
        """
        Check if a job is an internship

        Args:
            job: Job dictionary

        Returns:
            True if job appears to be an internship
        """
        title_lower = job.get('title', '').lower()
        url_lower = job.get('url', '').lower()

        internship_keywords = [
            'intern',
            'internship',
            'co-op',
            'co op',
            'student',
            'summer 2025',
            'summer 2026'
        ]

        # Check title and URL
        text_to_check = f"{title_lower} {url_lower}"

        for keyword in internship_keywords:
            if keyword in text_to_check:
                return True

        return False


if __name__ == "__main__":
    # Test the scraper
    logging.basicConfig(level=logging.INFO)

    scraper = YCombinatorScraper()
    jobs = scraper.fetch_jobs()

    print(f"\nTotal internships found: {len(jobs)}")

    # Show all internships
    for job in jobs:
        print(f"\n  Company: {job['company']}")
        print(f"  Title: {job['title']}")
        print(f"  URL: {job['url']}")
