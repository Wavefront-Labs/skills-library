---
id: computing-software.devops-ci-cd.argo-events.argo-events-metrics-prometheus-scrape-and-golden-signals
name: argo-events-metrics-prometheus-scrape-and-golden-signals
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, prometheus, metrics, golden-signals, scrape-config, pod-discovery, monitoring]
level: advanced
status: docs-checked
description: "Scrape Argo Events EventSource, Sensor, EventBus and controller metrics and map them to the four golden signals."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events metrics prometheus scrape and golden signals

Metrics (alpha, v1.3 and after) are exposed over HTTP by every generated EventSource, Sensor and EventBus pod. Prometheus discovers them with pod service discovery selecting `controller in (eventsource-controller,sensor-controller,eventbus-controller)`. Grant Prometheus's service account a ClusterRole allowing `get`, `list`, `watch` on `pods`.

EventSource metrics: `argo_events_event_service_running_total` (configured events running), `argo_events_events_sent_total`, `argo_events_events_sent_failed_total` (failed to reach the bus), `argo_events_events_processing_failed_total` (includes sent-failed), `argo_events_event_processing_duration_milliseconds` (receive to bus).

Sensor metrics: `argo_events_action_triggered_total`, `argo_events_action_failed_total`, `argo_events_action_retries_failed_total` (actions that failed after retries were exhausted; also incremented when no `retryStrategy` is specified), `argo_events_action_duration_milliseconds`.

EventBus: for native NATS see prometheus-nats-exporter.

Controllers: a second job selects `app in (eventsource-controller,sensor-controller,eventbus-controller)` and rewrites the address to port 7777.

Golden signals per the docs: latency (the two duration metrics), traffic (events_sent_total, action_triggered_total), errors (the four failed counters) and saturation (event_service_running_total plus Kubernetes CPU and memory).

Latency is the two duration metrics, traffic is `argo_events_events_sent_total` and `argo_events_action_triggered_total`, errors are the four failed counters, and saturation is `argo_events_event_service_running_total` plus Kubernetes CPU and memory metrics.

## Checked

2026-11-04. Confirmed against the Prometheus Metrics page (alpha, v1.3 and after): the `argo-events` and `argo-events-controllers` jobs with their label selectors and port 7777, the pod-discovery ClusterRole, every metric name and description, the EventBus pointer to prometheus-nats-exporter, and the Golden Signals grouping. Removed a duplicate paragraph and a remark about ServiceMonitor, which the page does not mention; completed the description of `argo_events_action_retries_failed_total`.
Method: documentation only; no commands were run.
