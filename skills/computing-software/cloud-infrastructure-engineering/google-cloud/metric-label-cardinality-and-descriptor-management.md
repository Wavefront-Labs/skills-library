---
id: computing-software.cloud-infrastructure-engineering.google-cloud.metric-label-cardinality-and-descriptor-management
name: metric-label-cardinality-and-descriptor-management
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-monitoring, metric-label-cardinality, delete-metric-descriptor, time-series-limits, custom-metrics, managed-prometheus]
level: practitioner
status: docs-checked
description: "Keep Cloud Monitoring custom and Prometheus metrics healthy: label cardinality limits and cost, finding high-cardinality series, and listing or deleting metric descriptors."
sources: ["https://cloud.google.com/monitoring/quotas#custom_metrics_quotas", "https://cloud.google.com/monitoring/custom-metrics/browsing-metrics#delete", "https://cloud.google.com/stackdriver/docs/managed-prometheus/cost-controls"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metric label cardinality and descriptor management

Each unique combination of metric type + resource labels + metric labels is a **time series**.
Cost and query performance scale with active series. Limits exist per descriptor (30 labels per custom, external or workload metric descriptor; 200 per Prometheus metric descriptor) and on active time series (200,000 per monitored resource for custom metrics). Check the Monitoring quotas page.

## Rules
- Never use unbounded values as labels: user IDs, request IDs, full URLs, timestamps, error messages.
- Bucket instead: `route="/orders/:id"`, `status_class="5xx"`.
- Prefer exemplars or traces/logs for per-request detail.

## Find high cardinality
Use the Metrics management page in Cloud Monitoring, or PromQL in Managed Prometheus:
```
topk(20, count by (__name__)({__name__=~".+"}))
count by (path) (http_requests_total)
```
MQL equivalent with `group_by` counts on Metrics Explorer.

## Drop or relabel at the source
Managed Prometheus `PodMonitoring` metric relabeling:
```yaml
endpoints:
- port: metrics
  metricRelabeling:
  - action: drop
    regex: "go_gc_.*|http_request_duration_seconds_bucket"
    sourceLabels: [__name__]
  - action: labeldrop
    regex: "user_id|request_id"
```

## Descriptors
```bash
curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://monitoring.googleapis.com/v3/projects/<P>/metricDescriptors?filter=metric.type%3Dstarts_with(%22custom.googleapis.com%2F%22)" | jq -r '.metricDescriptors[].type'
curl -s -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://monitoring.googleapis.com/v3/projects/<P>/metricDescriptors/custom.googleapis.com%2Fold%2Fmetric"
```
Check the Monitoring docs on deleting metric descriptors before deleting one, and prefer writing a new metric name over changing labels on an existing descriptor.

## Verify
- [ ] Metrics management shows no metric with runaway series growth week over week.

## Checked

2026-10-28. Confirmed against: Monitoring quotas page (30 labels per custom/external/workload descriptor, 200 per Prometheus descriptor, 200,000 active time series per monitored resource) and the Managed Prometheus cost-controls page (PodMonitoring metricRelabeling, drop action).

Removed or rewritten: per-MiB and per-sample cost wording, the billable-volume description of the Metrics management page, and the descriptor-deletion semantics.

Method: documentation only; no commands were run.
