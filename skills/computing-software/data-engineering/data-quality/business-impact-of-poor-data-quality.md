---
id: computing-software.data-engineering.data-quality.business-impact-of-poor-data-quality
name: business-impact-of-poor-data-quality
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, dq-business-impact, cost-of-poor-quality, prioritisation, business-case]
level: advanced
status: draft
description: "Quantify the business impact and cost of poor data quality to prioritise fixes and fund DQ work: impact categories, estimation methods and a simple business case."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://hbr.org/2016/09/bad-data-costs-the-u-s-3-trillion-per-year
  - https://books.google.com/books?vid=ISBN9780123737175
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Business impact and cost of poor data quality

**Goal:** turn "data is messy" into money, risk and time numbers that decide what gets fixed first.

## Impact categories
- **Revenue**: lost sales (wrong prices, failed campaigns to bad contacts), churn from billing errors.
- **Cost**: rework and manual corrections (analyst hours reconciling), returned mail/shipments, duplicate payments.
- **Risk/compliance**: regulatory reporting errors, fines, privacy breaches from wrong data.
- **Decision quality**: wrong forecasts, misallocated budget, ML models trained on bad labels.
- **Trust/productivity**: teams building shadow datasets, time spent validating numbers before meetings.

## Estimate
1. Pick a concrete issue (e.g. 4% of customer addresses invalid).
2. Trace consequences: 4% of 200k shipments/year = 8,000 failed deliveries x 12 EUR re-shipping + 15 min support each.
3. Add time-to-detect and repair effort from incident records.
4. Express as a range (low/likely/high); be explicit about assumptions.
Also count **near misses**: issues caught before release still cost repair time.

## Prioritise
Score issues by impact x frequency x affected critical data elements, against effort to fix (at source vs downstream cleansing). Fixing at the source usually wins long term.

## Business case template
- Problem and evidence (metrics, incidents).
- Annual cost estimate with assumptions.
- Proposed fix (source validation, contracts, monitoring, ownership) and cost.
- Expected reduction and how it will be measured (DQ score, incident count, hours saved).

## Measure after
Track the same metrics after the fix: incidents, manual hours, DQ scores. Report realised savings; it funds the next round.

## Gotchas
- Big industry figures (trillions) do not persuade your CFO: use your own incidents.
- Ignoring opportunity cost: analysts validating data are not analysing.

## Verify
Top 5 DQ issues each have an impact estimate and an owner-approved priority.
