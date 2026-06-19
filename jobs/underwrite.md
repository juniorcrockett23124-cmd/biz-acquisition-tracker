# Job 2: Underwrite Queue

## Goal

Underwrite each candidate on the master list that does not yet have an underwriting memo.

## Rules

1. Read `config/buy-box.json`.
2. Read `data/candidates.csv`.
3. Select candidates where:
   - `status` is `qualified`, `screening`, or `contacted`
   - `underwriting_status` is blank or `pending`
4. Create one memo per business in `data/underwriting/`.
5. Estimate:
   - revenue quality
   - cash flow quality
   - likely multiple attractiveness
   - seller financing attractiveness
   - key diligence gaps
   - preliminary pass / pursue recommendation
6. Update the candidate row with:
   - `underwriting_status`
   - `underwriting_score`
   - `last_reviewed`

## Output Template

- business overview
- why it fits
- likely risks
- key missing facts
- rough financing view
- preliminary verdict
