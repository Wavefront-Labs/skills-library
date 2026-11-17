---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-metrics-and-alarms
name: cloudwatch-metrics-and-alarms
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch, cloudwatch-alarm, cloudwatch-alarms, custom-metrics, composite-alarm, metric-math, anomaly-detection, embedded-metric-format, emf, putmetricdata, treat-missing-data, datapoints-to-alarm, percentile, sns-actions, alarm-actions, high-resolution-metrics, metric-filters, slo-alarms]
level: practitioner
status: docs-checked
description: "Design CloudWatch metrics and alarms that page for real problems: custom metrics via EMF, metric math and percentiles, M-of-N evaluation, missing-data handling and composite alarms."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Create_Composite_Alarm.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudWatch metrics and alarms — fewer pages, each one true

**Goal:** the metrics that describe user experience exist, alarms evaluate them with the
right window and missing-data rules, and composite alarms turn ten symptoms into one page.

## 1. Metrics basics you design around
- Namespace / metric name / up to 30 dimensions; **each unique dimension set is a separate
  metric** and billed as a custom metric. High-cardinality dimensions
  (request id, user id) are a cost bomb — put those in logs, not metric dimensions.
- Standard resolution 60 s; **high-resolution** 1 s (`StorageResolution=1`) for things like
  Lambda concurrency bursts; retained at full resolution 3 h, then rolled up.
- Statistics: `Average` lies for latency; use `p99`/`p95` (extended statistics) on
  metrics that support percentiles: custom metrics published as raw data points and some AWS service metrics.
- Percentiles are unavailable for metrics published only as pre-aggregated `StatisticValues` (apart from trivial sets) and when any value is negative — publish raw values or EMF.

## 2. Custom metrics: EMF, not PutMetricData loops
```json
{"_aws":{"Timestamp":1718000000000,"CloudWatchMetrics":[{"Namespace":"Shop","Dimensions":[["Service"]],"Metrics":[{"Name":"CheckoutLatency","Unit":"Milliseconds"}]}]},
 "Service":"checkout","CheckoutLatency":183,"orderId":"…","tenant":"…"}
```
- Write that line to stdout (Lambda) or the CloudWatch agent/FireLens; CloudWatch extracts
  the metric from the log line (**no `PutMetricData` calls from your code**) and keeps the full log line
  for Logs Insights with the high-cardinality fields.
- Libraries: open-source EMF client libraries exist for Node.js, Python, Java and C#.
- `PutMetricData` is fine for batch jobs (up to 1,000 metrics per call, and `Values`/`Counts` carry up to 150 values per metric); never per request.
- **Metric filters** turn log patterns into metrics (for space-delimited logs, for example
  `[..., request =*.html*, status_code = 4*, bytes]`); set a default value so the metric has data when nothing matches.

## 3. Alarm anatomy
```bash
aws cloudwatch put-metric-alarm --alarm-name api-p99-latency \
  --namespace AWS/ApiGateway --metric-name Latency --dimensions Name=ApiName,Value=shop \
  --extended-statistic p99 --period 60 --evaluation-periods 5 --datapoints-to-alarm 3 \
  --threshold 800 --comparison-operator GreaterThanThreshold \
  --treat-missing-data notBreaching --alarm-actions arn:aws:sns:…:oncall --ok-actions arn:aws:sns:…:oncall
```
- **M of N** (`datapoints-to-alarm 3` of `evaluation-periods 5`) absorbs single spikes.
- `treat-missing-data` takes `breaching`, `notBreaching`, `ignore` or `missing` (the default). Pick deliberately: `notBreaching` suits sparse metrics such as error counts, `breaching` suits heartbeat-style metrics that must report on schedule. Choosing wrong means a silent outage or flapping.
- Choose an alarm period at least as long as the metric's resolution (for example 300 s on EC2 basic monitoring metrics).
- Alarm on **rates**, not counts: metric math `errors / requests * 100`
  (`--metrics` with `Id`, `Expression`, `ReturnData`). `FILL(m1, 0)` to make gaps zero.
