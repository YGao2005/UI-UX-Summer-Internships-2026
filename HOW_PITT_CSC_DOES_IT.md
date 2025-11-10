# How Pitt CSC & Simplify Find High-Quality Job Postings

**Investigation Date:** 2025-11-10
**Your Current Results:** 24 UI/UX design internships
**Pitt CSC Results:** 1,725+ tech internships (503 Software Engineering alone)

---

## TL;DR - The Secret Sauce

**Pitt CSC uses crowdsourcing, not automation.** They have a community-driven model where hundreds of students manually submit job postings through GitHub issues. This is fundamentally different from your automated scraping approach.

---

## 🔍 Deep Dive: Their Methodology

### 1. Data Collection Approach

**Pitt CSC & Simplify:**
- **Crowdsourced submissions** via GitHub issues (not automated scraping)
- Contributors use a structured "New Internship" template
- Each job is manually submitted by students/community members
- Partnership with Simplify.jobs (proprietary job aggregation platform)
- Daily manual review and curation by Pitt CSC team + Simplify staff

**Your Current Approach:**
- Fully automated API scraping
- Runs on GitHub Actions daily
- Zero human intervention required
- Limited to companies with public APIs

### 2. Coverage & Scale

**Pitt CSC reaches companies YOU can't:**
- Microsoft, Apple, Google, Meta, Amazon (custom ATS systems)
- Adobe (Workday)
- Canva (SmartRecruiters)
- Netflix, Spotify (custom systems)
- Snap Inc, Atlassian (iCIMS)
- Shopify, Box, Zillow (custom systems)

**Your scraper limitations:**
- Only 39 companies with public APIs
- Cannot access custom ATS systems
- Missing FAANG companies entirely
- Missing most Fortune 500 companies

### 3. Quality Standards

**Pitt CSC submission requirements:**
- Must use formal ATS (Workday, Greenhouse, Ashby, etc.)
- Non-ATS platforms require Simplify team approval
- US/Canada/Remote locations only
- Categories: SWE, PM, Data Science, Quant Finance, Hardware, Other tech
- Human verification before adding to list
- Special indicators: 🔥 FAANG+, 🎓 Advanced degree, 🛂 No sponsorship, 🇺🇸 US citizenship

**Your current quality standards:**
- Keyword-based filtering for UI/UX design internships
- Relevance scoring algorithm
- Automated deduplication
- No human verification

### 4. The Numbers Game

| Metric | Pitt CSC | Your Scraper |
|--------|----------|--------------|
| Total Internships | 1,725+ | 24 |
| Companies | 100+ visible | 39 tracked |
| Update Frequency | Daily (manual) | Daily (automated) |
| Data Sources | Crowdsourced + Simplify API | 8 public APIs |
| Human Verification | Yes | No |
| Supports Custom ATS | Yes | No |

---

## 🎯 Why They Find More Jobs

### Reason #1: Human Network Effect
- Hundreds of students actively job hunting submit what they find
- Students apply to companies → find job → submit to list → others benefit
- Network effect: More users = More submissions = Better list = More users

### Reason #2: Simplify Partnership
- Simplify.jobs is a commercial job aggregation platform
- Likely has proprietary scraping infrastructure
- May have partnerships/data agreements with companies
- Can afford legal teams, infrastructure, anti-bot evasion
- You're competing with a funded startup's engineering resources

### Reason #3: Manual Curation Beats Automation
- Humans can navigate custom career portals
- Humans can verify job quality and relevance
- Humans can handle CAPTCHA, logins, JavaScript-heavy sites
- Humans can access Workday, SuccessFactors, Oracle Taleo
- Humans can spot and remove expired listings

### Reason #4: Broader Scope
- They track ALL tech internships (SWE, PM, Data, Quant, Hardware)
- Larger addressable market = More contributors
- More contributors = Better data quality
- You're focused on niche (UI/UX design only)

---

## 📊 Your Scraper's Strengths vs Weaknesses

### ✅ What You Do Well

1. **Fully Automated** - Zero manual work required
2. **Open Source** - Transparent, reproducible, customizable
3. **API-First** - Reliable, structured data from official sources
4. **Smart Filtering** - Relevance scoring for UI/UX specifically
5. **Free to Run** - GitHub Actions provides free compute
6. **Deduplication** - Handles multiple sources intelligently
7. **Niche Focus** - Specifically UI/UX design (less noise)

