"""
RSS Feed scraper for remote job boards
Aggregates from We Work Remotely, Remotive, Himalayas, and Jobicy
"""

import feedparser
import logging
from typing import List, Dict
from datetime import datetime
import time

logger = logging.getLogger(__name__)


class RSSJobScraper:
    """Scraper for remote job RSS feeds"""

    # Public RSS feeds for remote jobs
    FEEDS = {
        'We Work Remotely': 'https://weworkremotely.com/remote-jobs.rss',
        'Remotive': 'https://remotive.com/remote-jobs/rss-feed',
        'Himalayas': 'https://himalayas.app/jobs/rss',
        'Jobicy': 'https://jobicy.com/jobs-rss-feed.php'
    }

    def __init__(self):
        """Initialize RSS scraper"""
        pass

    def fetch_jobs(self) -> List[Dict]:
        """
        Fetch jobs from all RSS feeds

        Returns:
            List of standardized job dictionaries
        """
        all_jobs = []

        for feed_name, feed_url in self.FEEDS.items():
            try:
                logger.info(f"  Fetching {feed_name} RSS feed...")

                # Parse RSS feed
                feed = feedparser.parse(feed_url)

                if not feed.entries:
                    logger.warning(f"⊘ {feed_name}: No entries found in RSS feed")
                    continue

                # Filter and process entries
                jobs = self._process_feed_entries(feed.entries, feed_name)

                logger.info(f"✓ {feed_name}: {len(jobs)} design/intern jobs found")
                all_jobs.extend(jobs)

                # Be polite - small delay between feeds
                time.sleep(1)

            except Exception as e:
                logger.error(f"✗ {feed_name}: Error fetching RSS feed: {str(e)}")
                continue

        logger.info(f"✓ RSS Feeds: {len(all_jobs)} total jobs found")
        return all_jobs

    def _process_feed_entries(self, entries: List, feed_name: str) -> List[Dict]:
        """
        Process RSS feed entries and filter for design/internship jobs

        Args:
            entries: RSS feed entries
            feed_name: Name of the feed source

        Returns:
            List of standardized job dictionaries
        """
        jobs = []

        for entry in entries:
            # Check if design/UX related
            if not self._is_design_related(entry):
                continue

            # Check if internship (or skip this filter for remote jobs - we'll let keyword filter handle it)
            # Remote jobs often don't explicitly say "internship" in title
            # if not self._is_internship(entry):
            #     continue

            # Extract job details
            job = self._extract_job_from_entry(entry, feed_name)
            if job:
                jobs.append(job)

        return jobs

    def _is_design_related(self, entry) -> bool:
        """Check if entry is design/UX related"""
        title = entry.get('title', '').lower()
        description = entry.get('summary', '').lower() or entry.get('description', '').lower()

        design_keywords = [
            'design', 'ux', 'ui', 'user experience', 'user interface',
            'product design', 'visual design', 'figma', 'sketch'
        ]

        return any(keyword in title or keyword in description for keyword in design_keywords)

    def _is_internship(self, entry) -> bool:
        """Check if entry mentions internship"""
        title = entry.get('title', '').lower()
        description = entry.get('summary', '').lower() or entry.get('description', '').lower()

        internship_keywords = [
            'intern', 'internship', 'co-op', 'co op',
            'junior', 'entry level', 'entry-level',
            'graduate', 'new grad'
        ]

        return any(keyword in title or keyword in description for keyword in internship_keywords)

    def _extract_job_from_entry(self, entry, feed_name: str) -> Dict:
        """
        Extract job details from RSS entry

        Args:
            entry: RSS feed entry
            feed_name: Name of the feed source

        Returns:
            Standardized job dictionary or None
        """
        try:
            # Get basic fields
            title = entry.get('title', 'Remote Design Position')
            link = entry.get('link', '')

            # Extract company from title or author
            company = self._extract_company(entry)

            # Extract location
            location = self._extract_location(entry)

            # Get description
            description = entry.get('summary', '') or entry.get('description', '')

            # Get published date
            published = entry.get('published') or entry.get('updated')
            if published:
                try:
                    # Parse various date formats
                    posted_date = datetime(*entry.get('published_parsed')[:6]).isoformat() if entry.get('published_parsed') else published
                except:
                    posted_date = datetime.now().isoformat()
            else:
                posted_date = datetime.now().isoformat()

            # Build unique ID
            job_id = f"rss_{feed_name.replace(' ', '_').lower()}_{abs(hash(link))}"

            return {
                'id': job_id,
                'title': title,
                'company': company,
                'location': location,
                'url': link,
                'description': description[:500],  # Limit description length
                'posted_date': posted_date,
                'source': f"RSS ({feed_name})"
            }

        except Exception as e:
            logger.debug(f"Error extracting job from RSS entry: {str(e)}")
            return None

    def _extract_company(self, entry) -> str:
        """Extract company name from entry"""
        # Try author field first
        author = entry.get('author', '')
        if author and len(author) < 100:
            return author

        # Try to extract from title (pattern: "Company Name: Job Title" or "Job Title at Company")
        title = entry.get('title', '')

        # Pattern: "Company: Title" or "Company - Title"
        if ':' in title:
            company = title.split(':')[0].strip()
            if len(company) < 50 and company:
                return company

        if ' at ' in title:
            parts = title.split(' at ')
            if len(parts) > 1:
                company = parts[-1].strip()
                if len(company) < 50:
                    return company

        if ' - ' in title:
            parts = title.split(' - ')
            if len(parts) > 1:
                company = parts[0].strip()
                if len(company) < 50 and not any(word in company.lower() for word in ['remote', 'design', 'engineer']):
                    return company

        # Fallback to category or tag
        categories = entry.get('tags', [])
        if categories and isinstance(categories, list) and len(categories) > 0:
            for cat in categories:
                term = cat.get('term', '') if isinstance(cat, dict) else str(cat)
                if term and 'company' not in term.lower():
                    return term

        return 'Remote Company'

    def _extract_location(self, entry) -> str:
        """Extract location from entry"""
        title = entry.get('title', '').lower()
        description = (entry.get('summary', '') or entry.get('description', '')).lower()

        # Check for remote
        if 'remote' in title or 'remote' in description[:200]:
            return 'Remote'

        # Look for location in title or description
        import re
        # Pattern: City, Country or City, ST
        location_pattern = r'\b([A-Z][a-z]+(?:,\s*[A-Z]{2,})?)\b'
        match = re.search(location_pattern, entry.get('title', ''))
        if match:
            return match.group(1)

        return 'Remote'


if __name__ == "__main__":
    # Test the scraper
    logging.basicConfig(level=logging.INFO)

    scraper = RSSJobScraper()
    jobs = scraper.fetch_jobs()

    print(f"\nTotal jobs found: {len(jobs)}")

    # Show sample jobs
    for job in jobs[:5]:
        print(f"\n  Company: {job['company']}")
        print(f"  Title: {job['title']}")
        print(f"  Location: {job['location']}")
        print(f"  Source: {job['source']}")
        print(f"  URL: {job['url'][:60]}...")
