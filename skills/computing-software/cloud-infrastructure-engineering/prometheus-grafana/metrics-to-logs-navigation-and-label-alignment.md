---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.metrics-to-logs-navigation-and-label-alignment
name: metrics-to-logs-navigation-and-label-alignment
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [metrics-to-logs, label-alignment-across-signals, signal-correlation, loki, prometheus, grafana, explore]
level: practitioner
status: docs-checked
description: "Make metric-to-log jumps work in Grafana by aligning label names across Prometheus and Loki, using Explore's metrics-to-logs switch and correlations."
sources: ["https://grafana.com/docs/grafana/latest/explore/logs-integration/", "https://grafana.com/docs/loki/latest/get-started/labels/", "https://grafana.com/docs/grafana/latest/administration/correlations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metrics to logs navigation and label alignment

A metric spike is only useful if one click shows the logs for the same workload and time. That works only when both signals carry the same label names and values.

## How Explore switches from metrics to logs
Moving from a metrics data source that supports query export (such as Prometheus) to a logs data source that supports query import (such as Loki) keeps the labels of your query that exist in the logs and uses them to query the log streams. Example from the docs: `grafana_alerting_active_alerts{job="grafana"}` becomes `{job="grafana"}`. So label names must match exactly on both sides; labels that do not exist in the logs are dropped.

## Align labels at collection
- Loki labels follow Prometheus naming: ASCII letters, digits, underscores and colons, matching `[a-zA-Z_:][a-zA-Z0-9_:]*`. Convert unsupported characters to underscores (`app.kubernetes.io/name` becomes `app_kubernetes_io_name`). Do not begin and end label names with double underscores.
- Loki fills `service_name` automatically: it keeps an existing one, otherwise takes the first non-empty of service, app, application, app_name, name, app_kubernetes_io_name, container, container_name, k8s_container_name, component, workload, job, k8s_job_name, else `unknown_service`.
- With Alloy or the OpenTelemetry Collector as client, Loki stores a default list of OTel resource attributes as labels with periods replaced by underscores (for example `k8s.namespace.name` becomes `k8s_namespace_name`, `service.name` becomes `service_name`, `k8s.cluster.name` becomes `k8s_cluster_name`); other attributes become structured metadata. The list is configurable via `default_resource_attributes_as_index_labels` under the distributor's `otlp_config`. Make the Prometheus side use the same names, or relabel one side.
- Loki has a default limit of 15 index labels.

## Cardinality
Loki labels must be low-cardinality; unbounded values (timestamp, IP address, user ID) create huge indexes and many tiny chunks. Loki now advises against `k8s.pod.name` and `service.instance.id` as default index labels for new users and suggests converting them to structured metadata, so do not assume a `pod` stream label exists; check your Loki setup. Aim for no more than 10 to 15 labels.

## Correlations
Correlations create links from Explore visualizations (Logs panel, Table) that run a query in another data source (opened in Explore split view) or open an external URL. Configure them by provisioning, in Administration > Plugins and data > Correlations, or directly in Explore.

## Gotchas
- Never rely on labels present only on one side, such as the Prometheus `instance` (host:port) label, which logs do not carry unless you add it.
- Entries within a Loki stream must arrive in order inside the default two hour window, otherwise Loki answers `too far behind`.

## Checked
2026-11-08. Confirmed in the Grafana Logs in Explore page (metrics-to-logs switch), the Loki Understand labels page (label format, service_name discovery, OTel default labels, cardinality, 15 label limit) and the Grafana Correlations page. Removed: the Alloy `discovery.relabel` example and kube meta-label names, the split-view "Logs button" claim, the data link `/explore?...` instructions, the claim that pod is fine as a stream label (the Loki page now advises against it) and the Verify checklist.
Method: documentation only; no commands were run.
