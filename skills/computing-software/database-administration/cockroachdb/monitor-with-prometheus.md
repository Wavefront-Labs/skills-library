---
id: computing-software.database-administration.cockroachdb.monitor-with-prometheus
name: monitor-with-prometheus
category: computing-software
field: database-administration
product: cockroachdb
tags: [prometheus, metrics, monitoring, scrape-config, status-vars]
level: practitioner
status: docs-checked
description: "Scrape CockroachDB self-hosted node metrics with Prometheus: the /_status/vars path, scrape_interval, scheme and targets edits for production and secure clusters."
sources:
  - https://www.cockroachlabs.com/docs/stable/monitor-cockroachdb-with-prometheus
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pull per-node time series from a running self-hosted cluster into Prometheus 2.x.

Steps:
1. Install Prometheus 2.x, put the binary on `PATH`, check with `prometheus --version`.
2. Download the starter `prometheus.yml` from the docs. It scrapes one insecure local node every 10 seconds using:
   - `scrape_interval: 10s`
   - `metrics_path: '/_status/vars'` (the Prometheus endpoint)
   - `scheme: 'http'`
   - `targets: ['localhost:8080']` (host and `http-port` of the node)
3. Adjust per deployment:
   - Multi-node local: add `'localhost:<http-port>'` for each node.
   - Production: list `'<hostname>:<http-port>'` for every node and make sure the network allows TCP on those ports.
   - Secure cluster: uncomment `scheme: 'https'` and comment out `scheme: 'http'`.
4. Create a `rules` directory and download the CockroachDB `aggregation.rules.yml` and `alerts.rules.yml` files into it (links on the docs page).
5. Start Prometheus with `prometheus --config.file=prometheus.yml`.

## Checked

2026-11-03. Confirmed against the Prometheus monitoring page: Prometheus 2.x, `prometheus --version`, starter config keys, `/_status/vars`, scheme change for secure clusters, targets, rules files, `--config.file`. Removed: the managed-offering gotcha and the invented verification step.
Method: documentation only; no commands were run.
