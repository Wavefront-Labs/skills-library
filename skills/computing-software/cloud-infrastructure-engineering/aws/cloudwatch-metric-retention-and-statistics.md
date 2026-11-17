---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-metric-retention-and-statistics
name: cloudwatch-metric-retention-and-statistics
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch, metric-retention, metric-statistics, percentiles, get-metric-data, high-resolution-metrics]
level: practitioner
status: docs-checked
description: "Understand CloudWatch metric retention tiers (3 hours to 15 months), how data rolls up, choosing Average vs Maximum vs percentiles, and querying with GetMetricData."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Statistics-definitions.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_GetMetricData.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudWatch metric retention and statistics

## Retention and roll-up
| Period of data points | Kept for |
|---|---|
| < 60 s (high-resolution, 1/5/10/30 s) | 3 hours |
| 60 s | 15 days |
| 300 s (5 min) | 63 days |
| 3,600 s (1 hour) | 455 days (15 months) |
- Data is aggregated into the coarser periods as it ages: after 15 days you can no longer see
  1-minute detail, only 5-minute. Plan incident forensics accordingly (export what you need).
- Metrics cannot be deleted; they expire when no new data arrives for 15 months.
- For longer history: CloudWatch metric streams or periodic `get-metric-data` exports.

## Statistics
| Statistic | Use for |
|---|---|
| `Sum` | counts (requests, errors, bytes) |
| `Average` | utilisation over a fleet; hides spikes |
| `Maximum` / `Minimum` | queue age, worst-case latency, capacity floors |
| `SampleCount` | number of data points (requests for latency metrics) |
| `p50`, `p90`, `p99`, `p99.9` | latency SLOs |
| `tm99`, `TM(..)`, `IQM`, `WM(..)`, `TC(..)`, `TS(..)`, `PR(..)` | trimmed mean, interquartile mean, winsorized mean, trimmed count, trimmed sum, percentage of data points in a range |
- Percentiles need raw data points. A statistic set supports percentiles only if SampleCount is 1 with Min, Max and
  Sum equal, or Min equals Max and Sum equals Min times SampleCount. They are not available when any value is negative.
- Average of averages is wrong across dimensions; use Sum/SampleCount metric math.

## Query
```bash
aws cloudwatch get-metric-data --start-time 2026-10-17T00:00:00Z --end-time 2026-10-18T00:00:00Z \
  --metric-data-queries '[{"Id":"p99","MetricStat":{"Metric":{"Namespace":"AWS/ApplicationELB",
   "MetricName":"TargetResponseTime","Dimensions":[{"Name":"LoadBalancer","Value":"app/web/abc"}]},
   "Period":300,"Stat":"p99"}}]'
```
- `GetMetricData`: up to 500 metrics per call, metric math and one Metrics Insights query; it is priced differently from `GetMetricStatistics`.
- The start time is rounded down: to the minute if under 15 days old, to a 5-minute boundary for 15 to 63 days, to the hour beyond 63 days.
- `aws cloudwatch list-metrics` shows only metrics with data in the last 2 weeks.

## Gotchas
- 1-minute EC2 metrics need detailed monitoring; basic monitoring is 5-minute.
- Alarms on high-resolution metrics with 10/30 s periods cost more.
- Timestamps more than 2 weeks old cannot be published.

## Verify
- [ ] SLO dashboards use percentiles; capacity dashboards use Maximum where spikes matter.
- [ ] Data older than retention needed for compliance is exported.

## Checked
Checked 2026-10-27 against the live CloudWatch docs (current release).
- Metrics concepts and GetMetricData API reference: the four retention tiers (3 hours, 15 days, 63 days, 455 days), 15-month expiry, list-metrics hiding metrics with no data for two weeks, 2-week and 2-hour timestamp window, 500 metrics per GetMetricData call, start-time rounding.
- Statistics definitions: TM, IQM, WM, PR, TC, TS and tm99 forms; percentile rules for statistic sets.
- Metrics concepts: high-resolution alarms (10 s or 30 s) cost more.

Method: documentation only; no commands were run.
