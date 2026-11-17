---
id: computing-software.database-administration.time-series-databases.prometheus-ha-pairs
name: prometheus-ha-pairs
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-ha, prometheus-ha-pairs, prometheus]
level: practitioner
status: docs-checked
description: "Run redundant Prometheus servers with an Alertmanager cluster so scraping and alerting survive a node loss."
sources:
  - https://raw.githubusercontent.com/prometheus/alertmanager/main/README.md
  - https://prometheus.io/docs/prometheus/latest/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HA pairs

**Goal:** Run redundant Prometheus servers for scrape and alert availability.

## Steps
- Run two identical Prometheus servers scraping the same targets. Local storage is not clustered or replicated, so redundancy comes from running duplicates.
- Give each a distinct external label (for example `replica: a` and `replica: b`) under `global.external_labels` so downstream systems can tell the copies apart.
- Alertmanager clustering is enabled by default. Instances join through `--cluster.peer` (repeat per peer) and listen for gossip on `--cluster.listen-address` (default `0.0.0.0:9094`); both UDP and TCP are needed.
- Point each Prometheus at the full list of Alertmanagers under `alerting.alertmanagers`, and do not load balance between Prometheus and Alertmanager: Alertmanager expects every alert to reach every instance, and it deduplicates.
- Keep the two configs identical via templating.

**Gotcha:** The two servers are independent copies, not a replicated store; do not switch between them mid-dashboard.

## Verify
- Stopping one Prometheus replica produces no alert gap.
- A test alert sent by both Prometheus servers produces a single notification.

## Checked
2026-11-03. Confirmed against the Alertmanager README (HA enabled by default, `--cluster.peer`, `--cluster.listen-address` default port 9094, UDP and TCP, list all Alertmanagers and do not load balance, deduplication) and the Prometheus storage page (local storage not replicated). Removed: Thanos Query/Mimir replica dedup advice, "doubles cost" and byte-identical statements not found in the pages read.
Method: documentation only; no commands were run.
