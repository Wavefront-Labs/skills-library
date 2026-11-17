---
id: computing-software.data-engineering.data-quality.great-expectations-and-dq-frameworks
name: great-expectations-and-dq-frameworks
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, great-expectations, gx, expectation-suite, checkpoint, data-docs, sodacl, soda-core, soda-cloud, custom-expectation, validation-result, ci-cd-gating, data-context, batch-request]
level: advanced
status: gated
description: "Architect a standalone Great Expectations or Soda deployment: suites, checkpoints, custom expectations, and CI gating — beyond what dbt's built-in tests cover."
sources:
  - https://docs.greatexpectations.io/docs/
  - https://docs.soda.io/soda-documentation/soda-v3/soda-cl-overview/quick-start-sodacl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running Great Expectations or Soda as a standalone DQ layer

**Goal:** when checks need to run outside dbt's build graph — against raw/landing data before any model runs, against non-dbt-managed tables, or with checks too dynamic/statistical for a YAML `data_tests` block — stand up GX or Soda properly instead of ad hoc assert scripts. (See computing-software.data-engineering.data-quality.data-tests-and-freshness-slas for the check taxonomy and dbt-native tests this complements.)

## 1. Great Expectations' moving parts (1.0+ API — the pre-1.0 API differs substantially; verify version before copying snippets)
- **Data Context**: the project root config — where expectation suites, validation results, and data docs live (local filesystem, S3, or GX Cloud).
- **Expectation Suite**: a named, versioned set of expectations (`expect_column_values_to_not_be_null`, `expect_column_values_to_be_between`, etc.) attached to a specific table/batch shape — the GX equivalent of a dbt schema.yml, but runnable standalone and with a larger built-in expectation library (about 60 core expectation classes in GX 1.24, including statistical ones like `expect_column_kl_divergence_to_be_less_than` for distribution-shift detection that dbt's test framework has no native equivalent for).
- **Checkpoint**: in 1.x it groups one or more `ValidationDefinition`s (each = a batch definition + a suite) with an action list (Slack, email, PagerDuty, `UpdateDataDocsAction`, ...). `checkpoint.run(batch_parameters=...)` does NOT raise when expectations fail: it returns a result with `success=False` (tested on 1.24), so the orchestrator task must check `result.success` and raise itself. This is the runnable unit you call from Airflow/Dagster, not the suite directly.
- **Data Docs**: auto-generated static HTML documenting every expectation and its latest validation result per table — valuable as a discoverable data-quality catalogue for a team, not just a pass/fail log buried in CI output.
- **Custom Expectations**: when the built-in library doesn't cover a business rule (e.g. "this column's values must form a valid state machine transition from the previous row"), subclass `ColumnMapExpectation`/`TableExpectation` — worth it only when the rule is reused across many tables; a one-off rule is cheaper as a plain SQL assertion.

## 2. SodaCL — checks as readable YAML, not Python
The SodaCL page linked in sources now sits under the "Soda v3" docs; current Soda docs centre on data contracts. SodaCL syntax below is v3 and was not run here (soda-core would not install on Python 3.14) (gated: unconfirmed, source is paywalled or blocked).
Soda's SodaCL expresses most of the same check categories (freshness, schema, validity, anomaly) as declarative YAML, generally with less setup ceremony than GX for straightforward checks:
```yaml
checks for orders:
  - row_count > 0
  - missing_count(customer_id) = 0
  - duplicate_count(order_id) = 0
  - freshness(created_at) < 6h
  - anomaly detection for row_count     # built-in ML-based anomaly check, no manual threshold
```
Soda's anomaly-detection checks (gated: unconfirmed, source is paywalled or blocked) (statistical, trained on historical scan results) are a meaningful advantage over hand-set static thresholds for metrics with real seasonality — but they need a run history to warm up (several weeks of scans) before they're trustworthy; a brand-new anomaly check with no history will be noisy or silent, not useful, in week one.

## 3. CI/CD gating — where the check actually blocks something
A DQ framework that runs and reports but doesn't block anything is a dashboard, not a gate. Decide explicitly per check: does a failure (a) fail the pipeline/CI run (hard gate, use for grain/uniqueness/referential-integrity breaks that make downstream numbers wrong), or (b) just alert (soft gate, for drift/anomaly checks that need human judgment)? Wire the Checkpoint's/Soda scan's exit code into the orchestrator task so a hard-gate failure actually stops downstream tasks (an Airflow task returning success despite a logged GX failure teaches the team the checks don't matter).

## 4. Where this earns its keep over dbt-native tests
- Checking **raw/landing data before any dbt model runs** (dbt tests only run on models dbt builds).
- Checking **non-warehouse data**: files in a data lake, API responses, a non-dbt-managed database.
- **Statistical/ML-based checks** (distribution shift, anomaly detection) that dbt's test framework doesn't natively provide.
- A **shared validation layer across multiple tools** (Spark jobs, Airflow tasks, dbt models) that needs one consistent check definition and one Data Docs catalogue, rather than re-implementing checks per tool.

## Verify
- [ ] Every hard-gate check's failure actually stops the orchestrator DAG/CI pipeline — tested by deliberately breaking a check in a non-prod run.
- [ ] Data Docs (or Soda Cloud dashboard) is published somewhere the team actually looks, not just written to a local directory nobody opens.
- [ ] Anomaly-detection checks have at least several weeks of scan history before being trusted as a hard gate.
- [ ] Custom Expectations exist only for rules reused across 2+ tables — one-off rules use plain SQL assertions instead.
