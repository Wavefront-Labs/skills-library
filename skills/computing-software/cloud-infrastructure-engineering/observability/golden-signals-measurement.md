---
id: computing-software.cloud-infrastructure-engineering.observability.golden-signals-measurement
name: golden-signals-measurement
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [golden-signals, latency-measurement, latency-percentiles, traffic-metrics, error-rate-measurement, saturation-metrics, saturation-signal, tail-latency, worrying-about-the-tail, measurement-granularity, resolution-choice, promql]
level: practitioner
status: docs-checked
description: "Measure the four golden signals: success vs error latency, traffic, explicit/implicit/policy errors, saturation, tail latency buckets, histograms and measurement resolution."
sources: ["https://sre.google/sre-book/monitoring-distributed-systems/", "https://prometheus.io/docs/practices/histograms/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Measuring the four golden signals

## Latency: separate success from failure
Track latency of successful and failed requests separately: fast errors skew averages, and a slow error is worse than a fast one.
```promql
histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket{code!~"5.."}[5m])))   # successful
histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket{code=~"5.."}[5m])))   # failed
```
Classic histograms aggregate correctly with sum before histogram_quantile; averaging precomputed summary quantiles rarely makes sense. Prometheus advises native histograms where possible, then classic histograms with carefully chosen buckets, and summaries only when aggregation is not needed. Classic quantile error is bounded by the width of the bucket containing the quantile.

## Traffic and errors
Traffic is a system-specific demand metric such as HTTP requests per second. Errors are explicit (HTTP 500), implicit (a 200 with wrong content) or by policy (a response slower than the committed limit counts as an error).
```promql
sum(rate(http_requests_total[5m]))
sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
```

## Saturation
How full the service is, focused on its most constrained resource. Many systems degrade before 100 % utilisation, so set a utilisation target. Latency increases are often an early saturation signal, and predictions of future saturation count too.

## Worry about the tail
Averages hide problems: 100 ms average at 1,000 requests per second can still hide 1 % of requests taking 5 seconds. Count requests in latency buckets with roughly exponential boundaries about a factor of 3 apart (for example 0-10, 10-30, 30-100, 100-300 ms). For classic histograms, an SLO threshold needs a bucket at that exact boundary, otherwise results can be silently partial.

## Granularity
- Match resolution to the goal: minute-long CPU averages miss spikes that drive tail latency. The book's cheap approach is to sample CPU each second on the server, count samples into 5 % utilisation buckets, and aggregate every minute.
- For a 99.9 % availability target (about 9 hours down per year), probing more than once or twice a minute is probably unnecessary; checking disk fullness more often than every 1 to 2 minutes is excessive.

## Verify
- [ ] Service dashboard shows latency (success and error separately), traffic, errors and saturation
- [ ] Latency is bucketed, not averaged

## Checked

2026-11-08. Confirmed in the SRE book chapter: signal definitions, error kinds, tail example, bucket guidance, resolution examples. Confirmed on the Prometheus histograms page: aggregation, quantile error, exact-boundary warning, recommendation order. Removed as not on either page: the saturation alert expressions (pool ratio > 0.8, predict_linear), the 100-backend-calls p99 example, the 10 to 30 s CPU scrape advice, the 5m/30d alert-window claim and the scrape-interval consistency rule. The two PromQL latency queries are illustrative and use common instrument names rather than ones from the pages.
Method: documentation only; no commands were run.
