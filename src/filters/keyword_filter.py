"""
Smart keyword filtering for UI/UX internships
Uses weighted scoring to ensure high-quality matches
"""

import yaml
import logging
from typing import Dict, List, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class KeywordFilter:
    """Filters jobs based on keyword matching with scoring"""

    def __init__(self, config_path: str = None):
        """
        Initialize filter with keyword configuration

        Args:
            config_path: Path to keywords.yml file. If None, uses default location.
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / 'data' / 'keywords.yml'

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.internship_keywords = [k.lower() for k in self.config.get('internship_keywords', [])]
        self.include_title = [k.lower() for k in self.config.get('include_title', [])]
        self.exclude_title = [k.lower() for k in self.config.get('exclude_title', [])]
        self.include_description = [k.lower() for k in self.config.get('include_description', [])]
        self.minimum_score = self.config.get('minimum_match_score', 3)

        logger.info(f"Keyword filter initialized (min score: {self.minimum_score})")

    def is_internship(self, job: Dict) -> bool:
        """
        Check if job is an internship

        Args:
            job: Job dictionary with 'title' and 'description' keys

        Returns:
            True if job appears to be an internship
        """
        title = str(job.get('title', '')).lower()
        description = str(job.get('description', '')).lower()

        # Check title first (most reliable)
        for keyword in self.internship_keywords:
            if keyword in title:
                return True

        # Check description as fallback
        for keyword in self.internship_keywords[:3]:  # Only check intern/internship/co-op in description
            if keyword in description[:500]:  # Only check first 500 chars
                return True

        return False

    def calculate_relevance_score(self, job: Dict) -> Tuple[int, Dict]:
        """
        Calculate relevance score for a job

        Args:
            job: Job dictionary with 'title' and 'description' keys

        Returns:
            Tuple of (score, breakdown) where breakdown shows how score was calculated
        """
        title = str(job.get('title', '')).lower()
        description = str(job.get('description', '')).lower()

        breakdown = {
            'title_matches': [],
            'title_excludes': [],
            'description_matches': [],
            'total_score': 0
        }

        score = 0

        # Title matching (weighted +3)
        for keyword in self.include_title:
            if keyword in title:
                score += 3
                breakdown['title_matches'].append(keyword)

        # Title exclusions (heavy penalty -10)
        for keyword in self.exclude_title:
            if keyword in title:
                score -= 10
                breakdown['title_excludes'].append(keyword)

        # Description matching (+1 each)
        for keyword in self.include_description:
            if keyword in description:
                score += 1
                breakdown['description_matches'].append(keyword)

        breakdown['total_score'] = score

        return score, breakdown

    def is_relevant(self, job: Dict) -> bool:
        """
        Check if job is relevant for UI/UX design

        Args:
            job: Job dictionary

        Returns:
            True if job meets minimum relevance threshold
        """
        score, _ = self.calculate_relevance_score(job)
        return score >= self.minimum_score

    def filter_jobs(self, jobs: List[Dict], require_internship: bool = True) -> List[Dict]:
        """
        Filter jobs based on relevance and internship status

        Args:
            jobs: List of job dictionaries
            require_internship: If True, only return internships

        Returns:
            Filtered list of relevant jobs with scores attached
        """
        filtered_jobs = []

        for job in jobs:
            # Check if internship (if required)
            if require_internship and not self.is_internship(job):
                continue

            # Calculate relevance score
            score, breakdown = self.calculate_relevance_score(job)

            # Check if meets minimum threshold
            if score >= self.minimum_score:
                # Attach score and breakdown to job
                job['relevance_score'] = score
                job['score_breakdown'] = breakdown
                filtered_jobs.append(job)

        logger.info(f"Filtered {len(jobs)} jobs → {len(filtered_jobs)} relevant UI/UX internships")

        # Sort by relevance score (highest first)
        filtered_jobs.sort(key=lambda x: x['relevance_score'], reverse=True)

        return filtered_jobs

    def get_statistics(self, jobs: List[Dict]) -> Dict:
        """
        Get statistics about filtered jobs

        Args:
            jobs: List of filtered jobs (with relevance_score attached)

        Returns:
            Dictionary of statistics
        """
        if not jobs:
            return {
                'total': 0,
                'average_score': 0,
                'score_range': (0, 0),
                'top_keywords': {}
            }

        scores = [j['relevance_score'] for j in jobs]

        # Count top keywords
        keyword_counts = {}
        for job in jobs:
            for keyword in job.get('score_breakdown', {}).get('title_matches', []):
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1

        return {
            'total': len(jobs),
            'average_score': sum(scores) / len(scores),
            'score_range': (min(scores), max(scores)),
            'top_keywords': dict(sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        }


if __name__ == "__main__":
    # Test the filter
    logging.basicConfig(level=logging.INFO)

    filter_system = KeywordFilter()

    # Test jobs
    test_jobs = [
        {
            'title': 'UX Design Intern',
            'description': 'Work with Figma to create wireframes and prototypes for our mobile app',
            'company': 'Test Co'
        },
        {
            'title': 'Graphic Design Intern',
            'description': 'Create print materials and social media graphics',
            'company': 'Test Co'
        },
        {
            'title': 'Product Design Intern',
            'description': 'Help design our web application using Figma and conduct user research',
            'company': 'Test Co'
        },
        {
            'title': 'Senior Software Engineer',
            'description': 'Build backend systems with Python',
            'company': 'Test Co'
        }
    ]

    print("Testing keyword filter:\n")
    for job in test_jobs:
        is_intern = filter_system.is_internship(job)
        score, breakdown = filter_system.calculate_relevance_score(job)
        is_rel = filter_system.is_relevant(job)

        print(f"Title: {job['title']}")
        print(f"  Is internship: {is_intern}")
        print(f"  Relevance score: {score}")
        print(f"  Is relevant: {is_rel}")
        print(f"  Breakdown: {breakdown}")
        print()

    # Test full filtering
    print("\nFiltering all jobs:")
    filtered = filter_system.filter_jobs(test_jobs)
    print(f"Kept {len(filtered)} out of {len(test_jobs)} jobs")
    for job in filtered:
        print(f"  - {job['title']} (score: {job['relevance_score']})")
