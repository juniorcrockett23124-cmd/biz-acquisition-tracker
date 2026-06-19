# Job 1: Source And Qualify

## Goal

Daily find businesses that fit the buy box and add only credible prospects to the master list.

## Sources

- BizBuySell
- BusinessesForSale
- BizQuest
- BusinessBroker.net
- SMB.co
- Axial for larger lower-middle-market opportunities
- Acquire.com for SaaS or software-like service businesses
- LoopNet for business-with-real-estate situations
- niche broker sites
- targeted web searches for retiring owners and industry-specific firms

## Rules

1. Read `config/buy-box.json` first.
2. Read `data/candidates.csv` and avoid duplicates.
3. Prefer businesses with evidence of:
   - recurring or repeatable revenue
   - a team already in place
   - 5+ years in business
   - likely retiring seller
   - $150K-$500K+ cash flow
4. Add new records with status `sourced` or `screening`.
5. If a prospect clearly fits, move status to `qualified`.
6. Write a dated summary file in `data/daily-sourcing/YYYY-MM-DD.md`.
7. Do not fabricate owner age or retirement status. Mark it `Unverified` unless explicitly supported.
8. Capture the actual source of the prospect separately from the company website:
   - `listing_source_name`: marketplace, broker, or source site name
   - `listing_source_url`: exact listing or source page URL
   - if no live for-sale listing exists, explicitly mark the prospect as sourced from company website / targeted web search

## Output

- update `data/candidates.csv`
- create or update `data/daily-sourcing/YYYY-MM-DD.md`
- refresh dashboard data
