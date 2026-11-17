---
id: computing-software.data-engineering.data-quality.defining-dq-rules-per-dimension
name: defining-dq-rules-per-dimension
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, dq-rule-definition, dq-dimensions, completeness, validity, uniqueness, timeliness, consistency, accuracy]
level: practitioner
status: gated
description: "Turn DAMA data quality dimensions into testable rules: completeness, validity, uniqueness, consistency, timeliness and accuracy, with SQL patterns and thresholds."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://www.iso.org/standard/35736.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining DQ rules per dimension

**Goal:** quality requirements stated as measurable rules with a metric, threshold, owner and action, instead of "data must be accurate".

## Rule template
| Field | Example |
|---|---|
| Rule id / name | `ORD-COMP-01 order customer_id populated` |
| Dimension | completeness |
| Data element | `sales.orders.customer_id` |
| Logic | % of rows where `customer_id is not null` |
| Threshold | >= 99.9% (warn < 99.95%) |
| Scope / filter | orders created in the last 1 day, excluding test channel |
| Owner | sales-data steward |
| Action on breach | block publish / alert / ticket |

## Dimension -> SQL patterns
**Completeness** (required values present, expected records present):
```sql
select 100.0 * count(customer_id) / count(*) as pct_populated from orders where order_date = :d;
select count(*) from expected_stores e left join daily_sales s using (store_id) where s.store_id is null;
```
**Validity** (format, domain, range):
```sql
select count(*) from customers where not regexp_like(email, '^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$');   -- doubled backslashes suit engines where a backslash escapes inside string literals (Snowflake, Spark, MySQL); on DuckDB/PostgreSQL standard strings use single backslashes: with doubled backslashes DuckDB flagged every valid address (tested)
select count(*) from orders where status not in ('NEW','PAID','SHIPPED','CANCELLED');
select count(*) from orders where amount < 0 or amount > 1e6;
```
**Uniqueness**:
```sql
select order_id, count(*) from orders group by 1 having count(*) > 1;
```
**Consistency** (across fields, tables, systems):
```sql
select count(*) from orders where shipped_at < ordered_at;
select count(*) from order_lines l left join orders o using (order_id) where o.order_id is null;   -- referential
select abs(sum(o.amount) - sum(l.line_amount)) from ...;                                           -- cross-table totals
```
**Timeliness / freshness**:
```sql
select timestampdiff(minute, max(_loaded_at), current_timestamp) as minutes_stale from orders;   -- MySQL/Snowflake/Spark spelling; DuckDB has no timestampdiff: datediff('minute', max(_loaded_at), current_timestamp) (tested)
```
**Accuracy** (matches reality/authoritative source): needs a reference: reconcile with source system totals, sample audits, third-party reference data (postal codes, FX rates).

## Choosing thresholds
- Start from profiling baselines (current observed rates), not 100%.
- Tie thresholds to business impact: a 0.1% missing customer_id may be fine for marketing, not for billing.
- Distinguish warn vs error; error should block downstream use or trigger an incident.

## Implementation
Express rules in your framework (dbt tests with `severity`/`warn_if`/`error_if`, Great Expectations, Soda checks, Snowflake DMFs, DLT expectations) (gated: unconfirmed, source is paywalled or blocked, for the last two) and keep the rule catalogue (id, owner, rationale) in the data catalog / YAML next to the code.

## Verify
- [ ] Every critical data element has at least completeness, validity and uniqueness/consistency rules with owners.
- [ ] Rule results are stored over time (scorecards), not only pass/fail in logs.
