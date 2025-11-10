"""
Hacker News "Who is Hiring?" scraper
Scrapes monthly job threads from Hacker News for design/UX internships
API: Algolia HN Search (https://hn.algolia.com/api)
"""

import requests
import logging
import re
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class HackerNewsScraper:
    """Scraper for Hacker News 'Who is Hiring?' threads"""

    ALGOLIA_SEARCH_URL = "https://hn.algolia.com/api/v1/search"
    ALGOLIA_ITEM_URL = "https://hn.algolia.com/api/v1/items"
    HN_ITEM_URL = "https://news.ycombinator.com/item"

    def __init__(self):
        """Initialize Hacker News scraper"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'UI-UX-Internship-Tracker/1.0 (Educational Project)'
        })

    def fetch_jobs(self) -> List[Dict]:
        """
        Fetch design/UX internship jobs from latest 'Who is Hiring?' thread

        Returns:
            List of standardized job dictionaries
        """
        try:
            # Step 1: Find the latest "Who is Hiring?" thread
            logger.info("  Searching for latest 'Who is Hiring?' thread...")
            thread_id = self._find_latest_hiring_thread()

            if not thread_id:
                logger.warning("⊘ Hacker News: No hiring thread found")
                return []

            # Step 2: Fetch comments from the thread
            logger.info(f"  Fetching comments from thread {thread_id}...")
            comments = self._fetch_thread_comments(thread_id)

            if not comments:
                logger.warning("⊘ Hacker News: No comments found in thread")
                return []

            # Step 3: Filter and parse for design/UX internships
            logger.info(f"  Parsing {len(comments)} comments for design internships...")
            jobs = self._parse_comments_for_jobs(comments)

            logger.info(f"✓ Hacker News: {len(jobs)} design/UX internships found")
            return jobs

        except Exception as e:
            logger.error(f"✗ Hacker News: Error during scraping: {str(e)}")
            return []

    def _find_latest_hiring_thread(self) -> str:
        """Find the most recent 'Who is Hiring?' thread"""
        try:
            params = {
                'query': 'Ask HN: Who is hiring?',
                'tags': 'story',
                'hitsPerPage': 5
            }

            response = self.session.get(self.ALGOLIA_SEARCH_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            hits = data.get('hits', [])
            if not hits:
                return None

            # Find the most recent thread (should be first result)
            for hit in hits:
                title = hit.get('title', '').lower()
                # Look for pattern like "ask hn: who is hiring? (month year)"
                if 'who is hiring' in title and 'ask hn' in title:
                    return hit.get('objectID')

            return None

        except Exception as e:
            logger.error(f"Error finding hiring thread: {str(e)}")
            return None

    def _fetch_thread_comments(self, thread_id: str) -> List[Dict]:
        """Fetch all top-level comments from a thread"""
        try:
            url = f"{self.ALGOLIA_ITEM_URL}/{thread_id}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Get top-level comments (direct children of the story)
            children = data.get('children', [])
            return children

        except Exception as e:
            logger.error(f"Error fetching thread comments: {str(e)}")
            return []

    def _parse_comments_for_jobs(self, comments: List[Dict]) -> List[Dict]:
        """
        Parse comments to find design/UX internship postings

        Each comment is a job posting in unstructured text format
        """
        jobs = []

        for comment in comments:
            # Get comment text (HTML formatted)
            text = comment.get('text', '')
            if not text:
                continue

            # Check if it's design/UX related
            if not self._is_design_related(text):
                continue

            # Check if it mentions internship
            if not self._is_internship(text):
                continue

            # Parse the job details
            job = self._extract_job_details(comment, text)
            if job:
                jobs.append(job)

        return jobs

    def _is_design_related(self, text: str) -> bool:
        """Check if comment mentions design/UX/UI"""
        text_lower = text.lower()
        design_keywords = [
            'design', 'ux', 'ui', 'user experience', 'user interface',
            'product design', 'visual design', 'interaction design',
            'figma', 'sketch', 'adobe xd'
        ]
        return any(keyword in text_lower for keyword in design_keywords)

    def _is_internship(self, text: str) -> bool:
        """Check if comment mentions internship"""
        text_lower = text.lower()
        internship_keywords = [
            'intern', 'internship', 'co-op', 'co op',
            'summer 2025', 'summer 2026', 'fall 2025', 'spring 2026'
        ]
        return any(keyword in text_lower for keyword in internship_keywords)

    def _extract_job_details(self, comment: Dict, text: str) -> Dict:
        """
        Extract structured job details from unstructured comment text

        Returns:
            Standardized job dictionary or None if parsing fails
        """
        try:
            # Clean HTML tags from text
            import html
            text_clean = re.sub(r'<[^>]+>', ' ', text)
            text_clean = html.unescape(text_clean)

            # Extract company name (usually first line or capitalized word)
            company = self._extract_company(text_clean)

            # Extract location
            location = self._extract_location(text_clean)

            # Extract title (look for role/position keywords)
            title = self._extract_title(text_clean)

            # Build HN comment URL
            comment_id = comment.get('id') or comment.get('objectID')
            url = f"{self.HN_ITEM_URL}?id={comment_id}"

            # Get posting date
            created_at = comment.get('created_at')
            if created_at:
                try:
                    posted_date = datetime.fromisoformat(created_at.replace('Z', '+00:00')).isoformat()
                except:
                    posted_date = datetime.now().isoformat()
            else:
                posted_date = datetime.now().isoformat()

            return {
                'id': f"hn_{comment_id}",
                'title': title,
                'company': company,
                'location': location,
                'url': url,
                'description': text_clean[:500],  # First 500 chars
                'posted_date': posted_date,
                'source': 'Hacker News'
            }

        except Exception as e:
            logger.debug(f"Error extracting job details: {str(e)}")
            return None

    def _extract_company(self, text: str) -> str:
        """Try to extract company name from text"""
        # Try to find company name in first line or after common patterns
        lines = text.split('\n')
        first_line = lines[0].strip() if lines else ''

        # Pattern: "Company Name | Location | Remote"
        if '|' in first_line:
            company = first_line.split('|')[0].strip()
            if company and len(company) < 50:
                return company

        # Pattern: "COMPANY NAME is hiring..."
        match = re.search(r'^([A-Z][A-Za-z0-9\s&.-]+)\s+(?:is|are)\s+hiring', text, re.MULTILINE)
        if match:
            return match.group(1).strip()

        # Pattern: "Company: XYZ"
        match = re.search(r'Company:\s*([^\n]+)', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Fallback: look for capitalized words in first 100 chars
        words = first_line[:100].split()
        for word in words:
            if word and word[0].isupper() and len(word) > 2 and word not in ['Remote', 'REMOTE', 'USA', 'US']:
                return word

        return 'Startup (via HN)'

    def _extract_location(self, text: str) -> str:
        """Try to extract location from text"""
        # Common patterns
        patterns = [
            r'Location:\s*([^\n]+)',
            r'\|\s*([A-Z][a-z]+(?:,\s*[A-Z]{2})?)\s*\|',  # | City, ST |
            r'(?:Remote|REMOTE)',
            r'\b([A-Z][a-z]+,\s*(?:CA|NY|TX|MA|WA|OR|CO))\b',  # City, State
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1) if match.lastindex else match.group(0)
                return location.strip()

        # Check if "remote" appears anywhere
        if re.search(r'\bremote\b', text, re.IGNORECASE):
            return 'Remote'

        return 'See posting'

    def _extract_title(self, text: str) -> str:
        """Try to extract job title from text"""
        # Look for common title patterns
        title_patterns = [
            r'(?:Product|UX|UI|User Experience|Visual|Interaction)\s+(?:Design|Designer)\s+Intern',
            r'Design\s+Intern',
            r'Intern[:\-\s]+(?:Product|UX|UI|Design)',
        ]

        for pattern in title_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0).strip()

        # Fallback
        if 'intern' in text.lower():
            return 'Design Internship'

        return 'Product Design Intern'


if __name__ == "__main__":
    # Test the scraper
    logging.basicConfig(level=logging.INFO)

    scraper = HackerNewsScraper()
    jobs = scraper.fetch_jobs()

    print(f"\nTotal jobs found: {len(jobs)}")

    # Show sample jobs
    for job in jobs[:5]:
        print(f"\n  Company: {job['company']}")
        print(f"  Title: {job['title']}")
        print(f"  Location: {job['location']}")
        print(f"  URL: {job['url']}")
        print(f"  Description: {job['description'][:100]}...")
