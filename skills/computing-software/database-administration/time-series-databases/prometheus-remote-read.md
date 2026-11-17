---
id: computing-software.database-administration.time-series-databases.prometheus-remote-read
name: prometheus-remote-read
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-remote, prometheus-remote-read, prometheus]
level: practitioner
status: docs-checked
description: "Query data held in a remote store from Prometheus with remote_read, including read_recent, required_matchers and limits."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://prometheus.io/docs/prometheus/latest/configuration/configuration/
  - https://prometheus.io/docs/prometheus/latest/command-line/prometheus/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote read

**Goal:** Query historical data held in a remote store from Prometheus.

## Steps
```
remote_read:
  - url: https://remote-store.example.com/api/v1/read
    read_recent: false
    required_matchers:
      job: node
```
- `read_recent` (default `false`): whether reads are made for time ranges the local storage should have complete data for. Leave it false so remote read is used only for older data.
- `required_matchers` is a list of equality matchers that must be present in a selector for the remote read endpoint to be queried.
- `remote_timeout` (per remote_read entry) defaults to `1m`; `filter_external_labels` defaults to true.
- Server-side, `--storage.remote.read-sample-limit` caps samples returned through the remote read interface (default 5e7).
- Prometheus only fetches raw series for the selectors and time range; all PromQL evaluation still happens in Prometheus, so large queries move a lot of data and have a scalability limit.
- The read protocol is not yet considered a stable API.

**Gotcha:** Remote read returns raw series, so a wide query pulls all matching samples into the querying Prometheus before it is evaluated.

## Verify
- A query over a range older than local retention returns data from the remote.
- The latency of those queries is acceptable.

## Checked
2026-11-03. Confirmed against the configuration reference (`read_recent`, `required_matchers`, `remote_timeout`, `filter_external_labels`), the storage page (raw series only, evaluation in Prometheus, protocol not stable) and the command-line page (`--storage.remote.read-sample-limit`). Removed: the Thanos Query URL, "true duplicates work", "rules and alerts evaluate on local data only" and the vendor-comparison advice (not on a page read); the config key `remote_read.remote_timeout` is now stated per entry.
Method: documentation only; no commands were run.
