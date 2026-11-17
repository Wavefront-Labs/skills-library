---
id: computing-software.messaging-and-integration.temporal.monitoring-prometheus-grafana
name: monitoring-prometheus-grafana
category: computing-software
field: messaging-and-integration
product: temporal
tags: [monitoring, prometheus, grafana, metrics-port, sdk-metrics, health-checks, dashboards, datadog]
level: practitioner
status: docs-checked
description: "Monitor self-hosted Temporal with Prometheus and Grafana: server and SDK metrics endpoints, start-dev --metrics-port, scrape config, community dashboards, health checks on 7233."
sources:
  - https://docs.temporal.io/self-hosted-guide/monitoring
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both the Temporal Service and SDKs emit metrics by default, but you must enable a Prometheus endpoint: in Service configuration (`global.metrics.prometheus`) and in application code for Worker and Client metrics (per-SDK observability guides and metrics samples; the Prometheus ports 8077 and 8078 for SDK targets must be set on `WorkflowServiceStubs` in application code).

Prometheus scrape config from the guide:

    global:
     scrape_interval: 10s
    scrape_configs:
     - job_name: 'temporalmetrics'
       metrics_path: /metrics
       scheme: http
       static_configs:
         - targets: ['host.docker.internal:8000']
           labels: {group: 'server-metrics'}
         - targets: ['host.docker.internal:8077', 'host.docker.internal:8078']
           labels: {group: 'sdk-metrics'}

Port 8000 is the Service target; 8077 and 8078 are Worker targets, set via the SDK's metrics listen address. Run the dev server with `temporal server start-dev --metrics-port 8000`, and Prometheus with the `prom/prometheus` image on port 9090. Confirm scraping at `http://localhost:9090/targets`.

Grafana: run `grafana/grafana-enterprise` on port 3000 (initial login admin/admin, so configure authentication in production). Add Prometheus as a data source at `http://host.docker.internal:9090` when using Docker, then import the community dashboards from Temporal's dashboards repository (follow its README): at least one for Server and one for SDK metrics. Add Grafana alerts on the parameters you track.

Health checks: the Frontend Service supports TCP or gRPC checks on port 7233; Nomad example uses `interval = "10s"`, `timeout = "2s"` (gRPC needs Consul 1.0.5+). Helm chart installs can pre-populate Grafana. Datadog has a Temporal integration through the Datadog Agent on top of Prometheus; Cloud can integrate directly.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: self-hosted-guide/monitoring, references/service-configuration (global.metrics.prometheus) (under https://docs.temporal.io/). Removed the samples-go/metrics path and the temporalio/dashboards repository name; the page names neither.

Method: documentation only; no commands were run.
