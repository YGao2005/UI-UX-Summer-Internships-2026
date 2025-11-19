"""
Discord Webhook Notifier
Sends notifications about new internships and daily reminders
"""

import os
import logging
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class DiscordNotifier:
    """Send Discord notifications via webhook"""

    def __init__(self, webhook_url: Optional[str] = None):
        """
        Initialize Discord notifier

        Args:
            webhook_url: Discord webhook URL (or read from DISCORD_WEBHOOK_URL env var)
        """
        self.webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")

        if not self.webhook_url:
            logger.warning("Discord webhook URL not configured - notifications disabled")
            self.enabled = False
        else:
            self.enabled = True
            logger.info("Discord notifications enabled")

    def send_message(self, content: str, embeds: Optional[List[Dict]] = None) -> bool:
        """
        Send a message to Discord

        Args:
            content: Main message text
            embeds: Optional list of embed objects

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            logger.debug("Discord notifications disabled - skipping message")
            return False

        try:
            payload = {
                "content": content,
                "username": "Internship Tracker"
            }

            if embeds:
                payload["embeds"] = embeds

            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )

            if response.status_code == 204:
                logger.info("Discord notification sent successfully")
                return True
            else:
                logger.error(f"Discord notification failed: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error sending Discord notification: {e}")
            return False

    def send_daily_reminder(self, total_jobs: int = 0, jobs_today: int = 0) -> bool:
        """
        Send daily reminder to apply to internships

        Args:
            total_jobs: Total internships in database
            jobs_today: Number of internships posted today (by companies, based on posted_date)

        Returns:
            True if successful, False otherwise
        """
        # Create reminder message
        timestamp = datetime.now().strftime('%A, %B %d, %Y')

        if jobs_today > 0:
            content = f"@everyone **Daily Internship Reminder** \n\n**{jobs_today} internships posted today by companies!**\n\nRemember to check and apply to today's fresh opportunities!"
        else:
            content = f"@everyone **Daily Internship Reminder** \n\nNo new internships posted by companies today, but keep applying to existing opportunities!\n\nStay consistent and keep pushing!"

        # Create embed with statistics
        embed = {
            "title": "Internship Tracker Statistics",
            "color": 0x5865F2 if jobs_today > 0 else 0xFFA500,  # Blue if new jobs, orange otherwise
            "fields": [
                {
                    "name": "📊 Total Available",
                    "value": f"{total_jobs} internships",
                    "inline": True
                },
                {
                    "name": "🆕 Posted Today",
                    "value": f"{jobs_today} new" if jobs_today > 0 else "None today",
                    "inline": True
                }
            ],
            "footer": {
                "text": f"Updated on {timestamp}"
            },
            "timestamp": datetime.utcnow().isoformat()
        }

        return self.send_message(content, embeds=[embed])

    def send_new_jobs_notification(self, new_jobs: List[Dict[str, Any]], total_jobs: int) -> bool:
        """
        Send notification about newly found internships

        Args:
            new_jobs: List of new job dictionaries
            total_jobs: Total number of jobs in database

        Returns:
            True if successful, False otherwise
        """
        if not new_jobs:
            logger.info("No new jobs to notify about")
            return False

        # Limit to top 5 jobs to avoid message being too long
        jobs_to_show = new_jobs[:5]
        remaining = len(new_jobs) - len(jobs_to_show)

        content = f"@everyone **New UI/UX Internships Found!** \n\n{len(new_jobs)} new opportunities posted!"

        # Create embeds for each job
        embeds = []
        for job in jobs_to_show:
            company = job.get('company', 'Unknown Company')
            title = job.get('title', 'Unknown Title')
            location = job.get('location', 'Unknown Location')
            url = job.get('url', '')
            source = job.get('source', 'Unknown Source')
            salary = job.get('salary', 'Not specified')

            # Create title with link if URL available
            job_title = f"[{title}]({url})" if url else title

            embed = {
                "title": company,
                "description": job_title,
                "color": 0x00FF00,  # Green for new jobs
                "fields": [
                    {
                        "name": "Location",
                        "value": str(location) if location and str(location) != 'nan' else "Remote/Not specified",
                        "inline": True
                    },
                    {
                        "name": "Salary",
                        "value": str(salary) if salary and str(salary) != 'nan' else "Not specified",
                        "inline": True
                    },
                    {
                        "name": "Source",
                        "value": source,
                        "inline": True
                    }
                ]
            }

            embeds.append(embed)

        # Add summary embed
        if remaining > 0:
            summary_embed = {
                "description": f"_...and {remaining} more! Check the database for all opportunities._",
                "color": 0x5865F2,
                "footer": {
                    "text": f"Total internships available: {total_jobs}"
                }
            }
            embeds.append(summary_embed)

        return self.send_message(content, embeds=embeds)

    def send_scraper_success(self, stats: Dict[str, Any]) -> bool:
        """
        Send notification about successful scraper run

        Args:
            stats: Dictionary with scraper statistics

        Returns:
            True if successful, False otherwise
        """
        total_scraped = stats.get('total_scraped', 0)
        filtered = stats.get('filtered', 0)
        unique = stats.get('unique', 0)
        new_jobs = stats.get('new_jobs', 0)

        content = f"Scraper completed successfully!"

        embed = {
            "title": "Scraper Run Summary",
            "color": 0x00FF00,
            "fields": [
                {
                    "name": "Jobs Scraped",
                    "value": str(total_scraped),
                    "inline": True
                },
                {
                    "name": "Relevant (Filtered)",
                    "value": str(filtered),
                    "inline": True
                },
                {
                    "name": "Unique Jobs",
                    "value": str(unique),
                    "inline": True
                },
                {
                    "name": "New Jobs Found",
                    "value": str(new_jobs),
                    "inline": True
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }

        return self.send_message(content, embeds=[embed])

    def send_error_notification(self, error_msg: str) -> bool:
        """
        Send notification about scraper error

        Args:
            error_msg: Error message

        Returns:
            True if successful, False otherwise
        """
        content = f"**Scraper Error Occurred**"

        embed = {
            "title": "Error Details",
            "description": f"```{error_msg[:1000]}```",  # Limit to 1000 chars
            "color": 0xFF0000,  # Red for errors
            "timestamp": datetime.utcnow().isoformat()
        }

        return self.send_message(content, embeds=[embed])


if __name__ == "__main__":
    # Test the Discord notifier
    import logging
    logging.basicConfig(level=logging.INFO)

    # You need to set DISCORD_WEBHOOK_URL in your environment
    notifier = DiscordNotifier()

    if notifier.enabled:
        print("Testing daily reminder...")
        notifier.send_daily_reminder(total_jobs=92, jobs_today=5)

        print("\nTesting new jobs notification...")
        test_jobs = [
            {
                "company": "Figma",
                "title": "Product Design Intern",
                "location": "San Francisco, CA",
                "url": "https://www.figma.com/careers",
                "source": "Greenhouse",
                "salary": "$50-60/hr"
            },
            {
                "company": "Stripe",
                "title": "UX Design Intern",
                "location": "Remote",
                "url": "https://stripe.com/jobs",
                "source": "Greenhouse",
                "salary": "$55-65/hr"
            }
        ]
        notifier.send_new_jobs_notification(test_jobs, total_jobs=92)
    else:
        print("Discord webhook not configured. Set DISCORD_WEBHOOK_URL environment variable.")
