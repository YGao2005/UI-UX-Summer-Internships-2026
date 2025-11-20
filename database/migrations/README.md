# Database Migrations

This directory contains SQL migrations for the internship tracker database.

## Applying Migrations

### Via Supabase Dashboard (Recommended)

1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor** (left sidebar)
3. Open the migration file and copy its contents
4. Paste into the SQL Editor
5. Click **Run** to execute

### Migration List

| Migration | Description | Date |
|-----------|-------------|------|
| `001_add_url_unique_constraint.sql` | Add unique constraint on URL to prevent duplicate jobs | 2025-11-20 |

## 001_add_url_unique_constraint.sql

**Purpose:** Prevent duplicate job listings by enforcing URL uniqueness

**Why this is needed:**
- Different scrapers may assign different IDs to the same job
- The same job URL appearing multiple times causes database bloat
- URL-based deduplication is more reliable than ID-based

**What it does:**
- Adds a `UNIQUE` constraint on the `url` column
- Automatically creates an index for faster URL lookups

**Before applying:**

If you have existing duplicate URLs in your database, the migration will fail. Clean them up first:

```sql
-- Find duplicate URLs
SELECT url, COUNT(*) as count
FROM intern_jobs
GROUP BY url
HAVING COUNT(*) > 1
ORDER BY count DESC;

-- Delete duplicates, keeping the most recent one
DELETE FROM intern_jobs a USING (
  SELECT MIN(id) as id, url
  FROM intern_jobs
  GROUP BY url
  HAVING COUNT(*) > 1
) b
WHERE a.url = b.url AND a.id != b.id;
```

**After applying:**

The uploader will now use URL-based deduplication instead of ID-based. When the same job is scraped from multiple sources, it will update the existing record instead of creating a duplicate.

## Rollback (if needed)

To rollback migration 001:

```sql
ALTER TABLE intern_jobs DROP CONSTRAINT IF EXISTS intern_jobs_url_unique;
```

⚠️ **Warning:** Rolling back will allow duplicate URLs again.

## Future Migrations

When adding new migrations:
1. Use sequential numbering: `002_migration_name.sql`, `003_migration_name.sql`, etc.
2. Include a descriptive comment at the top explaining the purpose
3. Update this README with the new migration
4. Test on a development database first
