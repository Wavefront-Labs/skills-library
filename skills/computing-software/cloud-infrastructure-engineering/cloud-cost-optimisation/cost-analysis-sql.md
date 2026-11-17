---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-analysis-sql
name: cost-analysis-sql
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-reporting, cost-analysis-sql, athena, bigquery, cur-queries, focus-queries, sql, cost-explorer-api]
level: practitioner
status: docs-checked
description: "Answer cost questions with SQL over FOCUS/CUR/BigQuery exports: top services, day-over-day movers, cost by tag, commitment usage, with partition pruning to keep queries cheap."
sources: ["https://focus.finops.org/focus-specification/", "https://docs.aws.amazon.com/cur/latest/userguide/table-dictionary-cur2-line-item.html", "https://cloud.google.com/billing/docs/how-to/bq-examples"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost analysis queries

Examples on a FOCUS table `focus` (partitioned by billing period; the partitioning is your own table
design, not part of FOCUS). Date literals like `DATE '2026-10-01'` are engine syntax: FOCUS
`BillingPeriodStart` and `ChargePeriodStart` are Date/Time columns. Adapt column names for CUR 2.0
(`line_item_unblended_cost` is unblended rate times usage amount) or the Google Cloud BigQuery export
(net cost is `cost + IFNULL((SELECT SUM(c.amount) FROM UNNEST(credits) c),0)`; its partition field is
`_PARTITIONTIME`).

## Top services month to date
```sql
SELECT ServiceName, ROUND(SUM(EffectiveCost),2) AS cost
FROM focus
WHERE BillingPeriodStart = DATE '2026-10-01'
GROUP BY 1 ORDER BY 2 DESC LIMIT 20;
```

## Day-over-day movers (what changed yesterday)
```sql
WITH d AS (
  SELECT ServiceName, SubAccountId, CAST(ChargePeriodStart AS DATE) AS day, SUM(EffectiveCost) c
  FROM focus WHERE ChargePeriodStart >= current_date - INTERVAL '8' DAY
  GROUP BY 1,2,3)
SELECT ServiceName, SubAccountId,
       MAX(CASE WHEN day = current_date - INTERVAL '1' DAY THEN c END) AS yesterday,
       AVG(CASE WHEN day <  current_date - INTERVAL '1' DAY THEN c END) AS prior_avg
FROM d GROUP BY 1,2
ORDER BY yesterday - prior_avg DESC NULLS LAST LIMIT 20;
```

## Cost by team tag, unallocated visible
```sql
SELECT COALESCE(element_at(Tags, 'team'), '(untagged)') AS team, SUM(EffectiveCost) cost
FROM focus WHERE BillingPeriodStart = DATE '2026-09-01' GROUP BY 1 ORDER BY 2 DESC;
```
(FOCUS defines `Tags` as a JSON key-value column that may be null, and some tag keys are provider
prefixed. `element_at` assumes your engine loaded it as a map, as Athena can; otherwise use the
engine's JSON functions. Check how your provider names and prefixes the tag key.)

## Unused commitments
```sql
SELECT CommitmentDiscountId, SUM(EffectiveCost) AS wasted
FROM focus WHERE CommitmentDiscountStatus = 'Unused' AND ChargeCategory = 'Usage' AND BillingPeriodStart = DATE '2026-09-01'
GROUP BY 1 ORDER BY 2 DESC;
```

## Practice
- Always filter on the partition column — billing tables are large and the filter limits how much data a query reads.
- Exclude `ChargeCategory IN ('Tax','Purchase')` from usage analysis; include for reconciliation.
  `EffectiveCost` is amortized, so a prepaid commitment `Purchase` row has `EffectiveCost` 0, and
  unused commitment cost shows as `Usage` rows with `CommitmentDiscountStatus` = `Unused`.
- `EffectiveCost` totals for a period may not match the invoices; reconcile to invoices separately.
- Save validated queries in a shared library with owners.

## Verify
- [ ] Query totals match the console for the same filters.

## Checked
2026-11-08. Confirmed against the FOCUS v1.2 column pages for ServiceName, SubAccountId, BillingPeriodStart, ChargePeriodStart, EffectiveCost, Tags, ChargeCategory, CommitmentDiscountId and CommitmentDiscountStatus (names, types, allowed values), the CUR 2.0 line item dictionary (`line_item_unblended_cost`) and the Google Cloud billing BigQuery examples (credits `UNNEST` net cost, `_PARTITIONTIME`).
Removed: `product_servicecode` and `resource_tags['user_team']` (not on the pages read), the "billed by bytes scanned" claim, and the AWS query-library source (page not readable). The SQL is illustrative and was not executed.
Method: documentation only; no commands were run.
