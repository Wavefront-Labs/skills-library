---
id: computing-software.data-engineering.data-quality.monitors-as-code
name: monitors-as-code
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, monitors-as-code, sodacl, configuration-as-code, ci-cd]
level: practitioner
status: docs-checked
description: "Define data quality monitors as code (SodaCL, Monte Carlo monitors YAML, dbt tests, GX suites) in version control with review, CI validation and environment promotion."
sources:
  - https://docs.soda.io/soda-cl/soda-cl-overview.html
  - https://docs.getmontecarlo.com/docs/monitors-as-code
  - https://docs.greatexpectations.io/docs/core/introduction/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitors as code

**Goal:** data quality monitors are reviewed, versioned and deployed like pipeline code, not clicked together in a UI and forgotten.

## Examples
SodaCL:
```yaml
# checks/orders.yml
checks for analytics.fct_orders:
  - row_count > 0
  - freshness(loaded_at) < 2h
  - duplicate_count(order_id) = 0
  - missing_count(customer_id) = 0
```
```bash
soda scan -d snowflake_prod -c configuration.yml checks/orders.yml
```
Monte Carlo monitors-as-code: see the Monte Carlo monitors-as-code documentation for the YAML format and CLI.
dbt tests and Great Expectations suites are monitors as code too.

## Practices
- Keep monitors next to the model code they protect (same repo/PR), so a model change updates its monitors.
- Ownership/routing metadata in the files (`owner`, `severity`, `channel`).
- CI: run the checks against a CI data source on each PR, and fail PRs that add critical models without monitors (policy check).
- Promotion: same files applied to staging then prod with environment-specific data sources.
- UI-created monitors: periodically export/import them into code or forbid UI creation for production tables.

## Gotchas
- Anomaly monitors need history: new tables start in a learning period.

## Verify
A PR that changes a check shows the diff in review; after merge, the monitor in the platform matches the file.

## Checked

2026-10-28. Confirmed in the SodaCL overview: `checks for <dataset>:` syntax, `freshness(column) < 24h`, `duplicate_count(column) = 0`, `missing_count(column)`. Removed: the Monte Carlo YAML and CLI example, `montecarlo monitors apply --dry-run`, the namespace-replacement claim, `anomaly detection for row_count` and `missing_percent` (not confirmed in fetched pages; the Great Expectations page returned a stub).

Method: documentation only; no commands were run.
