---
id: computing-software.database-administration.vitess.vitess-monitoring-options
name: vitess-monitoring-options
category: computing-software
field: database-administration
product: vitess
tags: [monitoring, metrics, expvar, debug-vars, status-page, stats-backend]
level: intro
status: docs-checked
description: "Pick a Vitess monitoring method: /debug/status pages, the officially supported pull-based /debug/vars scrape, or push backends via --emit-stats, and note the Kubernetes caveat."
sources:
  - https://vitess.io/docs/25.0/reference/features/monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Monitoring page lists three ways to monitor a Vitess cluster, usable independently.

1. Status pages. Every component serves an HTML page at `http://<host>:<port>/debug/status`. It works out of the box but is basic; a vttablet page shows a QPS graph for the last few minutes.
2. Pull-based metrics. Vitess uses Go's expvar package and publishes JSON key-value pairs at `http://<host>:<port>/debug/vars`. Scraping these is described as the officially supported way to monitor Vitess and suits detailed dashboards.
3. Push-based metrics via plug-ins. Run each component with `--emit-stats`. Stats are pushed every 60 seconds by default, changed with `--stats-emit-period`. The backend is selected with `--stats-backend`. There is a preliminary OpenTSDB plug-in; a custom backend implements the `PushBackend` interface of the `stats` package and must be registered inside each relevant Vitess binary.

Kubernetes: the page says these integration methods are not yet supported by the Vitess team in Kubernetes, though it should be possible to get a Prometheus backend working.

The Reparenting page notes that VTOrc and VTCtld reparent metrics are on their `/debug/vars` pages, with Prometheus-compatible equivalents at `/metrics`.

## Checked

2026-11-04. The three methods, paths, flags and defaults, and the Kubernetes statement confirmed on the Monitoring page; the /metrics note on the Reparenting page.

Method: documentation only; no commands were run.
