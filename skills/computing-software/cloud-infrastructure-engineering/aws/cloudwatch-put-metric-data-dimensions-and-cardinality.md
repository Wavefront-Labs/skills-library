---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-put-metric-data-dimensions-and-cardinality
name: cloudwatch-put-metric-data-dimensions-and-cardinality
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch, put-metric-data, metric-dimensions, metric-cardinality, custom-metrics, statistic-sets]
level: practitioner
status: docs-checked
description: "Publish custom CloudWatch metrics without runaway cost: PutMetricData batching and statistic sets, dimension design, cardinality math, high resolution, and EMF as the alternative."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutMetricData.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Dimension"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PutMetricData, dimensions and cardinality

## 1. A metric is namespace + name + unique dimension set
`Namespace=Shop, MetricName=Latency, Dimensions={Service=checkout, Region=eu-west-1}` is one
metric; adding `Customer=12345` creates a new metric **per customer**. Each unique
combination is billed as a custom metric per month. 10 services x 3 regions x 50,000
customers = 1.5 million metrics: a very large bill. Never put unbounded values (user IDs,
request IDs, URLs with IDs, IPs) in dimensions.

## 2. Dimension design
- Up to 30 dimensions per metric; keep 1-3 low-cardinality ones (service, operation,
  environment, AZ).
- CloudWatch does **not aggregate across dimensions** for you: if you publish with
  `{Service, Operation}` only, you cannot graph per-Service totals unless you also publish
  `{Service}` (or use Metrics Insights `SUM ... GROUP BY`, or metric math `SEARCH`).
  Decide which roll-ups you need and publish them deliberately (each is another metric).
- Put high-cardinality context into logs (EMF properties) instead of dimensions.

## 3. Publishing efficiently
```bash
aws cloudwatch put-metric-data --namespace Shop --metric-data '[
  {"MetricName":"Latency","Dimensions":[{"Name":"Service","Value":"checkout"}],
   "Unit":"Milliseconds","StatisticValues":{"SampleCount":250,"Sum":31250,"Minimum":12,"Maximum":890}},
  {"MetricName":"Orders","Dimensions":[{"Name":"Service","Value":"checkout"}],"Unit":"Count","Value":42}]'
```
- Up to 1,000 metrics per call (and 1 MB payload); batch in the client.
- **Statistic sets** aggregate client-side (count, sum, min, max) to cut API calls; but
  percentiles need raw values: use `Values`/`Counts` arrays (up to 150 values per
  metric per request) for percentile support.
- `StorageResolution=1` makes it high resolution (1-second); alarms can use 10 s or 30 s
  periods; costs more (and API volume).
- API calls are charged per 1,000 requests: per-request publishing from hot code paths is
  expensive and adds latency. Use async batching (CloudWatch agent StatsD, EMF, SDK
  buffering).

## 4. EMF instead of PutMetricData
Embedded Metric Format: write JSON logs that CloudWatch Logs converts to metrics. No API
calls from the app, high-cardinality properties stay in the log for drill-down, only listed
`Dimensions` become metric dimensions. The EMF client libraries suit Lambda and agent-based hosts.

## 5. Find cardinality problems
```bash
aws cloudwatch list-metrics --namespace Shop --metric-name Latency --query 'length(Metrics)'
```
Cost Explorer usage type `CW:MetricMonitorUsage` trend; Metrics Insights
`SELECT COUNT(Latency) FROM Shop GROUP BY Customer` style queries to see dimension spread.
Metrics cannot be deleted; they expire after 15 months of no data (billing stops when you
stop publishing, prorated hourly).

## Verify
- [ ] Dimension values are bounded (documented allow-list per dimension).
- [ ] Custom metric count per namespace within budget; no growth with user count.
- [ ] Publishing is batched (API request count per minute small and steady).

## Checked
Checked 2026-10-27 against the live CloudWatch docs (docs.aws.amazon.com, current release) and the botocore cloudwatch 2010-08-01 model.
- PutMetricData API reference: 1,000 metrics per call, 1 MB per request, 30 dimensions per metric, Values/Counts limited to 150 values per metric per request, StorageResolution.
- Metrics concepts: 10 s and 30 s high-resolution alarm periods, metrics cannot be deleted and expire after 15 months without data, no aggregation across dimensions for custom metrics.
- Billing page: MetricMonitorUsage usage type, custom metrics prorated by the hour, API requests billed per 1,000.
- EMF specification: only DimensionSet keys become metric dimensions and every DimensionSet creates a new metric.
No prices or quotas beyond those pages are stated.

Method: documentation only; no commands were run.
