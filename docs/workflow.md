# Workflow

## 0. Expand The Source Stack

Periodically search for new acquisition marketplaces, aggregators, and niche broker sites that fit the buy box.

- Record candidate sources in `data/source-discovery/YYYY-MM-DD.md`
- Promote proven channels into `data/source-registry.md`
- Feed approved sources into the daily sourcing job

## 1. Source

Search marketplaces and note any business that appears to fit the target profile.

## 2. Screen

Check for:

- recurring or repeatable revenue
- evidence of a team
- years in business
- cash flow range
- likely owner-retirement signal

## 3. Qualify

Move to `qualified` if:

- annual cash flow is within target range
- operating history is 5+ years
- recurring revenue is likely
- business does not look like a solo-owner job masquerading as a company

## 4. Diligence Questions

- Is the owner actively retiring?
- Owner age?
- How many full-time employees?
- Revenue mix: recurring vs project-based?
- Customer concentration?
- Any seller financing?
- Why is the business being sold now?
- What is owner involvement today?

## 5. Ranking Heuristics

- Accounting / bookkeeping / payroll: high priority
- Managed IT / MSP: high priority
- HVAC with service contracts and dispatch staff: high priority
- Brokerage-heavy, personality-led, or thin-team businesses: lower priority

## 6. Publish The Dashboard

- Rebuild dashboard data after candidate changes.
- Verify the React app still builds.
- Push the updated repo state to `main` so GitHub Pages redeploys the live site.
- Preferred path: run `scripts/publish_latest.sh`.
