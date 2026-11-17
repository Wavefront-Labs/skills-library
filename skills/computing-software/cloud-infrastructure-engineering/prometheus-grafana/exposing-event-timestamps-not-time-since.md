---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.exposing-event-timestamps-not-time-since
name: exposing-event-timestamps-not-time-since
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [timestamp-not-time-since, event-timestamp-metric, instrumentation, freshness-alerts, last-success-age, batch-job-instrumentation]
level: practitioner
status: docs-checked
description: "Export the Unix timestamp of events (last success, last backup) as gauges instead of 'seconds since' values, and query age with time() minus the metric."
sources: ["https://prometheus.io/docs/practices/instrumentation/", "https://prometheus.io/docs/practices/naming/", "https://pkg.go.dev/github.com/prometheus/client_golang/prometheus"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event timestamps, not time-since

The Prometheus instrumentation page: "If you want to track the amount of time since something happened, export the Unix timestamp at which it happened - not the time since it happened." With the timestamp exported, `time() - my_timestamp_metric` gives the time since the event, "removing the need for update logic and protecting you against the update logic getting stuck."

## Instrumentation
A timestamp is a gauge. The naming page's own example of a timestamp metric is `data_pipeline_last_record_processed_timestamp_seconds`, so use a `_timestamp_seconds` suffix. In Go, a `prometheus.Gauge` has `SetToCurrentTime()`, which sets it to the current Unix time in seconds.
```go
lastSuccess := prometheus.NewGauge(prometheus.GaugeOpts{
    Name: "backup_last_success_timestamp_seconds",
    Help: "Unix time of the last successful backup",
})
// after a successful backup:
lastSuccess.SetToCurrentTime()
```

## Query
```promql
time() - backup_last_success_timestamp_seconds
```
Alert by comparing that age with a threshold you choose, for example `> 26*3600` (the threshold is yours, not from the docs).

## Why not "seconds since"
A "time since" gauge needs update logic to keep it moving; if that logic gets stuck the value freezes and looks healthy. With a timestamp, the age keeps growing in PromQL.

## Batch jobs
The instrumentation page says the key metric of a batch job is the last time it succeeded; also useful are how long each major stage took, the overall runtime and the last time the job completed (successful or failed). These are all gauges and should be pushed to a PushGateway. Jobs running more often than about every 15 minutes: consider converting them to daemons handled as offline processing. For offline-processing pipelines the page suggests passing a heartbeat item that carries its insertion timestamp through the stages, each stage exporting the latest heartbeat timestamp it saw.

## Verify
- [ ] The timestamp gauge changes only when the event happens, and the PromQL age grows while the job is not running.

## Checked
Date: 2026-11-07. Read in full: the Prometheus instrumentation practices page (the "Timestamps, not time since", "Batch jobs" and offline-processing sections) and the naming page (the timestamp example); the Go `Gauge.SetToCurrentTime` entry was found by searching the very large prometheus package page on pkg.go.dev, which was not read end to end. Trims: removed the Python `prometheus_client` snippet and `set_to_current_time`, the `last_completion` and `_duration_seconds` metric names as prescriptions (the page names the concepts, not those metric names), the claim that "an exporter only updates when scraped code runs", the 0-initialisation and milliseconds gotchas, and the "kill the updater" verify, none of which the pages state. The `26*3600` threshold is labelled as an example.
Method: documentation only; no commands were run.
