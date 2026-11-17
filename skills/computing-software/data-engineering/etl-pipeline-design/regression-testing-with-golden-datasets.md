---
id: computing-software.data-engineering.etl-pipeline-design.regression-testing-with-golden-datasets
name: regression-testing-with-golden-datasets
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, golden-dataset, regression-testing, snapshot-testing, pipeline-testing]
level: advanced
status: draft
description: "Regression-test pipelines against golden datasets: curating inputs and expected outputs, deterministic runs, comparing with tolerances, and updating goldens deliberately."
sources:
  - https://docs.getdbt.com/docs/build/unit-tests
  - https://github.com/dbt-labs/dbt-audit-helper
  - https://docs.pytest.org/en/stable/how-to/fixtures.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Regression testing with golden datasets

**Goal:** refactors and upgrades (engine, dbt, Spark versions) do not change outputs unintentionally.

## Build the golden set
- **Inputs**: a small, representative, anonymised extract covering edge cases: nulls, duplicates, late records, deletes, time zone boundaries, currency conversions, each status value. Keep it in version control (CSV/Parquet) or a frozen schema/clone.
- **Expected outputs**: produced once by the trusted pipeline version, reviewed by a domain expert, stored alongside.
- Include known historical bug cases as permanent fixtures.

## Run
1. Load golden inputs into an isolated schema (seed, `COPY`, or clone).
2. Run the pipeline end to end pointed at that schema (dbt `--target golden`, Spark job with input paths as parameters).
3. Compare outputs to expected.

## Compare
```sql
-- rows in expected not in actual, and vice versa
(select * from expected.fct_orders except select * from golden_run.fct_orders)
union all
(select * from golden_run.fct_orders except select * from expected.fct_orders);
```
- Exclude volatile columns (load timestamps, run ids) or normalise them.
- Numeric tolerance for floats: compare `round(x, 6)` or `abs(a - b) < 1e-9`.
- `dbt_audit_helper.compare_relations` / datacompy (pandas/Spark) give per-column match rates.
- Deterministic ordering: compare as sets, not ordered lists, unless order is part of the contract.

## Updating goldens
When a change intentionally alters outputs, regenerate expected outputs in the PR, show the diff in review, and get sign-off. Never auto-update goldens in CI.

## vs unit tests and data diffs
Unit tests check one transformation's logic on tiny inputs; golden tests check the whole pipeline; data diffs against prod check real-volume behaviour. Use all three at different frequencies.

## Verify
A deliberate logic change makes the golden comparison fail with a readable diff; reverting it passes.
