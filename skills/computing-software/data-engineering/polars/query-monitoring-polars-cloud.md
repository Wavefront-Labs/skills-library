---
id: computing-software.data-engineering.polars.query-monitoring-polars-cloud
name: query-monitoring-polars-cloud
category: computing-software
field: data-engineering
product: polars
tags: [polars-query-monitoring, monitoring, polars-cloud, polars-nanook, query-profile, streaming-engine, config, workspace, metrics]
level: practitioner
status: docs-checked
description: "Send metrics from locally run Polars queries to the Polars Nanook query profile with pl.Config.enable_monitoring, scoped to a workspace or a single query."
sources:
  - https://docs.pola.rs/user-guide/misc/monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitor local queries in Polars Nanook

Goal: see which part of a query is slow, via a query profile in the Polars Nanook dashboard, while data and compute stay local. (The skill id says Polars Cloud; the current docs page names the service Polars Nanook.)

## What is sent
Only the query plan and per-node runtime counters. No rows or column values. The plan does include the schema, column names, source paths and any literals written into the query.

## Requirements
- A Polars Nanook account.
- The `polars-nanook` package in the same environment as Polars:
```bash
pip install 'polars-nanook>=0.13.0'
```

## Enable
```python
import polars as pl

pl.Config.enable_monitoring()
```
The first call opens a browser to authenticate if you are not logged in. Every query collected afterwards reports to the Polars Nanook dashboard.

Use the streaming engine: it is the only engine that reports per-node metrics, so enabling monitoring also sets engine affinity to `"streaming"`.

## Choose a workspace
Metrics go to the account's default workspace. Override with `workspace`, and add `organization` when the workspace name exists in more than one organization:
```python
pl.Config.enable_monitoring(workspace="My workspace")
pl.Config.enable_monitoring(workspace="My workspace", organization="My organization")
```

## One query only
`Config` also works as a context manager; the previous monitoring state and the previous engine affinity are restored on exit:
```python
with pl.Config(enable_monitoring=True):
    lf.collect()
```

## Disable
```python
pl.Config.enable_monitoring(False)
```

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/misc/monitoring/. Corrected: Rewritten for the current Polars Nanook naming and the polars-nanook package; the skill id keeps its old name. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
