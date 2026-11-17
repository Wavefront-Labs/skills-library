---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-metrics-insights-queries
name: cloudwatch-metrics-insights-queries
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch, metrics-insights, sql, fleet-monitoring, alarms, dashboards]
level: practitioner
status: docs-checked
description: "Query CloudWatch metrics with Metrics Insights SQL: SELECT/FROM SCHEMA/WHERE/GROUP BY/ORDER BY/LIMIT, top-N fleet views, tag-based queries, and alarms on a query."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/query_with_cloudwatch-metrics-insights.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-metrics-insights-querylanguage.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-metrics-insights-alarms.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudWatch Metrics Insights queries

**Use:** fleet-wide "top N" and aggregate views that would otherwise need one metric per
resource on a dashboard — and alarms that automatically cover new resources.

## 1. Grammar
```
SELECT FUNCTION(metricName)
FROM namespace | SCHEMA(namespace[, dimension...])
[WHERE dimension = 'value' [AND ...]]
[GROUP BY dimension[, ...]]
[ORDER BY FUNCTION() [ASC|DESC]]
[LIMIT n]
```
Functions: `AVG`, `MAX`, `MIN`, `SUM`, `COUNT`. Queries for graphs and widgets can cover up to two weeks of data;
alarm condition evaluation can use only the most recent three hours. Keywords are case-insensitive, identifiers
(metric, namespace, dimension names) are case-sensitive.

## 2. Examples
Top 10 busiest EC2 instances:
```sql
SELECT AVG(CPUUtilization) FROM SCHEMA("AWS/EC2", InstanceId)
GROUP BY InstanceId ORDER BY AVG() DESC LIMIT 10
```
Lambda errors by function, only prod-tagged functions:
```sql
SELECT SUM(Errors) FROM SCHEMA("AWS/Lambda", FunctionName)
WHERE tag.env = 'prod'
GROUP BY FunctionName ORDER BY SUM() DESC LIMIT 20
```
`SCHEMA("AWS/EC2", InstanceId)` restricts to metrics with exactly that dimension set
(excluding the aggregated ones), avoiding double counting. Tag filters in alarm queries need
**Enable resource tags on telemetry** turned on under CloudWatch Settings.

## 3. Use from the CLI / dashboards
```bash
aws cloudwatch get-metric-data --start-time $(date -u -d '-1 hour' +%FT%TZ) --end-time $(date -u +%FT%TZ) \
  --metric-data-queries '[{"Id":"q1","Expression":"SELECT MAX(ApproximateAgeOfOldestMessage) FROM SCHEMA(\"AWS/SQS\", QueueName) GROUP BY QueueName ORDER BY MAX() DESC LIMIT 5","Period":300}]'
```
Dashboards: add a widget with the query in the Metrics Insights query builder.

## 4. Alarm on a query
An alarm on a single-series query result (e.g. `SELECT MAX(CPUUtilization) FROM SCHEMA("AWS/EC2", InstanceId)`)
fires if *any* instance is hot — new instances are covered automatically.

## Gotchas
- A query processes at most 10,000 metrics and returns at most 500 time series; with `ORDER BY` the 500 returned are the highest or lowest by that ordering, without it you cannot control which 500.
- At most 200 Metrics Insights alarms per Region; high-resolution (sub-minute) data is returned at one-minute granularity.
- Each `GetMetricData` call can include only one Metrics Insights query.

## Verify
- [ ] Dashboard shows a top-N widget per critical namespace (EC2, Lambda, SQS, RDS).
- [ ] A query-based alarm fires when one test resource breaches, without per-resource alarm setup.

## Checked
Checked 2026-10-27 against the live CloudWatch docs (current release).
- Query components and syntax page: grammar, the five functions, SCHEMA semantics, tag.keyName filters, ORDER BY with LIMIT, maximum LIMIT of 500.
- Metrics Insights quotas page: two-week query window, 10,000 metrics processed, 500 time series returned, 200 alarms per Region, one-minute granularity, one query per GetMetricData.
- Metrics Insights alarms page: alarms track new resources automatically; tag use needs Enable resource tags on telemetry; GetMetricData API page: alarm evaluation uses the most recent three hours.
- Removed claims no page confirmed: multi-series alarm behaviour, mixing with metric math, dashboard JSON key, approximate results.

Method: documentation only; no commands were run.
