---
id: computing-software.data-engineering.etl-pipeline-design.restatements-and-versioned-outputs
name: restatements-and-versioned-outputs
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, late-arriving-data, restatement, versioned-outputs, bitemporal, as-of-reporting, period-close, snapshot-tables, reproducibility]
level: advanced
status: draft
description: "Handle restatements when late or corrected data changes published numbers: closed periods, versioned snapshots, bitemporal tables, as-of queries, and communicating changes."
sources:
  - https://martinfowler.com/articles/bitemporal-history.html
  - https://docs.snowflake.com/en/user-guide/data-time-travel
  - https://iceberg.apache.org/docs/latest/branching/
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Restatements and versioned outputs

**Goal:** when late or corrected data changes a number that was already reported, you can show both the original and the restated figure, explain the difference, and reproduce any past report exactly.

## 1. Decide the policy per output (with the business owner)
| Policy | Behaviour | Typical for |
|---|---|---|
| Always current | late data silently updates history | operational dashboards |
| Closed periods | after close (e.g. month-end + 5 business days), period is frozen; corrections post to the current period as adjustments | finance, regulatory |
| Restate with versions | history may change, but every published version is kept | KPIs reported externally, ML training sets |
Write it down per table; "always current" is the accidental default and surprises auditors.

## 2. Versioned snapshots (simplest)
Publish each reporting run as an immutable snapshot:
```sql
INSERT INTO marts.kpi_monthly_snapshots
SELECT 'v2026_10_05' AS version, current_timestamp() AS published_at, k.*
FROM marts.kpi_monthly k;
```
- Reports cite the version; "latest" is a view over the newest version.
- Restatement report: diff current version vs previously published one by key and measure.
- Table-format alternatives: Iceberg tags (`CREATE TAG v2026_10 ...`), Delta/Snowflake time travel (bounded by retention — not a long-term archive).

## 3. Bitemporal facts (when you need "as known at")
Two time axes:
- **valid time** — when the fact was true in the business (`order_date`, `valid_from/valid_to`);
- **transaction/recorded time** — when the warehouse learned it (`recorded_from/recorded_to`).
Corrections close the old row's recorded interval and insert a new row; nothing is updated in place.
```sql
-- what did we believe on 2026-10-01 about September revenue?
SELECT SUM(amount) FROM fct_revenue_bt
WHERE order_date BETWEEN '2026-09-01' AND '2026-09-30'
  AND recorded_from <= '2026-10-01' AND (recorded_to > '2026-10-01' OR recorded_to IS NULL);
```

## 4. Closed periods with adjustments
- Add `posting_period` alongside `business_date`. After close, late records get `posting_period = current open period` and a flag `is_prior_period_adjustment`.
- Reports by posting period never change after close; reports by business date show the restated view. Show both clearly labelled.

## 5. Mechanics and communication
- Reprocess affected windows only (lookback on late data), but always regenerate the comparison against the last published version.
- Restatement threshold: auto-publish changes under X% / $Y; above it, require owner sign-off and a release note ("September revenue restated from 1.20M to 1.23M due to late partner file").
- Keep the inputs reproducible (pinned source snapshots, code version in the output row) so any version can be regenerated.

## Verify
- [ ] Each published table has a documented restatement policy.
- [ ] A past published report can be reproduced exactly (version or as-of query).
- [ ] Restatement diffs above threshold generate a notification to the owner.
