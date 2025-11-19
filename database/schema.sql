-- Internship Tracker Database Schema for Supabase
-- Prefix: intern_ to avoid conflicts with other tables in shared database

-- Table 1: Store all internship job data
CREATE TABLE IF NOT EXISTS intern_jobs (
    id TEXT PRIMARY KEY,  -- Job ID from scraper (e.g., "jobspy_glassdoor_123")
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT,
    url TEXT NOT NULL,
    description TEXT,
    posted_date DATE,
    scraped_date DATE NOT NULL DEFAULT CURRENT_DATE,
    source TEXT,
    job_type TEXT DEFAULT 'internship',
    salary TEXT,
    relevance_score INTEGER,
    score_breakdown JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table 2: Track which jobs have been posted to Discord
CREATE TABLE IF NOT EXISTS intern_posted_jobs (
    id SERIAL PRIMARY KEY,
    job_id TEXT NOT NULL REFERENCES intern_jobs(id) ON DELETE CASCADE,
    discord_channel_id TEXT NOT NULL,
    discord_message_id TEXT NOT NULL,
    posted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(job_id, discord_channel_id)  -- Prevent duplicate posts in same channel
);

-- Table 3: Track Discord users
CREATE TABLE IF NOT EXISTS intern_users (
    discord_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_active TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table 4: Track user applications
CREATE TABLE IF NOT EXISTS intern_applications (
    id SERIAL PRIMARY KEY,
    user_discord_id TEXT NOT NULL REFERENCES intern_users(discord_id) ON DELETE CASCADE,
    job_id TEXT NOT NULL REFERENCES intern_jobs(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'applied' CHECK (status IN ('applied', 'interviewing', 'offer', 'rejected', 'withdrawn')),
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    notes TEXT,
    UNIQUE(user_discord_id, job_id)  -- One application per user per job
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_intern_jobs_scraped_date ON intern_jobs(scraped_date DESC);
CREATE INDEX IF NOT EXISTS idx_intern_jobs_company ON intern_jobs(company);
CREATE INDEX IF NOT EXISTS idx_intern_jobs_relevance ON intern_jobs(relevance_score DESC);
CREATE INDEX IF NOT EXISTS idx_intern_posted_jobs_job_id ON intern_posted_jobs(job_id);
CREATE INDEX IF NOT EXISTS idx_intern_applications_user ON intern_applications(user_discord_id);
CREATE INDEX IF NOT EXISTS idx_intern_applications_job ON intern_applications(job_id);
CREATE INDEX IF NOT EXISTS idx_intern_applications_status ON intern_applications(status);

-- View: User statistics (computed on-the-fly)
CREATE OR REPLACE VIEW intern_user_stats AS
SELECT
    u.discord_id,
    u.username,
    COUNT(a.id) as total_applications,
    COUNT(CASE WHEN a.status = 'applied' THEN 1 END) as applied_count,
    COUNT(CASE WHEN a.status = 'interviewing' THEN 1 END) as interviewing_count,
    COUNT(CASE WHEN a.status = 'offer' THEN 1 END) as offer_count,
    COUNT(CASE WHEN a.status = 'rejected' THEN 1 END) as rejected_count,
    COUNT(CASE WHEN DATE(a.applied_at) >= CURRENT_DATE - INTERVAL '7 days' THEN 1 END) as applications_this_week,
    COUNT(CASE WHEN DATE(a.applied_at) >= CURRENT_DATE - INTERVAL '30 days' THEN 1 END) as applications_this_month,
    MIN(a.applied_at) as first_application,
    MAX(a.applied_at) as last_application,
    COUNT(DISTINCT j.company) as unique_companies
FROM intern_users u
LEFT JOIN intern_applications a ON u.discord_id = a.user_discord_id
LEFT JOIN intern_jobs j ON a.job_id = j.id
GROUP BY u.discord_id, u.username;

-- Function: Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_intern_jobs_updated_at
    BEFORE UPDATE ON intern_jobs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_intern_applications_updated_at
    BEFORE UPDATE ON intern_applications
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE intern_jobs IS 'Stores all scraped internship job listings';
COMMENT ON TABLE intern_posted_jobs IS 'Tracks which jobs have been posted to Discord to prevent duplicates';
COMMENT ON TABLE intern_users IS 'Discord users using the internship tracker';
COMMENT ON TABLE intern_applications IS 'User application tracking and status';
COMMENT ON VIEW intern_user_stats IS 'Aggregated statistics per user for /stats command';
