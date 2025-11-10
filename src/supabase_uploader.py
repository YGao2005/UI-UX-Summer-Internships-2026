"""
Supabase Uploader - Uploads scraped internships to Supabase database
Designed to run after main.py completes scraping
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseUploader:
    def __init__(self):
        """Initialize Supabase client"""
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError(
                "Missing Supabase credentials. Set SUPABASE_URL and SUPABASE_KEY in .env"
            )

        self.client: Client = create_client(supabase_url, supabase_key)
        self.uploaded_count = 0
        self.updated_count = 0
        self.error_count = 0

    def load_jobs_from_file(self, file_path: str = "data/jobs.json") -> List[Dict[str, Any]]:
        """Load jobs from jobs.json file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                jobs = data.get('jobs', [])
                print(f"✓ Loaded {len(jobs)} jobs from {file_path}")
                return jobs
        except FileNotFoundError:
            print(f"✗ Error: {file_path} not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"✗ Error parsing JSON: {e}")
            sys.exit(1)

    def transform_job_for_database(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Transform job data to match database schema"""
        return {
            'id': job.get('id'),
            'title': job.get('title'),
            'company': job.get('company'),
            'location': job.get('location'),
            'url': job.get('url'),
            'description': job.get('description'),
            'posted_date': job.get('posted_date'),
            'scraped_date': datetime.now().date().isoformat(),
            'source': job.get('source'),
            'job_type': job.get('job_type', 'internship'),
            'salary': job.get('salary'),
            'relevance_score': job.get('relevance_score'),
            'score_breakdown': job.get('score_breakdown'),  # JSONB field
        }

    def upload_jobs(self, jobs: List[Dict[str, Any]]) -> None:
        """Upload jobs to Supabase using upsert"""
        if not jobs:
            print("⚠ No jobs to upload")
            return

        print(f"\n⬆ Uploading {len(jobs)} jobs to Supabase...")

        # Transform all jobs
        transformed_jobs = [self.transform_job_for_database(job) for job in jobs]

        # Batch upsert (insert or update if exists)
        try:
            # Supabase upsert: insert new rows or update existing ones
            response = self.client.table('intern_jobs').upsert(
                transformed_jobs,
                on_conflict='id'  # Use job ID as conflict resolution
            ).execute()

            self.uploaded_count = len(response.data)
            print(f"✓ Successfully upserted {self.uploaded_count} jobs")

        except Exception as e:
            print(f"✗ Error during batch upload: {e}")
            print("⚠ Falling back to individual uploads...")
            self._upload_jobs_individually(transformed_jobs)

    def _upload_jobs_individually(self, jobs: List[Dict[str, Any]]) -> None:
        """Fallback: Upload jobs one by one"""
        for i, job in enumerate(jobs, 1):
            try:
                response = self.client.table('intern_jobs').upsert(
                    job,
                    on_conflict='id'
                ).execute()

                if response.data:
                    self.uploaded_count += 1
                    if i % 10 == 0:
                        print(f"  Progress: {i}/{len(jobs)} jobs uploaded")

            except Exception as e:
                self.error_count += 1
                print(f"  ✗ Error uploading job {job.get('id', 'unknown')}: {e}")

    def get_statistics(self) -> Dict[str, int]:
        """Get database statistics"""
        try:
            # Count total jobs
            response = self.client.table('intern_jobs').select('id', count='exact').execute()
            total_jobs = response.count

            # Count jobs scraped today
            today = datetime.now().date().isoformat()
            response = self.client.table('intern_jobs').select(
                'id', count='exact'
            ).eq('scraped_date', today).execute()
            jobs_today = response.count

            # Count total users
            response = self.client.table('intern_users').select('discord_id', count='exact').execute()
            total_users = response.count

            # Count total applications
            response = self.client.table('intern_applications').select('id', count='exact').execute()
            total_applications = response.count

            return {
                'total_jobs': total_jobs,
                'jobs_today': jobs_today,
                'total_users': total_users,
                'total_applications': total_applications
            }
        except Exception as e:
            print(f"⚠ Error fetching statistics: {e}")
            return {}

    def print_summary(self, stats: Dict[str, int]) -> None:
        """Print upload summary"""
        print("\n" + "="*50)
        print("📊 UPLOAD SUMMARY")
        print("="*50)
        print(f"Uploaded/Updated: {self.uploaded_count}")
        print(f"Errors:           {self.error_count}")
        print("\n📈 DATABASE STATISTICS")
        print("-"*50)
        if stats:
            print(f"Total jobs in DB:      {stats.get('total_jobs', 'N/A')}")
            print(f"Jobs scraped today:    {stats.get('jobs_today', 'N/A')}")
            print(f"Total users:           {stats.get('total_users', 'N/A')}")
            print(f"Total applications:    {stats.get('total_applications', 'N/A')}")
        print("="*50 + "\n")


def main():
    """Main execution"""
    print("\n🚀 Starting Supabase Upload...")
    print("-"*50)

    try:
        uploader = SupabaseUploader()

        # Load jobs from file
        jobs = uploader.load_jobs_from_file()

        # Upload to Supabase
        uploader.upload_jobs(jobs)

        # Get and print statistics
        stats = uploader.get_statistics()
        uploader.print_summary(stats)

        # Exit with appropriate code
        if uploader.error_count > 0:
            print(f"⚠ Completed with {uploader.error_count} errors")
            sys.exit(1)
        else:
            print("✓ Upload completed successfully!")
            sys.exit(0)

    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
