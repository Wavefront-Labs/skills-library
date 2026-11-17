---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.scrape-limits-and-body-size
name: scrape-limits-and-body-size
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, scrape-config, scrape-limits, target-limit, sample-limit-tuning, sample-limit, label-limit, label-name-length-limit, label-value-length-limit, body-size-limit, keep-dropped-targets, scrape-failures, cardinality-protection, prometheus-target-scrapes-exceeded, pca]
level: practitioner
status: verified
description: "Protect Prometheus from runaway targets with sample_limit, label_limit, body_size_limit and target_limit: pick values, find which targets trip them, alert on the exceeded counters."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config", "https://prometheus.io/docs/prometheus/latest/querying/api/#targets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scrape limits

**Goal:** one misbehaving exporter (a label with a user id, a 50 MB /metrics page, a service
discovery returning 20,000 pods) cannot take down the whole Prometheus.

## 1. The limits and what happens when they trip
All are per `scrape_config`, with `global:` defaults (0 = unlimited):
| Key | Trips when | Effect |
|---|---|---|
| `sample_limit` | post-`metric_relabel_configs` sample count > N | **whole scrape dropped**, `up=0`, `scrape_samples_post_metric_relabeling` still recorded |
| `label_limit` | any series has > N labels | whole scrape dropped |
| `label_name_length_limit` / `label_value_length_limit` | any label name/value longer than N bytes | whole scrape dropped |
| `body_size_limit` | uncompressed response > N (e.g. `50MB`) | scrape aborted, `up=0` |
| `target_limit` | targets after relabeling > N | **every target in the job fails** with `up=0` |
| `keep_dropped_targets` | — | cap on relabel-dropped targets kept in memory for the UI; `0` (the default) means no limit |

"Whole scrape dropped" is deliberate: a partial scrape would make counters look like resets. The target `lastError` values seen on
3.15.1: `sample limit exceeded`, `body size limit exceeded`, `label_limit exceeded (metric: lab, number of labels: 7, limit: 3)` (the
count includes `__name__`, `job` and `instance`), `label_value_length_limit exceeded (metric: lab, label name: a, value: "...", length: 50,
limit: 10)` and `target_limit exceeded (number of targets: 3, limit: 2)`. A body-size failure records `scrape_samples_scraped 0`; a
sample-limit failure still records `scrape_samples_post_metric_relabeling` (100 against a limit of 10).

```yaml
global:
  sample_limit: 50000
  label_limit: 40
  label_name_length_limit: 200
  label_value_length_limit: 1024
  body_size_limit: 50MB
scrape_configs:
  - job_name: kubernetes-pods
    target_limit: 5000
    sample_limit: 20000       # tighter for untrusted app pods
```

## 2. Choosing values
Measure first:
```promql
topk(20, scrape_samples_post_metric_relabeling)             # biggest targets today
max_over_time(scrape_samples_post_metric_relabeling[7d])     # peak per target
count by (job) (up)                                          # targets per job
```
Set `sample_limit` at 2-3× the current p99 target for the job; app-pod jobs lower than
infrastructure jobs (kube-state-metrics or node_exporter on a big node legitimately emit
tens of thousands). `target_limit` at 2× today's count catches SD explosions (an operator
bug creating thousands of Endpoints) without blocking growth.

## 3. See who hit a limit
```promql
increase(prometheus_target_scrapes_exceeded_sample_limit_total[1h]) > 0
increase(prometheus_target_scrapes_exceeded_body_size_limit_total[1h]) > 0
increase(prometheus_target_scrape_pool_exceeded_label_limits_total[1h]) > 0
increase(prometheus_target_scrape_pool_exceeded_target_limit_total[1h]) > 0
```
These are per-Prometheus counters, not per target. To find the target: the `/targets` page
shows the last error (`sample limit exceeded`), or
```bash
curl -s localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.lastError!="") | {job: .labels.job, instance: .labels.instance, lastError}'
```

## 4. Fix at the source, not the limit
When a target trips `sample_limit`, the cure is usually `metric_relabel_configs` dropping the
offending metric family or label (see `drop-unused-metrics`), or fixing the instrumentation.
Raising the limit for one noisy target is a temporary measure — note it with a comment and a
ticket.

## Gotchas
- `sample_limit` is evaluated **after** `metric_relabel_configs`, so dropping metrics there
  is a valid way to stay under it; `body_size_limit` is evaluated before parsing, so it is not.
- A target that trips a limit shows `up=0` with no HTTP error: dashboards that alert on
  `up==0` fire "target down" while the target is fine. Add the exceeded counters to the runbook.
- `target_limit` failing **all** targets in the job is a bigger blast radius than the SD
  problem it guards against; keep it generous and alert on `count(up) by (job)` growth instead
  for critical jobs.
- Limits in the Prometheus Operator are set per ServiceMonitor/PodMonitor (`sampleLimit`,
  `targetLimit`, `labelLimit`) and as defaults on the Prometheus CR (`enforcedSampleLimit`,
  which overrides a monitor's own `sampleLimit` unless that is greater than zero and lower).

## Verify
- [ ] `global.sample_limit` and `body_size_limit` are non-zero and documented.
- [ ] An alert on the four `exceeded_*` counters exists with a runbook link.
- [ ] Deliberately set `sample_limit: 10` on a test job: `up` goes 0, counter increments, UI shows the error; revert.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), Prometheus Operator API reference (main), jq 1.8.2.
- A local HTTP server served 100 samples, 5 samples, a series with 4 labels, a 50-character label value, a 5 KB body and three targets for one job; Prometheus 3.15.1 jobs with `sample_limit: 10`, `label_limit: 3`, `label_value_length_limit: 10`, `body_size_limit: 1KB`, `target_limit: 2`: every one failed with the error text above and `up 0`; with `target_limit: 2` all three targets were down. A job with `sample_limit: 10` plus a `metric_relabel_configs` drop of 90 series stayed up (sample limit is checked after metric relabeling).
- Counters seen at `/metrics`: `prometheus_target_scrapes_exceeded_sample_limit_total`, `prometheus_target_scrapes_exceeded_body_size_limit_total`, `prometheus_target_scrape_pool_exceeded_target_limit_total` and `prometheus_target_scrape_pool_exceeded_label_limits_total` (the old name in the skill does not exist).
- The global and per-job YAML block passes `promtool check config`; `keep_dropped_targets` semantics, limit semantics and units come from the 3.15 configuration page. The `/api/v1/targets` jq filter ran under jq 1.8.2.
- Prometheus Operator: the API reference lists `sampleLimit`, `targetLimit`, `labelLimit` on monitors and `enforcedSampleLimit` and friends on the Prometheus resource with the override rule stated above; a cluster was not available.