### ❌ Where You Fall Short

1. **API Limitations** - Only 39 companies accessible
   - Pitt CSC reaches 100+ companies
   - Missing all FAANG companies
   - Missing most Fortune 500 companies

2. **Cannot Access Custom ATS Systems**
   - Workday (Adobe, Airbnb, IBM, Oracle, VMware, etc.)
   - SuccessFactors (SAP, Cisco, Hewlett Packard)
   - Oracle Taleo (Boeing, Dell, HP, Intel)
   - iCIMS (Amazon sometimes, Atlassian)
   - Custom portals (Apple, Google, Meta, Microsoft, Netflix)

3. **No Human Verification**
   - Can't verify job quality
   - Can't spot outdated listings
   - Can't handle edge cases
   - Can't navigate ambiguous job titles

4. **Smaller Network Effect**
   - UI/UX niche vs all tech roles
   - No community submitting jobs
   - No viral growth mechanism

---

## 🚀 How to Close the Gap

### Option A: Hybrid Approach (Recommended)
**Add crowdsourcing to your automation:**

1. **Keep your automated scraping** (solid foundation)
2. **Add GitHub issue template** for manual submissions
   - Copy Pitt CSC's "New Internship" template
   - Let users submit jobs from Workday, custom ATS, etc.
   - Manual review + merge = Best of both worlds

3. **Benefits:**
   - Automation finds 70% of jobs
   - Community fills in the 30% gap (FAANG, custom ATS)
   - Still mostly automated
   - Can reach 50-100+ internships

### Option B: Expand Automation (Harder)
**Add more scrapers:**

1. **Workday Scraper** (hardest but highest impact)
   - Used by Adobe, Airbnb, IBM, Oracle, VMware, many more
   - Requires: JavaScript rendering, CAPTCHA handling, API reverse engineering
   - Risky: Workday actively blocks scrapers
   - Reward: 50-100+ additional companies

2. **University Job Boards**
   - Handshake (most universities)
   - WayUp (internship-focused)
   - Symplicity (career services)
   - May require university login credentials

3. **Design-Specific Boards**
   - Dribbble Jobs
   - Behance Jobs
   - Coroflot
   - AIGA Design Jobs

4. **More API Sources**
   - Indeed API (paid)
   - LinkedIn API (restricted)
   - Glassdoor API (no longer public)
   - Monster API (exists?)

### Option C: Partner with Simplify (Easiest)
**Why reinvent the wheel?**

1. Simplify already solved this problem
2. They have 1,700+ internships
3. They might have an API or data partnership program
4. Could white-label their data for UI/UX specifically

### Option D: Focus on Quality Over Quantity
**Accept the limitation, optimize for niche:**

1. Your 24 internships are all UI/UX design specific
2. Pitt CSC's 1,725 includes SWE, PM, Data, Quant, Hardware
3. Maybe 50-100 of theirs are actually UI/UX relevant
4. You might already be competitive in the niche

**Action items:**
- Filter Pitt CSC list for design roles → compare coverage
- Focus on design-forward companies (Figma, Linear, Notion)
- Add design-specific job boards
- Target quality: "Best UI/UX internships" not "Most internships"

---

## 📈 Realistic Expectations

### What You Can Achieve with Automation Alone:
- **30-50 internships** with optimal API scraping
- **50-100 internships** if you add Workday scraper (risky)
- **100-200 internships** if you add university job boards

### What Requires Human Network:
- **200+ internships** = Need crowdsourcing
- **500+ internships** = Need Simplify-level resources
- **1,000+ internships** = Need commercial platform + team

### The Hard Truth:
You're competing with:
1. A university club with 1,000+ active student members
2. A funded startup (Simplify) with engineering team, infrastructure, legal support
3. A community-driven network effect that took years to build

**You cannot beat them at scale with automation alone.**

---

## 🎓 Key Learnings from Pitt CSC

### 1. Crowdsourcing Works
- GitHub issues as submission mechanism is genius
- Low barrier to entry (anyone can submit)
- Version controlled, transparent, reviewable
- Community ownership creates sustainability

### 2. Manual Curation Adds Value
- Not everything should be automated
- Human judgment matters for quality
- Daily review catches errors automation misses
- Special indicators (🔥 🎓 🛂 🇺🇸) add context

