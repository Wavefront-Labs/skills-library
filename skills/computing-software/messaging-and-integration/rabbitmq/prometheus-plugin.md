---
id: computing-software.messaging-and-integration.rabbitmq.prometheus-plugin
name: prometheus-plugin
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, prometheus-plugin, rmq-monitoring]
level: practitioner
status: docs-checked
description: "Enable rabbitmq_prometheus and scrape port 15692 for per-node and per-object metrics."
sources:
  - https://www.rabbitmq.com/docs/prometheus
  - https://www.rabbitmq.com/docs/monitoring
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus plugin

**Goal:** Get metrics into Prometheus and Grafana.

## Steps
1. `rabbitmq-plugins enable rabbitmq_prometheus`; scrape port 15692 (`curl <hostname>:15692/metrics`).
2. Use `/metrics/per-object` carefully; with many connections and queues it returns very large payloads and uses a lot of CPU, so scrape it infrequently or not at all.
3. The guide covers Grafana dashboards and TLS support for the scraping endpoint.

## Failure modes
- Per-object metrics increase CPU use on busy brokers.

## Verify
- `curl <hostname>:15692/metrics` returns metrics.

## Checked

2026-11-02. Confirmed in docs/prometheus and docs/monitoring: port 15692, /metrics, /metrics/per-object cost warning, Grafana and TLS sections. Removed: "official dashboards" import step wording and head pipe example.
Method: documentation only; no commands were run.
