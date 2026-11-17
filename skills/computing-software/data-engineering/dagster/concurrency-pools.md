---
id: computing-software.data-engineering.dagster.concurrency-pools
name: concurrency-pools
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, concurrency-pools, pool, default-limit, granularity, free-slots-after-run-end-seconds]
level: advanced
status: docs-checked
description: "Limit ops or runs across all Dagster runs with concurrency pools: pool keyword, dagster instance concurrency set, run granularity and stale slot cleanup."
sources:
  - https://docs.dagster.io/guides/operate/managing-concurrency/concurrency-pools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Concurrency pools

Goal: protect a shared resource (database, API) across all runs.

1. Default limit: Dagster+ edit `concurrency` in deployment settings (UI or `dagster-cloud` CLI); OSS `dagster.yaml`:
```yaml
concurrency:
  pools:
    default_limit: 1
```
2. Assign assets or ops to a pool with the `pool` keyword argument; verify in the asset details pane.
3. Set a pool limit: UI **Deployments > Concurrency > Add pool limit**, or CLI `dagster instance concurrency set database 1`.

## Limit runs rather than ops
Default granularity is `op`: a pool `foo` with limit 1 allows one op executing at a time across runs, but run count is unaffected. To limit runs containing those ops set:
```yaml
concurrency:
  pools:
    granularity: 'run'
```

## Stale slots (deadlock)
Dagster does not free pool slots when a run is cancelled or fails. With limit 1, one cancelled run blocks all future runs. Strongly recommended:
```yaml
run_monitoring:
  enabled: true
  free_slots_after_run_end_seconds: 300
```

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/operate/managing-concurrency/concurrency-pools

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
