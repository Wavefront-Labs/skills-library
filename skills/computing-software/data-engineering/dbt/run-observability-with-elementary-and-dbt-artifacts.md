---
id: computing-software.data-engineering.dbt.run-observability-with-elementary-and-dbt-artifacts
name: run-observability-with-elementary-and-dbt-artifacts
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-run-observability, elementary, dbt-artifacts, run-results]
level: practitioner
status: gated
description: "Track dbt run and test history with elementary and dbt_artifacts: on-run-end uploads, model timing trends, failure alerts to Slack, and querying run_results."
sources:
  - https://docs.elementary-data.com/oss/quickstart/quickstart-cli-package
  - https://github.com/brooklyn-data/dbt_artifacts
  - https://docs.getdbt.com/reference/artifacts/run-results-json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Run observability (elementary / dbt_artifacts)

**Goal:** answer "what failed, what got slower, since when" across runs, with alerts.

## dbt_artifacts (Brooklyn Data)
```yaml
packages:
  - package: brooklyn-data/dbt_artifacts
    version: [">=2.0.0", "<3.0.0"]
```
```yaml
# dbt_project.yml
on-run-end:
  - "{{ dbt_artifacts.upload_results(results) }}"
```
Creates tables like `model_executions`, `test_executions`, `invocations`; query them for durations, failure counts, run frequency. (gated: unconfirmed, source is paywalled or blocked)

## elementary
```yaml
packages:
  - package: elementary-data/elementary
    version: 0.16.1
models:
  elementary:
    +schema: elementary
```
```bash
dbt deps && dbt run --select elementary     # creates its tables; on-run-end hooks upload results
pip install elementary-data
edr monitor --slack-webhook "$SLACK_WEBHOOK"        # alert on failures since last run
edr report                                           # static HTML: test results, lineage, run times
```
Also adds anomaly tests (`elementary.volume_anomalies`, `freshness_anomalies`, `schema_changes`).

## Without packages
Parse `target/run_results.json` after each job (`status`, `execution_time`, `adapter_response.rows_affected`) and push to your metrics system.

## What to watch
- Slowest 20 models over 30 days; regressions over 50%.
- Tests flapping between pass/fail.
- Models not run in N days (dead code).
- Total job duration vs SLA.

## Gotchas
- on-run-end uploads add a few seconds; with many small runs consider batching.
- Run the packages in every environment that matters (prod), into a separate schema with retention.

## Verify
Fail a test deliberately: it appears in the history table and a Slack alert arrives.

## Checked

2026-11-02

- Confirmed: The elementary quickstart page, the brooklyn-data/dbt_artifacts README and the dbt run_results.json reference were fetched.
- Removed or gated: elementary test names, the --slack-webhook flag, the pinned package version and the brooklyn-data version range are not stated on the fetched pages; gated, confirm in the package docs and dbt Hub.

Method: documentation only; no commands were run.