### 3. Partnership Amplifies Reach
- Simplify partnership gives them proprietary data
- Commercial API access they couldn't afford alone
- Shared brand: "by Pitt CSC & Simplify"
- Win-win: Simplify gets traffic, Pitt CSC gets data

### 4. Broad Scope Attracts Contributors
- All tech roles = bigger audience
- Bigger audience = more contributors
- More contributors = better data
- Network effects compound

### 5. Sustainability Through Community
- Not dependent on one person maintaining scrapers
- Community ownership = longevity
- Public list = reputation = continued contributions
- Open source but curated = best of both worlds

---

## 💡 Recommendations

### Immediate Actions (This Week):

1. **Test the hypothesis: Are you actually behind?**
   - Filter Pitt CSC's 1,725 jobs for "design", "UI", "UX", "product design"
   - Compare company overlap
   - If they only have 30-40 design internships, you're competitive
   - If they have 100+, there's a real gap

2. **Analyze your 39 companies:**
   - Are these the RIGHT companies for UI/UX?
   - Should you track fewer companies but higher quality?
   - Add more design-forward startups (Linear, Framer, Miro)

3. **Add GitHub issue template for manual submissions:**
   - Copy Pitt CSC's template
   - Takes 30 minutes to implement
   - Start building community contribution pipeline
   - Hybrid approach = Best of both worlds

### Medium-term (This Month):

1. **Add design-specific job boards:**
   - Dribbble Jobs (has API)
   - Behance Jobs (Adobe network)
   - AIGA Design Jobs
   - Coroflot

2. **Research Simplify's API:**
   - Do they have a public/partner API?
   - Can you white-label their data?
   - Might save you months of engineering

3. **Expand Greenhouse/Ashby company list:**
   - There are 1,000+ companies using Greenhouse
   - Research design-forward companies
   - Startups often use Greenhouse/Ashby (cheaper than Workday)

### Long-term (Next Quarter):

1. **Decide on strategy:**
   - **Niche leader:** Best UI/UX internships (quality over quantity)
   - **Automation purist:** Never accept manual submissions
   - **Hybrid model:** Automation + crowdsourcing
   - **Commercial:** Partner with/compete with Simplify

2. **If pursuing scale, consider:**
   - Workday scraper (legal risks, technical complexity)
   - University job board integrations
   - Commercial API subscriptions (Indeed, ZipRecruiter)
   - Team/community building for manual curation

---

## 🎯 The Bottom Line

**Why Pitt CSC finds 1,725 internships:**
1. Crowdsourcing (not automation)
2. Simplify partnership (proprietary data)
3. Manual curation (humans beat bots for quality)
4. Broader scope (all tech roles, not just UI/UX)
5. Network effects (years of community building)

**Why you find 24 internships:**
1. Fully automated (no manual work)
2. Only 39 companies with public APIs
3. Cannot access custom ATS systems (Workday, etc.)
4. Niche focus (UI/UX only)
5. Solo project (no community network)

**Can you catch up?**
- Not at their scale (1,725) without crowdsourcing
- Maybe at UI/UX-specific scale (50-100) with more APIs
- Definitely in quality if you focus on best companies

**Should you try?**
- Depends on your goal:
  - **Learn automation?** You've already succeeded.
  - **Compete with Pitt CSC?** You need crowdsourcing.
  - **Best UI/UX list?** Focus on quality, not quantity.
  - **Commercial product?** You need significant investment.

**Best path forward:**
1. Add GitHub issue template (30 minutes)
2. Add 2-3 design-specific job boards (1-2 days)
3. Expand Greenhouse/Ashby company list (research afternoon)
4. Aim for 50-100 high-quality UI/UX internships
5. Position as "curated" not "comprehensive"

**Remember:** Pitt CSC took years and a community to build. Don't compare Day 1 to their Year 5.

---

## 📚 Resources

- **Pitt CSC GitHub:** https://github.com/SimplifyJobs/Summer2026-Internships
- **Simplify Jobs Platform:** https://simplify.jobs
- **Contributing Guidelines:** https://github.com/SimplifyJobs/Summer2026-Internships/blob/dev/CONTRIBUTING.md
- **Your Investigation Results:** See `INVESTIGATION_RESULTS.md` for your scraper's current status

---

**Last Updated:** 2025-11-10
**Next Review:** After implementing GitHub issue template and analyzing Pitt CSC's design-specific jobs
