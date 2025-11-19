"""
Job deduplication using fuzzy string matching
Handles cases where same job appears on multiple platforms
"""

import logging
from typing import List, Dict, Tuple
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class JobDeduplicator:
    """Deduplicates jobs based on company + title similarity"""

    def __init__(self, title_similarity_threshold: float = 0.85):
        """
        Initialize deduplicator

        Args:
            title_similarity_threshold: Minimum similarity ratio (0-1) to consider titles duplicate
        """
        self.title_threshold = title_similarity_threshold

    def calculate_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate similarity ratio between two strings

        Args:
            str1: First string
            str2: Second string

        Returns:
            Similarity ratio between 0 and 1
        """
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

    def are_jobs_duplicate(self, job1: Dict, job2: Dict) -> Tuple[bool, str]:
        """
        Check if two jobs are duplicates

        Args:
            job1: First job dictionary
            job2: Second job dictionary

        Returns:
            Tuple of (is_duplicate, reason)
        """
        # Exact ID match (same source)
        if job1.get('id') == job2.get('id'):
            return True, "Exact ID match"

        # Same company check - handle non-string values (float, NaN, etc)
        company1_raw = job1.get('company', '')
        company2_raw = job2.get('company', '')

        # Convert to string if not already (handles float, NaN, etc)
        company1 = str(company1_raw).lower().strip() if company1_raw not in [None, ''] else ''
        company2 = str(company2_raw).lower().strip() if company2_raw not in [None, ''] else ''

        # Skip if NaN or invalid company names
        if company1 in ['nan', 'none', ''] or company2 in ['nan', 'none', '']:
            return False, "Missing or invalid company"

        # Different companies = not duplicate
        if company1 != company2:
            return False, "Different companies"

        # Same company - check title similarity - handle non-string values
        title1_raw = job1.get('title', '')
        title2_raw = job2.get('title', '')

        title1 = str(title1_raw).lower().strip() if title1_raw not in [None, ''] else ''
        title2 = str(title2_raw).lower().strip() if title2_raw not in [None, ''] else ''

        if title1 in ['nan', 'none', ''] or title2 in ['nan', 'none', '']:
            return False, "Missing or invalid title"

        # Exact title match
        if title1 == title2:
            return True, f"Exact match: {company1}"

        # Fuzzy title match
        similarity = self.calculate_similarity(title1, title2)
        if similarity >= self.title_threshold:
            return True, f"Similar titles: {company1} ({similarity:.2f})"

        return False, f"Different roles at {company1}"

    def deduplicate(self, jobs: List[Dict]) -> List[Dict]:
        """
        Remove duplicate jobs, keeping the one with highest relevance score

        Args:
            jobs: List of job dictionaries

        Returns:
            Deduplicated list of jobs
        """
        if not jobs:
            return []

        unique_jobs = []
        duplicates_found = 0

        for job in jobs:
            is_duplicate = False

            for existing_job in unique_jobs:
                is_dup, reason = self.are_jobs_duplicate(job, existing_job)

                if is_dup:
                    is_duplicate = True
                    duplicates_found += 1

                    # Keep the one with higher relevance score (if available)
                    job_score = job.get('relevance_score', 0)
                    existing_score = existing_job.get('relevance_score', 0)

                    if job_score > existing_score:
                        # Replace existing with new one
                        unique_jobs.remove(existing_job)
                        unique_jobs.append(job)
                        logger.debug(f"Replaced duplicate (better score): {reason}")
                    else:
                        logger.debug(f"Skipped duplicate: {reason}")

                    break

            if not is_duplicate:
                unique_jobs.append(job)

        logger.info(f"Deduplication: {len(jobs)} jobs → {len(unique_jobs)} unique ({duplicates_found} duplicates removed)")

        return unique_jobs

    def find_duplicates(self, jobs: List[Dict]) -> List[Tuple[Dict, Dict, str]]:
        """
        Find all duplicate pairs (useful for debugging)

        Args:
            jobs: List of job dictionaries

        Returns:
            List of tuples (job1, job2, reason)
        """
        duplicates = []

        for i, job1 in enumerate(jobs):
            for job2 in jobs[i+1:]:
                is_dup, reason = self.are_jobs_duplicate(job1, job2)
                if is_dup:
                    duplicates.append((job1, job2, reason))

        return duplicates


if __name__ == "__main__":
    # Test the deduplicator
    logging.basicConfig(level=logging.INFO)

    dedup = JobDeduplicator()

    # Test jobs with duplicates
    test_jobs = [
        {
            'id': '1',
            'company': 'Figma',
            'title': 'Product Design Intern',
            'relevance_score': 10
        },
        {
            'id': '2',
            'company': 'Figma',
            'title': 'Product Design Internship',
            'relevance_score': 8
        },
        {
            'id': '3',
            'company': 'Stripe',
            'title': 'UX Design Intern',
            'relevance_score': 9
        },
        {
            'id': '4',
            'company': 'Figma',
            'title': 'Engineering Intern',
            'relevance_score': 7
        },
        {
            'id': '5',
            'company': 'Stripe',
            'title': 'UX Design Intern',
            'relevance_score': 11
        }
    ]

    print("Original jobs:")
    for job in test_jobs:
        print(f"  {job['company']}: {job['title']} (score: {job['relevance_score']})")

    print("\nFinding duplicates:")
    duplicates = dedup.find_duplicates(test_jobs)
    for job1, job2, reason in duplicates:
        print(f"  DUPLICATE: {job1['company']} - {job1['title']} ≈ {job2['title']}")
        print(f"    Reason: {reason}")

    print("\nDeduplicating:")
    unique = dedup.deduplicate(test_jobs)

    print("\nUnique jobs:")
    for job in unique:
        print(f"  {job['company']}: {job['title']} (score: {job['relevance_score']})")
