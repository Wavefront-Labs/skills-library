---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.job-and-instance-target-labels
name: job-and-instance-target-labels
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [job-instance-labels, target-labels, honor-labels, scrape-config, data-model, up-metric]
level: practitioner
status: verified
description: "How Prometheus attaches job and instance target labels, the synthetic per-scrape series, and how to set meaningful instance values via relabeling."
sources: ["https://prometheus.io/docs/concepts/jobs_instances/", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job and instance target labels

## What Prometheus adds to every scraped series
- `job` = `job_name` of the scrape config (unless relabeled).
- `instance` = `__address__` after relabeling (`host:port`) unless set explicitly.
- Any target labels from SD/relabeling not starting with `__`.

## Synthetic series per target (per scrape)
| Series | Meaning |
|---|---|
| `up` | 1 if the scrape succeeded, 0 otherwise |
| `scrape_duration_seconds` | scrape time |
| `scrape_samples_scraped` | samples exposed |
| `scrape_samples_post_metric_relabeling` | after `metric_relabel_configs` |
| `scrape_series_added` | new series this scrape (churn signal) |
| `scrape_timeout_seconds`, `scrape_sample_limit`, `scrape_body_size_bytes` | only with `extra_scrape_metrics: true` |

## Meaningful instance values
IP:port changes on reschedule; set instance to a stable name:
```yaml
relabel_configs:
  - source_labels: [__meta_kubernetes_pod_name]
    target_label: instance
  # or for VMs: hostname without port
  - source_labels: [__address__]
    regex: "([^:]+):\\d+"
    target_label: instance
```
Keep `instance` unique per target within a job, or series from two targets collide.

## Conflicts with exposed labels
If the target exposes its own `job`/`instance` labels, Prometheus renames them to `exported_job`/`exported_instance` (default `honor_labels: false`; a series `exp{job="mine",instance="theirs"}` was stored with `exported_job="mine"`, `exported_instance="theirs"`, `job=<job_name>`). With `honor_labels: true` the exposed values win (`job="mine"`, `instance="theirs"`): use it only for Pushgateway and federation where the exposed labels are authoritative.

## Gotchas
- Two jobs scraping the same target double its series under different `job` values.

## Verify
- [ ] `count by (job, instance) (up) > 1` is empty.
- [ ] Instance values survive a pod reschedule (name-based, not IP-based) where history continuity matters. (`__meta_kubernetes_pod_name` is a label of the Kubernetes `pod` role; it was not run here, the regex form below was.)

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), prometheus_client 0.26.0 on Python 3.14, client_golang 1.25.0 on Go 1.26.
- Synthetic series: a 3.15.1 target listed `up`, `scrape_duration_seconds`, `scrape_samples_scraped`, `scrape_samples_post_metric_relabeling`, `scrape_series_added`, plus `scrape_timeout_seconds`, `scrape_sample_limit`, `scrape_body_size_bytes` once `extra_scrape_metrics: true` was set.
- The instance relabel rule from the skill (regex capturing the part before the colon, `target_label: instance`) turned `localhost:18082` into `instance="localhost"`; `target_label: podname` from a static `pod` label also worked.
- `exported_job`/`exported_instance` and `honor_labels: true` behaviour: two jobs scraping a target that exposes `job` and `instance` labels.
- `__meta_kubernetes_pod_name` is listed in the 3.15 configuration page for the pod role; Kubernetes itself was not available.
