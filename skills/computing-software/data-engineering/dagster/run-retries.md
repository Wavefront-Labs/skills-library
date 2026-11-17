---
id: computing-software.data-engineering.dagster.run-retries
name: run-retries
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, run-retries, retry-strategy, from-failure, max-retries, dagster-yaml]
level: advanced
status: docs-checked
description: "Configure whole-run retries in Dagster via dagster.yaml run_retries or dagster/max_retries tags, retry strategies and avoiding double retries with op retries."
sources:
  - https://docs.dagster.io/deployment/execution/run-retries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Run retries

A failed run (any reason, including crash or termination) starts a new run. The limit applies to the whole run, unlike op retries which apply per op.

## Enable
Dagster+: set a default maximum via UI or dagster-cloud CLI full deployment settings; retries are enabled by default. OSS `dagster.yaml`:

```yaml
run_retries:
  enabled: true # omit on Dagster+
  max_retries: 3
```
Also configurable with tags on jobs or in the Launchpad (for example `dagster/max_retries`). For asset jobs, `op_retry_policy` on `define_asset_job()` takes a `RetryPolicy`; there the limit applies per asset, not per run.

## Strategy
Tag `dagster/retry_strategy`: default `FROM_FAILURE` skips successful ops and reuses their outputs; `ALL_STEPS` reruns everything. `FROM_FAILURE` needs an I/O manager that reads outputs across runs; on Kubernetes the S3 pickle I/O manager works but `FilesystemIOManager` does not (new run is a new job with its own filesystem).

## Combining with op retries
Op retry counts reset per retried run, causing extra retries. Set `retry_on_asset_or_op_failure: false` (default true) so only crashes or terminations retry; per job use tag `dagster/retry_on_asset_or_op_failure`:

```python
@dg.job(tags={"dagster/max_retries": 3, "dagster/retry_on_asset_or_op_failure": False})
def sample_job(): pass
```
Effective only for Dagster 1.6.7 or greater.

## FROM_ASSET_FAILURE
With `retry_on_asset_or_op_failure` false, `FROM_ASSET_FAILURE` uses persisted materialization records in the event log to exclude already materialized assets. Speeds recovery from node eviction or spot loss; useful for dbt since no persisted dbt artifacts are needed.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/deployment/execution/run-retries

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
