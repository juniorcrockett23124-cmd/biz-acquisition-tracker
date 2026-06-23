# Biz Acquisition Tracker

Central workspace for sourcing, screening, and tracking small business acquisition targets.

## Current Focus

- Recurring revenue
- Team already in place
- 5+ years operating history
- Retiring owner preferred, ideally 60+
- $150K-$500K+ annual cash flow

## Structure

- `config/buy-box.json`: acquisition criteria and scoring weights
- `data/candidates.csv`: master list of sourced businesses
- `data/source-registry.md`: active, trial, and backlog sourcing channels
- `data/source-discovery/`: dated source-expansion research notes
- `data/underwriting/`: underwriting memos by company
- `data/research/`: deep research memos by company
- `data/daily-sourcing/`: dated sourcing snapshots
- `docs/workflow.md`: sourcing and diligence workflow
- `jobs/`: prompts and notes for scheduled jobs
- `scripts/`: local utilities for dashboard data and file maintenance
- `app/`: phone-friendly React dashboard
- `templates/outreach.md`: intro and diligence prompts

## Status Model

- `sourced`: found and logged
- `screening`: validating fit
- `qualified`: strong fit, worth outreach
- `contacted`: intro requested or broker reached
- `diligence`: in active review
- `pass`: rejected

## Notes

Seller age / retirement status is often not public. Treat that as a diligence field until verified.

Separate `company website` from `listing source`. A company URL is not the same thing as a for-sale listing or broker source URL.

Primary listing sources should be marketplace or broker URLs first: `BizBuySell`, `BusinessesForSale`, `BizQuest`, `BusinessBroker.net`, `SMB.co`, `Axial`, `Acquire.com`, `LoopNet`, and strong niche broker sites where relevant.

Track source expansion separately from daily prospecting:

- use `jobs/discover-sources.md` to find new marketplaces, aggregators, and niche broker sites
- record findings in `data/source-discovery/YYYY-MM-DD.md`
- update `data/source-registry.md` with `active`, `trial`, `backlog`, or `rejected` status

## Publish

The live dashboard is deployed from `main` via GitHub Pages.

- Local data refresh is not enough to update the website.
- After updating sourcing, underwriting, research, or dashboard output, publish the repo changes to `main`.
- Use `scripts/publish_latest.sh` to rebuild the dashboard, verify the app build, commit tracked and new output files, and push `main`.
