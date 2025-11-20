-- Migration: Add unique constraint on URL to prevent duplicate job listings
-- Created: 2025-11-20
-- Purpose: Prevent the same job (identified by URL) from being inserted multiple times
--          even if scrapers assign different IDs

-- Note: This will fail if there are existing duplicate URLs in the database.
-- If it fails, you'll need to manually clean up duplicates first:
--
--   DELETE FROM intern_jobs a USING intern_jobs b
--   WHERE a.id > b.id AND a.url = b.url;

-- Add unique constraint on URL
ALTER TABLE intern_jobs
ADD CONSTRAINT intern_jobs_url_unique UNIQUE (url);

-- Add index for faster URL lookups (if not created by unique constraint)
-- CREATE INDEX IF NOT EXISTS idx_intern_jobs_url ON intern_jobs(url);
-- (UNIQUE constraint automatically creates an index)
