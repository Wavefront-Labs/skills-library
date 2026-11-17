---
id: computing-software.cloud-infrastructure-engineering.google-cloud.prometheus-receiver-in-ops-agent
name: prometheus-receiver-in-ops-agent
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, ops-agent, prometheus-receiver-ops-agent, prometheus-scrape, managed-prometheus, vm-metrics, exporters]
level: practitioner
status: docs-checked
description: "Scrape Prometheus exporters on Compute Engine VMs with the Ops Agent prometheus receiver: scrape config, relabeling, PromQL naming, and cost controls."
sources: ["https://cloud.google.com/stackdriver/docs/solutions/agents/ops-agent/prometheus", "https://cloud.google.com/stackdriver/docs/solutions/agents/ops-agent/configuration#receivers", "https://cloud.google.com/stackdriver/docs/managed-prometheus/query"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus receiver in Ops Agent

The Ops Agent can scrape Prometheus endpoints on the VM and send samples to Google Cloud Managed
Service for Prometheus (queryable with PromQL), no Prometheus server needed.

## Config
```yaml
# /etc/google-cloud-ops-agent/config.yaml
metrics:
  receivers:
    prometheus:
      type: prometheus
      config:
        scrape_configs:
        - job_name: node_app
          scrape_interval: 30s
          static_configs:
          - targets: ["localhost:9100", "localhost:8080"]
          metric_relabel_configs:
          - source_labels: [__name__]
            regex: "go_.*"
            action: drop
  service:
    pipelines:
      prometheus_pipeline:
        receivers: [prometheus]
```
```bash
sudo systemctl restart google-cloud-ops-agent
sudo systemctl status google-cloud-ops-agent
```
Uses a standard Prometheus scrape config; `relabel_configs` and `metric_relabel_configs` can reduce what is ingested. Check the Ops Agent Prometheus page for which scrape options are supported.

## Querying
Metrics land as `prometheus.googleapis.com/<metric>/<kind>`; in PromQL use the original name:
```promql
rate(http_requests_total{instance_name="web-1"}[5m])
```
Check the Ops Agent Prometheus page for the labels added to ingested series.

## Gotchas
- Prometheus metrics are ingested as custom metrics and are subject to their quotas and billing; longer scrape intervals and drop relabeling reduce volume.
- Ops Agent version must support the receiver (2.25.0 or higher); pin versions in fleets via agent policies.

## Verify
- [ ] `up{job="node_app"}` returns 1 per VM in Metrics Explorer (PromQL tab).

## Checked

2026-10-28. Confirmed against: Ops Agent Prometheus page: Ops Agent 2.25.0 or higher required, type: prometheus receiver, scrape_interval, relabel_configs/metric_relabel_configs, metrics ingested as prometheus.googleapis.com custom metrics.

Removed or rewritten: the exact label list, file_sd and Kubernetes SD support statements, the journalctl unit name (replaced with a plain status command), the third-party receiver overlap note and per-sample billing wording; none confirmed.

Method: documentation only; no commands were run.
