---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.monitoring-federation-scrapes
name: monitoring-federation-scrapes
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [federation-scrape-duration, federation-monitoring, federation, scrape-timeout, meta-monitoring]
level: practitioner
status: docs-checked
description: "Watch federation health: scrape duration vs timeout, samples per federation scrape, staleness of federated series and alerts before scrapes fail."
sources: ["https://prometheus.io/docs/prometheus/latest/federation/", "https://prometheus.io/docs/concepts/jobs_instances/#automatically-generated-labels-and-time-series", "https://prometheus.io/docs/prometheus/latest/querying/basics/#staleness"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring federation scrapes

Federation is a normal scrape of a leaf server's `/federate` endpoint, so the automatically generated scrape series describe its health. Watch them so a growing scrape is caught before it hits the timeout.

## Queries
```promql
# headroom: duration as fraction of timeout
scrape_duration_seconds{job="federate"} / scrape_timeout_seconds{job="federate"}   # scrape_timeout_seconds needs the extra-scrape-metrics feature flag
# or compare against the configured value
max_over_time(scrape_duration_seconds{job="federate"}[1h]) > 20      # with scrape_timeout 25s
scrape_samples_scraped{job="federate"}
up{job="federate"}
```
`up` is 1 if the instance is reachable and 0 if the scrape failed; `scrape_duration_seconds` is the duration of the scrape; `scrape_samples_scraped` is the number of samples the target exposed.

## Alerts
Example thresholds; the 25 assumes a 25s `scrape_timeout`, adjust it to yours.
```yaml
- alert: FederationScrapeSlow
  expr: max_over_time(scrape_duration_seconds{job="federate"}[30m]) > 0.8 * 25
  for: 30m
  labels: {severity: ticket}
- alert: FederationTargetDown
  expr: up{job="federate"} == 0
  for: 5m
  labels: {severity: page}
- alert: FederationSamplesGrowing
  expr: scrape_samples_scraped{job="federate"} > 1.5 * scrape_samples_scraped{job="federate"} offset 7d
  for: 1h
```

## Staleness
Queries use the newest sample that is less than the lookback period old. The lookback period is 5 minutes by default (`--query.lookback-delta`, or the `lookback_delta` query parameter). A series is marked stale when a scrape no longer returns it, and a stale series returns no value in queries. Exporters that put their own timestamps on samples behave differently: a series that stops being exported keeps its last value for 5 minutes by default (the `track_timestamps_staleness` setting changes this).

## Gotchas
- `/federate` returns the series selected by the `match[]` parameters (union of all of them), so `scrape_samples_scraped` jumps when someone broadens `match[]`; review federation config changes.
- Federation needs `honor_labels: true` so labels from the source server are not overwritten.

## Checked
Date: 2026-11-07.
Confirmed by reading in full: the Federation page (`/federate`, `match[]` union, `honor_labels`), the Jobs and instances page (`up`, `scrape_duration_seconds`, `scrape_samples_scraped`, `scrape_timeout_seconds` behind the extra-scrape-metrics feature flag) and the Querying basics page including its Staleness section (5 minute lookback, `--query.lookback-delta`, `lookback_delta`, `track_timestamps_staleness`).
Removed because no cited page confirms them: the claim that federated series carry the leaf's timestamps and go stale at the next scrape, the `process_resident_memory_bytes` gotcha, and the invented Verify checklist. The alert thresholds are labelled as examples.
Method: documentation only; no commands were run.
