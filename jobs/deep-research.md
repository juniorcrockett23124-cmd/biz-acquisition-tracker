# Job 3: Deep Research

## Goal

Produce decision-useful research memos for prospects that have already been underwritten.

## Rules

1. Read `config/buy-box.json`.
2. Read `data/candidates.csv`.
3. Select candidates where:
   - `underwriting_status` is `complete`
   - `research_status` is blank or `pending`
4. Create one memo per business in `data/research/`.
5. Research:
   - company quality and brand reputation
   - industry attractiveness
   - likely customer profile
   - competitive landscape
   - possible operational traps
   - what would matter in an owner call
6. Update the candidate row with:
   - `research_status`
   - `research_score`
   - `last_reviewed`

## Output Template

- core thesis
- market and industry notes
- what is attractive
- what is dangerous
- must-ask diligence questions
- buy / watch / pass recommendation
