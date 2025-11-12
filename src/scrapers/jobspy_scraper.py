"""
JobSpy scraper - Aggregates jobs from Indeed, Glassdoor, ZipRecruiter, and more
Free and open-source library for job scraping
GitHub: https://github.com/speedyapply/JobSpy
"""

import logging
import time
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class JobSpyScraper:
    """Scraper using JobSpy library for multiple job boards"""

    def __init__(self):
        """Initialize JobSpy scraper"""
        # Removed zip_recruiter (known library issue - returns 0 jobs)
        # See: https://github.com/speedyapply/JobSpy/issues/283, #302, #273
        self.site_names = ["indeed", "glassdoor", "linkedin"]

    def fetch_jobs(
        self,
        search_terms: List[str] = None,  # Now accepts list of terms
        location: str = "United States",
        results_wanted: int = 100
    ) -> List[Dict]:
        """
        Fetch jobs from multiple sources using JobSpy
        Runs multiple searches with different terms to maximize coverage

        Args:
            search_terms: List of search queries (default: ['UX intern', 'UI intern', 'design intern'])
            location: Job location to search in
            results_wanted: Number of results to fetch per site per term

        Returns:
            List of standardized job dictionaries (combined from all searches)
        """
        if search_terms is None:
            search_terms = ['UX intern', 'UI intern', 'design intern']

        # Handle legacy single string parameter
        if isinstance(search_terms, str):
            search_terms = [search_terms]

        try:
            # Import here to provide clearer error message if not installed
            from jobspy import scrape_jobs
        except ImportError:
            logger.error("✗ JobSpy: jobspy not installed. Run: pip install jobspy")
            return []

        all_jobs = []

        logger.info(f"  Running {len(search_terms)} searches: {', '.join(search_terms)}")

        for i, search_term in enumerate(search_terms, 1):
            try:
                logger.info(f"    [{i}/{len(search_terms)}] Searching for '{search_term}'...")

                # Add small delay before starting to be respectful
                if i > 1:
                    time.sleep(10)  # Rate limiting between searches

                # Scrape jobs from multiple sites
                # Note: job_type removed - conflicts with hours_old on Indeed
                # Note: hours_old removed - LinkedIn performs much better without it (53 vs 19 jobs)
                # Our keyword filter handles both internship detection and recency filtering
                jobs_df = scrape_jobs(
                    site_name=self.site_names,
                    search_term=search_term,
                    location=location,
                    distance=50,  # 50 mile radius
                    is_remote=True,  # Include remote jobs
                    results_wanted=results_wanted,  # Per site
                )

                if jobs_df is None or jobs_df.empty:
                    logger.info(f"      ⊘ No jobs found for '{search_term}'")
                    continue

                # Convert DataFrame to list of dicts
                jobs_list = jobs_df.to_dict('records')

                logger.info(f"      ✓ {len(jobs_list)} jobs found for '{search_term}'")

                # Convert to standardized format
                standardized = [self._normalize_job(job) for job in jobs_list]

                # Filter out any jobs that failed normalization
                standardized = [job for job in standardized if job is not None]

                all_jobs.extend(standardized)

            except Exception as e:
                logger.error(f"      ✗ Error searching '{search_term}': {str(e)}")
                continue

        logger.info(f"✓ JobSpy: {len(all_jobs)} total jobs from {len(search_terms)} searches (before deduplication)")

        return all_jobs

    def _normalize_job(self, job: Dict) -> Dict:
        """
        Convert JobSpy job format to standardized format

        JobSpy returns fields like:
        - title, company, location, job_url, description
        - date_posted, site, job_type
        - min_amount, max_amount, currency (salary info)
        """
        try:
            # Extract required fields
            import math

            # Handle title (can be NaN from pandas DataFrame)
            title_raw = job.get('title', '')
            if isinstance(title_raw, float) and math.isnan(title_raw):
                title = ''
            else:
                title = str(title_raw) if title_raw else ''

            # Handle company (can be NaN from pandas DataFrame)
            company_raw = job.get('company', 'Unknown')
            if isinstance(company_raw, float) and math.isnan(company_raw):
                company = 'Unknown'
            else:
                company = str(company_raw) if company_raw else 'Unknown'

            # Handle location (can be NaN from pandas DataFrame)
            location_raw = job.get('location', 'Remote')
            if isinstance(location_raw, float) and math.isnan(location_raw):
                location = 'Remote'
            else:
                location = str(location_raw) if location_raw else 'Remote'

            job_url = job.get('job_url', '')
            description = job.get('description', '')

            # Extract date posted (JobSpy returns datetime/date object or string)
            date_posted = job.get('date_posted')
            if isinstance(date_posted, str):
                posted_date = date_posted
            elif date_posted is not None:
                # Convert datetime/date to ISO format string
                try:
                    posted_date = date_posted.isoformat() if hasattr(date_posted, 'isoformat') else str(date_posted)
                except Exception:
                    posted_date = str(date_posted)
            else:
                posted_date = datetime.now().isoformat()

            # Get source site
            source_site = job.get('site', 'JobSpy')

            # Build unique ID using site and job_url hash
            job_id = f"jobspy_{source_site}_{abs(hash(job_url))}"

            # Extract salary info if available
            salary_info = None
            min_amount = job.get('min_amount')
            max_amount = job.get('max_amount')
            currency = job.get('currency', 'USD')

            # Check for valid salary amounts (not None and not NaN)
            import math
            salary_parts = []
            if min_amount is not None and not (isinstance(min_amount, float) and math.isnan(min_amount)):
                try:
                    salary_parts.append(f"${int(min_amount):,}")
                except (ValueError, TypeError):
                    pass
            if max_amount is not None and not (isinstance(max_amount, float) and math.isnan(max_amount)):
                try:
                    salary_parts.append(f"${int(max_amount):,}")
                except (ValueError, TypeError):
                    pass
            if salary_parts:
                salary_info = f"{' - '.join(salary_parts)} {currency}"

            return {
                'id': job_id,
                'title': title,
                'company': company,
                'location': location,
                'url': job_url,
                'description': description,
                'posted_date': posted_date,
                'source': f"JobSpy ({source_site.title()})",
                'job_type': job.get('job_type'),
                'salary': salary_info
                # Note: raw_data omitted to avoid JSON serialization issues with date objects
            }

        except Exception as e:
            logger.warning(f"  Skipping job due to normalization error: {str(e)}")
            return None


if __name__ == "__main__":
    # Test the scraper
    logging.basicConfig(level=logging.INFO)

    scraper = JobSpyScraper()

    # Fetch UI/UX design internships
    jobs = scraper.fetch_jobs(
        search_term='UI UX design intern',
        location='United States',
        results_wanted=20  # Small number for testing
    )

    print(f"\nTotal jobs found: {len(jobs)}")

    # Show a few sample jobs
    for job in jobs[:3]:
        print(f"\n  Company: {job['company']}")
        print(f"  Title: {job['title']}")
        print(f"  Location: {job['location']}")
        print(f"  Source: {job['source']}")
        print(f"  URL: {job['url'][:80]}...")
        if job.get('salary'):
            print(f"  Salary: {job['salary']}")
