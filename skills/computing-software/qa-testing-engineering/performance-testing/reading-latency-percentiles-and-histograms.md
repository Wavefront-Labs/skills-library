---
id: computing-software.qa-testing-engineering.performance-testing.reading-latency-percentiles-and-histograms
name: reading-latency-percentiles-and-histograms
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [latency-histogram, hdrhistogram, percentiles, performance-analysis, tail-latency]
level: practitioner
status: verified
description: "Read latency distributions correctly: percentiles vs averages, histograms and HdrHistogram, why percentiles cannot be averaged, multimodal shapes, and tail amplification."
sources:
  - https://hdrhistogram.github.io/HdrHistogram/
  - https://www.brendangregg.com/FrequencyTrails/mean.html
  - https://grafana.com/docs/k6/latest/results-output/real-time/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading percentile distributions and histograms

## Why not averages
Latency is skewed (long right tail); the mean is pulled by outliers and hides both typical and worst experiences. Report p50 (typical), p95/p99 (tail), max (outliers), and count.

## Percentile basics
- p95 = 95% of requests were at or below this value.
- With fan-out, tail matters more: a page making 20 backend calls has a 1 - 0.99^20 = 18.2% chance of hitting at least one p99-slow call (computed, assuming independent calls).
- Percentiles need enough samples: p99 from 200 samples is 2 data points; report sample counts.

## Aggregation rules
- **Never average percentiles** across time windows, hosts or generators; the result is meaningless. Example computed here: host A with 9,000 requests (exponential, mean 50 ms) and host B with 1,000 slow requests (400 ms plus exponential): the average of the two p99 values was 428 ms while the true combined p99 was 515 ms.
- Merge histograms and compute percentiles from the merged histogram: with the Python `hdrhistogram` package, `a.add(b)` on the two hosts' histograms gave a p99 of 515.07 ms against 514.94 ms from the raw samples.
- Prometheus: `histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))`; the Prometheus docs show the same shape (`sum by (job, le)` to keep a label); bucket boundaries limit precision; choose buckets around your SLO values.

## HdrHistogram
Records values with configurable significant digits (the HdrHistogram docs example is 1 ns to 1 hour at 3 significant digits) in memory that is fixed regardless of the number of samples; wrk2 reports with it (its README mentions HdrHistograms and Coordinated Omission). Percentile distribution plots (log scale x-axis of percentile: 90%, 99%, 99.9%, 99.99%) show tail behaviour clearly.

## Histogram shapes and what they mean
- **Bimodal**: two populations (cache hit vs miss, two code paths, GC pauses). Split by tag before tuning.
- **Long flat tail**: queuing, lock contention, retries.
- **Spikes at fixed values**: timeouts (e.g. a cluster at exactly 5 s or 30 s = timeout + retry).
- **Comb pattern**: timer resolution or scheduler quantum.

## Over time
Plot percentiles per interval (heatmaps are best: time on x, latency buckets on y, colour = count) to see degradation during a test.

## Gotchas
- Closed-model tools under-report tails due to coordinated omission; prefer open models or corrected recording.
- Client-measured and server-measured latency differ by network and queueing; label which.

## Verify
Reports show p50/p95/p99/max with counts per transaction, percentiles come from merged histograms or raw data, and multimodal distributions are split and explained.

## Checked
Python 3.14 with NumPy and `hdrhistogram` in a scratch venv; fetched docs.
- Computed: 1 - 0.99^20 = 0.182; 1% of 200 samples = 2 points; average-of-p99 (428 ms) vs true p99 (515 ms) on a synthetic two-host sample (seeded NumPy); HdrHistogram merge (`add`) p99 515.07 ms vs raw 514.94 ms.
- Fetched: HdrHistogram project page (configurable significant digits, fixed memory footprint, 1 ns to 1 h at 3 digits example), wrk2 README (HdrHistogram, coordinated omission), Prometheus query-functions page (`histogram_quantile` examples), k6 real-time results page and Brendan Gregg's mean page (URLs live).
