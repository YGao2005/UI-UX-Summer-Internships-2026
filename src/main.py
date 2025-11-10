#!/usr/bin/env python3
"""
Main orchestrator for UI/UX Internship Scraper
Coordinates all scrapers, filtering, deduplication, and output generation
"""

import os
import sys
import json
import yaml
import logging
from pathlib import Path
from datetime import datetime

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from scrapers.greenhouse_scraper import GreenhouseScraper
from scrapers.lever_scraper import LeverScraper
from scrapers.ashby_scraper import AshbyScraper
from scrapers.remoteok_scraper import RemoteOKScraper
from scrapers.themuse_scraper import TheMuseScraper
from scrapers.adzuna_scraper import AdzunaScraper
from filters.keyword_filter import KeywordFilter
from utils.deduplicator import JobDeduplicator
from utils.markdown_generator import MarkdownGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class InternshipScraper:
    """Main orchestrator for the scraping pipeline"""

    def __init__(self, project_root: Path = None):
        """
        Initialize scraper with all components

        Args:
            project_root: Root directory of the project
        """
        if project_root is None:
            # Assume we're in src/, go up one level
            project_root = Path(__file__).parent.parent

        self.project_root = project_root
        self.data_dir = project_root / 'data'
        self.companies_file = self.data_dir / 'companies.yml'
        self.jobs_cache_file = self.data_dir / 'jobs.json'

        # Initialize all components
        logger.info("Initializing scraper components...")
        self.greenhouse = GreenhouseScraper()
        self.lever = LeverScraper()
        self.ashby = AshbyScraper()
        self.remoteok = RemoteOKScraper()
        self.themuse = TheMuseScraper()
        self.adzuna = AdzunaScraper()
        self.filter = KeywordFilter()
        self.deduplicator = JobDeduplicator()
        self.markdown = MarkdownGenerator()

        # Load company list
        self.companies = self._load_companies()
        logger.info(f"Loaded {len(self.companies)} companies to track")

    def _load_companies(self) -> list:
        """Load company list from YAML"""
        try:
            with open(self.companies_file, 'r') as f:
                data = yaml.safe_load(f)
                return data.get('companies', [])
        except FileNotFoundError:
            logger.error(f"Companies file not found: {self.companies_file}")
            return []

    def scrape_all_sources(self) -> list:
        """
        Scrape jobs from all sources

        Returns:
            List of all jobs from all sources
        """
        all_jobs = []

        logger.info("="*80)
        logger.info("PHASE 1: Scraping Jobs from All Sources")
        logger.info("="*80)

        # 1. Greenhouse (company-specific)
        logger.info("\n[1/6] Scraping Greenhouse...")
        greenhouse_jobs = self.greenhouse.fetch_multiple_companies(self.companies)
        logger.info(f"  → Found {len(greenhouse_jobs)} jobs from Greenhouse")
        all_jobs.extend(greenhouse_jobs)

        # 2. Lever (company-specific)
        logger.info("\n[2/6] Scraping Lever...")
        lever_jobs = self.lever.fetch_multiple_companies(self.companies)
        logger.info(f"  → Found {len(lever_jobs)} jobs from Lever")
        all_jobs.extend(lever_jobs)

        # 3. Ashby (company-specific)
        logger.info("\n[3/6] Scraping Ashby...")
        ashby_jobs = self.ashby.fetch_multiple_companies(self.companies)
        logger.info(f"  → Found {len(ashby_jobs)} jobs from Ashby")
        all_jobs.extend(ashby_jobs)

        # 4. RemoteOK (general job board)
        logger.info("\n[4/6] Scraping RemoteOK...")
        remoteok_jobs = self.remoteok.fetch_jobs(search_tag='design')
        logger.info(f"  → Found {len(remoteok_jobs)} design jobs from RemoteOK")
        all_jobs.extend(remoteok_jobs)

        # 5. The Muse (internship-focused)
        logger.info("\n[5/6] Scraping The Muse...")
        themuse_jobs = self.themuse.fetch_jobs(category='Design', level='Internship')
        logger.info(f"  → Found {len(themuse_jobs)} design internships from The Muse")
        all_jobs.extend(themuse_jobs)

        # 6. Adzuna (broad coverage)
        logger.info("\n[6/6] Scraping Adzuna...")
        adzuna_jobs = self.adzuna.fetch_jobs(query='UI UX design intern')
        logger.info(f"  → Found {len(adzuna_jobs)} jobs from Adzuna")
        all_jobs.extend(adzuna_jobs)

        logger.info(f"\n✓ Total jobs scraped: {len(all_jobs)}")

        return all_jobs

    def filter_jobs(self, jobs: list) -> list:
        """
        Filter jobs for UI/UX internships

        Args:
            jobs: List of all scraped jobs

        Returns:
            Filtered list of relevant jobs
        """
        logger.info("\n" + "="*80)
        logger.info("PHASE 2: Filtering for UI/UX Internships")
        logger.info("="*80)

        filtered_jobs = self.filter.filter_jobs(jobs, require_internship=True)

        logger.info(f"✓ {len(jobs)} total jobs → {len(filtered_jobs)} relevant UI/UX internships")

        # Show statistics
        stats = self.filter.get_statistics(filtered_jobs)
        if stats['total'] > 0:
            logger.info(f"  Average relevance score: {stats['average_score']:.2f}")
            logger.info(f"  Score range: {stats['score_range'][0]} - {stats['score_range'][1]}")

        return filtered_jobs

    def deduplicate_jobs(self, jobs: list) -> list:
        """
        Remove duplicate jobs

        Args:
            jobs: List of filtered jobs

        Returns:
            Deduplicated list of jobs
        """
        logger.info("\n" + "="*80)
        logger.info("PHASE 3: Deduplication")
        logger.info("="*80)

        unique_jobs = self.deduplicator.deduplicate(jobs)

        logger.info(f"✓ Removed {len(jobs) - len(unique_jobs)} duplicates")

        return unique_jobs

    def save_jobs_cache(self, jobs: list):
        """Save jobs to JSON cache file"""
        cache_data = {
            'last_updated': datetime.now().isoformat(),
            'total_jobs': len(jobs),
            'jobs': jobs
        }

        with open(self.jobs_cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)

        logger.info(f"✓ Saved {len(jobs)} jobs to {self.jobs_cache_file}")

    def generate_readme(self, jobs: list):
        """Generate and save README.md"""
        logger.info("\n" + "="*80)
        logger.info("PHASE 4: Generating README")
        logger.info("="*80)

        readme_content = self.markdown.generate_readme(jobs)

        readme_path = self.project_root / 'README.md'
        with open(readme_path, 'w') as f:
            f.write(readme_content)

        logger.info(f"✓ Generated README with {len(jobs)} internships")
        logger.info(f"  Saved to: {readme_path}")

    def run(self):
        """Execute the complete scraping pipeline"""
        logger.info("\n" + "="*80)
        logger.info("UI/UX INTERNSHIP SCRAPER")
        logger.info("="*80)
        logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            # Step 1: Scrape all sources
            all_jobs = self.scrape_all_sources()

            if not all_jobs:
                logger.warning("⚠ No jobs found from any source!")
                return

            # Step 2: Filter for relevance
            filtered_jobs = self.filter_jobs(all_jobs)

            if not filtered_jobs:
                logger.warning("⚠ No relevant UI/UX internships found after filtering!")
                return

            # Step 3: Deduplicate
            unique_jobs = self.deduplicate_jobs(filtered_jobs)

            # Step 4: Save cache
            self.save_jobs_cache(unique_jobs)

            # Step 5: Generate README
            self.generate_readme(unique_jobs)

            # Final summary
            logger.info("\n" + "="*80)
            logger.info("COMPLETE!")
            logger.info("="*80)
            logger.info(f"✓ {len(all_jobs)} jobs scraped")
            logger.info(f"✓ {len(filtered_jobs)} relevant internships")
            logger.info(f"✓ {len(unique_jobs)} unique listings")
            logger.info(f"✓ README.md updated")
            logger.info(f"\nFinished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            logger.error(f"✗ Error during scraping: {str(e)}", exc_info=True)
            sys.exit(1)


if __name__ == "__main__":
    scraper = InternshipScraper()
    scraper.run()
