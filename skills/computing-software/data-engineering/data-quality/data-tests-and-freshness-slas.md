---
id: computing-software.data-engineering.data-quality.data-tests-and-freshness-slas
name: data-tests-and-freshness-slas
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, data-testing, data-observability, freshness, source-freshness, sla, slo, volume-anomaly, schema-drift, dbt-tests, data-tests, great-expectations, gx, soda, soda-core, data-contracts, severity, warn-vs-error, quarantine, dead-letter, unique, not-null, referential-integrity, accepted-values]
level: practitioner
status: gated
description: "Set up data tests that catch real breakage: core check categories, dbt/Great Expectations/Soda checks, freshness and volume SLAs, data contracts, warn vs error severity and quarantine."
sources:
  - https://docs.getdbt.com/docs/build/data-tests
  - https://docs.getdbt.com/reference/resource-properties/freshness
  - https://docs.greatexpectations.io/docs/
  - https://docs.soda.io/
  - https://docs.getdbt.com/docs/collaborate/govern/model-contracts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data tests and freshness SLAs — know before your stakeholders do

**Goal:** a small, high-signal set of automated checks that stops bad data at the right layer, alerts the owner, and makes "is the dashboard up to date?" answerable from a number.

## 1. Cover the check categories that actually break
1. **Freshness:** the latest record is recent enough.
2. **Volume:** row counts within expected range for the period.
3. **Schema:** expected columns and types present (drift detection).
4. **Uniqueness / grain:** primary key unique; no duplicate grain.
5. **Completeness:** `not_null` on required fields; null rate below a threshold on optional ones.
6. **Validity:** accepted values, ranges, formats (`amount >= 0`, ISO country codes).
7. **Referential integrity:** every fact foreign key exists in its dimension.
8. **Reconciliation:** totals match the source system (counts, sum of amounts) for a period.
Start with 1, 2, 4 and 7 on every important table — they catch most incidents.

## 2. dbt tests
```yaml
# models/marts/schema.yml
models:
  - name: fct_orders
    columns:
      - name: order_id
        data_tests: [unique, not_null]        # "tests:" in dbt < 1.8 (gated: unconfirmed, source is paywalled or blocked)
      - name: customer_id
        data_tests:
          - relationships:
              arguments: {to: "ref('dim_customer')", field: customer_id}   # dbt 1.12: args nested under `arguments`
      - name: status
        data_tests:
          - accepted_values:
              arguments:
                values: ['placed', 'shipped', 'cancelled']
              config: {severity: warn}
```
Run with dbt-core 1.12.6 + dbt-duckdb 1.11.0: top-level `to:`/`values:` still run but emit `MissingArgumentsPropertyInGenericTestDeprecation` ("Arguments to generic tests should be nested under the `arguments` property"); the nested form ran fine, `severity: warn` gave WARN and `warn_if`/`error_if` worked (a failing `unique` test gave ERROR). Source freshness with a 3-hour-old `_loaded_at` gave WARN under `warn_after: 2 hours`.
- Custom checks: a singular test is any SQL in `tests/` that returns failing rows.
- Packages like `dbt_utils` / `dbt_expectations` add row-count, recency and range tests.
- `dbt build` runs tests right after each model, so downstream models are skipped when an upstream test errors (tested: a model selecting from a model with a failing `unique` test showed SKIP).
- Thresholds: `config: {severity: error, warn_if: ">0", error_if: ">100"}` to tolerate a few known-bad rows.

## 3. Freshness SLAs
```yaml
sources:
  - name: shop
    loaded_at_field: _loaded_at
    freshness:
      warn_after: {count: 2, period: hour}
      error_after: {count: 6, period: hour}
    tables:
      - name: orders
```
Run `dbt source freshness` on a schedule (independent of the main build — a stuck pipeline won't run its own checks).
- Define the SLA from the consumer's need ("finance dashboard reflects yesterday by 07:00 UTC") and derive thresholds backwards from it.
- **Gotcha:** `loaded_at_field` should be ingestion time, not business event time — a quiet sales day isn't a stale pipeline. Weekends and holidays need tolerance or calendars.

## 4. Volume and anomaly checks
- Static bounds (`row_count between 50k and 500k`) for stable tables.
- Relative checks: today's count vs trailing 7-day same-weekday average, alert beyond ±30–50% (tune from history).
- Great Expectations (`ExpectTableRowCountToBeBetween`, `ExpectColumnValuesToNotBeNull` in the 1.x API, snake-case names in 0.x) or Soda v3 SodaCL (`row_count > 0`, `anomaly detection for row_count` (gated: unconfirmed, source is paywalled or blocked)) cover these outside dbt. GX's API changed substantially in 1.0 — pin and follow your version's docs.
- Observability platforms learn baselines automatically; useful at scale, but keep explicit tests for business rules.

## 5. Severity: warn vs error
- **Error (block):** violations that make downstream numbers wrong — duplicate keys, broken grain, missing partitions, schema breakage.
- **Warn (notify):** degradations someone should look at — new enum value, slight null-rate rise, minor freshness delay.
- Every test has an owner and a route (channel/pager). A warning nobody reads is noise; delete or promote it.
- **Gotcha:** alert fatigue kills data quality programs. Review noisy tests monthly.

## 6. Quarantine instead of all-or-nothing
For row-level validity failures, split rather than stop: valid rows continue, invalid rows go to a `_quarantine` table with the rule that failed and the run id. Fail the run only if quarantine volume crosses a threshold (e.g. > 1%). See computing-software.data-engineering.etl-pipeline-design.idempotent-incremental-loads.

## 7. Data contracts
Agree with producers on schema, semantics, freshness and ownership at the boundary. Enforce in code: dbt model contracts (`contract: {enforced: true}` with declared `data_type`s fail the build on mismatch; tested with a double column vs declared decimal; constraints are not applied to views: dbt warns "Constraint types are not supported for view materializations"), schema registry compatibility rules for Kafka topics, CI checks on producer schema changes. Contracts move breakage left to the producer's PR instead of your 3 a.m. pager.

## Verify
- [ ] Every mart has primary-key `unique` + `not_null` and FK `relationships` tests.
- [ ] Source freshness runs on its own schedule and alerts to a named owner.
- [ ] Deliberately inserting a duplicate key in dev causes `dbt build` to fail and skip downstream models.
- [ ] A volume check fires when a day's load is truncated to half (tested by simulation).
- [ ] Each test has a documented severity and alert route; warn-level tests were reviewed in the last month.