- Actions: SNS notifications, Auto Scaling policies, EC2 stop/terminate/reboot/recover, SSM OpsItems.
  Add `--ok-actions` so resolution auto-closes the page.

## 4. Anomaly detection
`--threshold-metric-id ad1` with `ANOMALY_DETECTION_BAND(m1, 2)` learns daily/weekly
seasonality; use for traffic volume, request count, cost — things with a pattern but no fixed
threshold. Not for latency SLOs (those have a number). The model trains on up to two weeks of data (it can be enabled with less); exclude
known incident windows from training.

## 5. Composite alarms: the page
```
ALARM("api-5xx-rate") OR (ALARM("api-p99-latency") AND ALARM("db-cpu-high"))
```
- Typically give child alarms no actions so only the composite pages. Add `--actions-suppressor`
  (a maintenance/deploy alarm) with extension/wait periods to mute during deploys.
- Pattern: one composite per service = "service unhealthy", children = symptoms; dashboards
  show children for diagnosis.

## 6. Which metrics to alarm on (per service, the usual suspects)
| Service | Page-worthy |
|---|---|
| ALB | `HTTPCode_Target_5XX_Count`/`RequestCount` rate, `TargetResponseTime p99` |
| Lambda | `Errors`/`Invocations`, `Throttles`, `IteratorAge`, `ConcurrentExecutions` near limit |
| SQS | `ApproximateAgeOfOldestMessage`, DLQ `ApproximateNumberOfMessagesVisible` > 0 |
| RDS | `CPUUtilization`, `FreeableMemory`, `FreeStorageSpace`, `DatabaseConnections` vs max, `ReadLatency/WriteLatency` |
| DynamoDB | `SystemErrors`, `SuccessfulRequestLatency p99` |
| EC2 | `StatusCheckFailed_System` → recover action; CPU only with agent memory/disk |

## Gotchas
- Alarm state `INSUFFICIENT_DATA` at creation is normal; permanently insufficient = wrong
  dimensions (case-sensitive, exact values) or period.
- `Average` of `Latency` over 5 min hides p99 spikes; the SLO is a percentile.
- Deleting a metric is impossible; stopping publishing makes it vanish from lists after 2 weeks (data kept 15 months).
- Custom metric pricing is not stated here: check the CloudWatch pricing page.

## Verify
- [ ] Every page-level alarm has `treat-missing-data` chosen deliberately (documented).
- [ ] Simulate: `set-alarm-state --state-value ALARM --state-reason test` on a child → composite pages once.
- [ ] A deploy flips the suppressor alarm and the composite stays quiet.
- [ ] The service dashboard shows p99 latency and error *rate*, not raw counts.
- [ ] EMF lines in logs produce the metric, and Logs Insights can query the same line.

## Checked
Checked 2026-10-27 against the live CloudWatch docs (current release) and the botocore cloudwatch 2010-08-01 model.
- Metrics concepts, PutMetricData and statistics pages: 30 dimensions, 1 s storage resolution, 3-hour retention at full resolution, percentile rules, 1,000 metrics and 150 values limits, metrics cannot be deleted.
- PutMetricAlarm API reference and botocore: CLI flags in the example, treat-missing-data values and default, --threshold-metric-id; anomaly detection page: ANOMALY_DETECTION_BAND, two-week training window, excluding periods; metric math page: FILL and ANOMALY_DETECTION_BAND forms.
- Alarm actions page: EC2 stop, terminate, reboot, recover and Systems Manager OpsItem actions; StatusCheckFailed_System with recover.
- Recommended-alarms page: the listed ALB, Lambda, SQS, RDS and DynamoDB metric names; names it does not list were removed. EMF client libraries page: Node.js, Python, Java, C#. Metric filter pages: default value and the space-delimited pattern form.
- Removed unconfirmed claims: custom metric price, no-throttling and asynchronous EMF behaviour, cross-region alarm remark, email reliability remark.

Method: documentation only; no commands were run.
