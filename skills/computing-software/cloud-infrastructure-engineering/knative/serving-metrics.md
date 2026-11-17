---
id: computing-software.cloud-infrastructure-engineering.knative.serving-metrics
name: serving-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [serving-metrics, opentelemetry, queue-depth, invocation-duration, revision-pods-desired, kn-revision]
level: practitioner
status: docs-checked
description: "Know the queue-proxy, activator and autoscaler metrics Serving exposes and their attributes."
sources:
  - https://knative.dev/docs/serving/observability/metrics/serving-metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right Serving metric when monitoring the control plane and workloads.

Administrators can watch the Serving control plane through metrics each component exposes. Metrics are OpenTelemetry style, with names under `kn.`.

Workload metrics come from the queue-proxy sidecar, which enforces container concurrency and feeds the autoscaler. Attributes include `container.name` (always `queue-proxy`), `k8s.namespace.name`, `k8s.pod.name`, `service.version`, `service.name`, `service.instance.id`, `kn.service.name`, `kn.configuration.name` and `kn.revision.name`.
- `kn.serving.queue.depth`: Int64Gauge, number of items currently in the queue proxy queue.
- `kn.serving.invocation.duration`: Float64Histogram in seconds, duration of task execution.

HTTP server and client metrics are also listed for the workload and activator.

Activator metrics:
- `kn.revision.request.concurrency`: concurrent requests routed to the activator.
- `kn.activator.stats.conn.reachable`: whether a peer is reachable from the activator (1 reachable, 0 not).
- `kn.activator.stats.conn.errors`: cumulative connection errors, complementing the reachable gauge.

Autoscaler metrics:
- `kn.autoscaler.scrape.duration`: time spent scraping a revision.
- `kn.revision.pods.desired` and `kn.revision.pods.requested`: pods the autoscaler wants and has requested.
- `kn.revision.capacity.excess`: excess burst capacity over the stable window.
- `kn.revision.concurrency.stable`, `.panic` and `.target`, and `kn.revision.rps.stable` and `.panic`: observed and target load per window.

The page warns these metrics may change during the migration from OpenCensus to OpenTelemetry. It also lists webhook, workqueue and Go runtime metrics, not covered here.

## Checked

Method: docs-checked 2026-11-09 against https://knative.dev/docs/serving/observability/metrics/serving-metrics/ (read in full; metric names, instrument types and attributes match).
