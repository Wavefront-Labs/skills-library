---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.instrumenting-batch-and-offline-jobs
name: instrumenting-batch-and-offline-jobs
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [batch-job-instrumentation, offline-processing-metrics, instrumentation, pushgateway, prometheus-best-practices]
level: practitioner
status: docs-checked
description: "Instrument offline pipelines and batch jobs: per-stage items in and out, last-processed timestamps, heartbeats, Pushgateway for service-level batch jobs, staleness alerts."
sources: ["https://prometheus.io/docs/practices/instrumentation/", "https://prometheus.io/docs/practices/pushing/", "https://github.com/prometheus/pushgateway/blob/master/README.md", "https://prometheus.github.io/client_python/exporting/pushgateway/", "https://prometheus.github.io/client_python/instrumenting/gauge/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instrumenting offline processing and batch jobs

## Offline processing (no one waits for a response; batching common)
From the Prometheus instrumentation page, for each stage track the items coming in, how many are in progress, the last time
you processed something, and how many items were sent out; if batching, also batches in and out. The last-processed time
detects a stall but is very localised: a better approach is a heartbeat, a dummy item passed all the way through that carries
the timestamp when it was inserted; each stage exports the most recent heartbeat timestamp it has seen, showing how long items
take to propagate. Systems with no quiet periods may not need an explicit heartbeat.

## Batch jobs (do not run continuously, so are hard to scrape)
The key metric is the last time the job succeeded. Also useful: how long each major stage took, the overall runtime, the last
time the job completed (successfully or not), and job-specific totals such as records processed. These are gauges and should be
pushed to a Pushgateway. A job that runs more than a few minutes can also be scraped with pull-based monitoring. A job that runs
more often than about every 15 minutes: consider converting it to a daemon handled as offline processing.

Python client (`push_to_gateway`, `Gauge.set_to_current_time()`, and `Gauge.time()` as context manager or decorator, which
overwrites the gauge with the latest duration):
```python
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
r = CollectorRegistry()   # separate registry: the default one may hold other metrics such as process metrics
last = Gauge('job_last_success_unixtime', 'Last time the batch job finished successfully', registry=r)
dur = Gauge('job_duration_seconds', 'Runtime of the last run', registry=r)
with dur.time():
    run()
last.set_to_current_time()
push_to_gateway('localhost:9091', job='nightly_reconcile', registry=r)
```
- `push_to_gateway` replaces metrics with the same grouping key (HTTP PUT); `pushadd_to_gateway` replaces only metrics with
  the same name and grouping key (POST); `delete_from_gateway` deletes by job and grouping key.
- Set `honor_labels: true` in the Prometheus scrape config for the Pushgateway so the pushed `job` and `instance` labels are kept.
- The Pushgateway adds `push_time_seconds` and `push_failure_time_seconds` (Unix time of the last successful and failed
  push to each group; 0 means never).

## When to use the Pushgateway
Only for the outcome of a service-level batch job (not tied to a machine or instance); leave `instance` out of such jobs'
grouping key so stale metrics are easier to manage. Pitfalls: a single point of failure and bottleneck when many instances
share one, loss of the automatic `up` health metric, and it never forgets pushed series until deleted via its API
(`curl -X DELETE http://pushgateway.example.org:9091/metrics/job/<job>`; the request is queued and returns 202).
For batch jobs tied to a machine (security update cron jobs, configuration management runs) the page recommends the Node
Exporter textfile collector instead.

## Alert on staleness
```promql
time() - job_last_success_unixtime{job="nightly_reconcile"} > 26 * 3600
absent(job_last_success_unixtime{job="nightly_reconcile"})
```
Export the Unix timestamp of the event and compute the age with `time() - metric`, not an age value that needs the job to
keep updating it. Choose the threshold from the job schedule plus slack. `absent()` returns a 1-element vector when the
selector has no series.

## Verify
- [ ] Each stage exports items in, in progress, last processed time and items out (offline), or last success time (batch).
- [ ] The Pushgateway scrape job has `honor_labels: true`, and retired jobs' groups are deleted.

## Checked
Checked 2026-11-07. Read in full: the Prometheus instrumentation practices page, the "When to use the Pushgateway" page, the client_python
Pushgateway page (the first 70 lines, through the push_to_gateway API entry; the rest of its API reference was not read) and the first 50 lines plus the time()
entry of the client_python Gauge page. From the Pushgateway README (30 KB) I read the introduction, run and use sections and the
PUT, POST and DELETE method text, found by search (not every section). Removed as not on those pages: the invented
`pipeline_*` metric names, "processing time histogram", the `job_last_failure_timestamp_seconds` advice, the atomic
`*.prom.$$` textfile recipe, the alert-rule YAML labels, the "never succeeded for 1h" rule, and the Gotcha that
a job run on random hosts must not carry instance (reworded as the page's service-level advice). The writing-client-libraries source was not read and was
removed from sources. The 26-hour threshold is an example; the pages give no schedule slack figure.
Method: documentation only; no commands were run.
