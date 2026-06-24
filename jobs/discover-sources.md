# Job 0: Discover Sources

## Goal

Expand the sourcing funnel by finding additional high-signal listing marketplaces, broker sites, and niche aggregators that may surface better acquisition targets.

## Current Active Universe

- BizBuySell
- BusinessesForSale
- SMB.co

## Configured / Intended Universe

- BizBuySell
- BusinessesForSale
- BizQuest
- BusinessBroker.net
- SMB.co
- Axial
- Acquire.com
- LoopNet
- niche broker sites
- targeted web searches for retiring owners and industry-specific firms

## What Good New Sources Look Like

Prioritize sources that:

- publish real for-sale listings, not generic lead-gen pages
- expose enough detail to screen quickly: cash flow, revenue, tenure, team, seller motivation, or financing
- fit small business acquisitions rather than venture-backed startups or franchise spam
- over-index toward accounting, bookkeeping, payroll, MSP, property management, and service businesses with repeat revenue
- allow repeated reuse instead of one-off manual digging

## Rules

1. Read `config/buy-box.json` and `data/source-registry.md` first.
2. Avoid rediscovering sources already marked `active` or `rejected` unless there is a material reason to revisit them.
3. Search for both broad marketplaces and niche channels:
   - regional business brokers
   - accounting / CPA practice brokers
   - MSP / IT services M&A brokers
   - property management business brokers
   - retiree-owner / succession-focused brokerages
4. For each candidate source, capture:
   - source name
   - source URL
   - type: marketplace, broker, niche broker, aggregator, targeted search
   - category fit
   - detail quality
   - reasons it may be useful
   - risks or weaknesses
   - recommended status: `active`, `trial`, `backlog`, or `rejected`
5. Prefer quality over volume. Five strong new sources are better than fifty weak directories.
6. If a source is promising but unproven, mark it `trial` rather than `active`.
7. If a source repeatedly lacks detail or produces weak leads, mark it `rejected` and explain why.

## Output

- create or update `data/source-discovery/YYYY-MM-DD.md`
- update `data/source-registry.md`
- if a source is approved for use, add it to `jobs/source-and-qualify.md`
