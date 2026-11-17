---
id: computing-software.cybersecurity-defensive.zitadel.metrics-and-health-endpoints
name: metrics-and-health-endpoints
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, metrics, prometheus, opentelemetry, health, probes]
level: practitioner
status: docs-checked
description: "Scrape ZITADEL metrics at /debug/metrics and wire Kubernetes probes to the ready and healthy endpoints."
sources:
  - https://zitadel.com/docs/self-hosting/manage/metrics/overview
  - https://zitadel.com/docs/apis/observability/health
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Metrics are enabled by default. ZITADEL exposes them at `/debug/metrics` in Prometheus exposition format. They are instrumented with OpenTelemetry and include process and Go runtime metrics, HTTP and gRPC server metrics (counts, latencies, error rates) and ZITADEL-specific metrics. The set of metrics and labels can change between releases. If you changed ports, paths or exposure through Helm values, proxies or ingress, adjust the address.

Ways to collect them: a Prometheus server scrapes the endpoint directly, an OpenTelemetry Collector scrapes it with a Prometheus receiver and forwards elsewhere, or a managed platform such as Grafana Cloud, Amazon Managed Service for Prometheus, Datadog or New Relic ingests it through a Prometheus-compatible agent. If metrics were explicitly disabled in your configuration, re-enable them first; the defaults are in `defaults.yaml`.

Health:

- `/debug/ready` shows whether the process is ready to accept traffic. Kubernetes calls this the readinessProbe. It stays not ready while ZITADEL is busy with something such as a database schema migration, which supports zero downtime upgrades.
- `/debug/healthz` shows the process is alive: the livenessProbe.

Point load balancers and uptime probes at these paths rather than at a user-facing page.

## Checked

2026-11-08. Read in full: the metrics overview page and the ready and health endpoints page. All claims confirmed.

Method: documentation only; no commands were run.
