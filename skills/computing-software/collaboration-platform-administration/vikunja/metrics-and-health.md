---
id: computing-software.collaboration-platform-administration.vikunja.metrics-and-health
name: metrics-and-health
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, prometheus-metrics, health-endpoint, pprof-profiler, basic-auth-monitoring]
level: practitioner
status: docs-checked
description: "Expose Vikunja's Prometheus metrics endpoint and health checks with optional basic auth, and the caution about the pprof profiler."
sources:
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/metric.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Metrics (`metrics.*`):
- `metrics.enabled` default false; when true Prometheus can scrape `/api/v1/metrics`.
- `metrics.username` and `metrics.password`: when non-empty the endpoint requires basic auth.
- `metrics.pprof` default false: exposes the Go profiler at `/debug/pprof/`, behind the same basic auth if set. Profiles reveal internals, so enable only on instances not reachable from the internet.

Health (`health.*`): endpoints `/health` and `/api/v2/health`. Set `health.username` and `health.password` to require basic auth.

The key-value store (`keyvalue.type`, `memory` by default or `redis`) is used for metrics and a few cache systems; with `redis` it must be configured separately.

Prometheus scrape job from the docs: `metrics_path: '/api/v1/metrics'`, `scrape_interval: 5s`, target `your-vikunja-host-url:3456`. For Grafana import dashboard ID `21928`.

## Checked

2026-11-04. Confirmed against the Vikunja Metrics page (setup/metric: scrape config and dashboard ID) and config-raw.json (metrics.*, health.* and keyvalue.type keys, defaults and comments, health endpoint paths). Removed: the claim that metrics state is per process with the memory store, which neither page states.

Method: documentation only; no commands were run.
