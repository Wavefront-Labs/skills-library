---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-logs-pattern-analysis-and-time-comparison
name: cloudwatch-logs-pattern-analysis-and-time-comparison
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch-logs, pattern-analysis, logs-insights, log-anomaly-detection, compare-time-ranges, incident-triage]
level: practitioner
status: docs-checked
description: "Triage incidents from logs with CloudWatch Logs Insights pattern analysis: the pattern command, comparing against a previous period, and log anomaly detectors."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_AnalyzeLogData_Patterns.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-Pattern.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-Diff.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/LogsAnomalyDetection.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logs Insights pattern analysis and comparing time ranges

**Goal:** in the first ten minutes of an incident, see which kinds of log lines are new or
spiking, without knowing what to search for.

## Patterns
```
fields @timestamp, @message
| filter @logStream like /orders/
| pattern @message
| sort @sampleCount desc
```
- Groups messages into templates, replacing variable parts with tokens such as `<Time-1>` or `<Token-1>`, and returns
  `@pattern`, `@sampleCount`, `@ratio` and `@severityLabel` per pattern. Input can be `@message`, a field extracted with `parse`, or a string-function result.
- The console's **Patterns** tab shows the patterns found for a query result, with event ratio and log samples.
- Works across multiple log groups selected in the query.

## Compare with a previous period
- The `diff` command compares the selected time range with the immediately preceding range of equal length;
  `diff previousDay`, `diff previousWeek` and `diff previousMonth` compare with the same time one day, week or month earlier.
  It shows whether log events are new and how trends changed. Log groups in the Infrequent Access class do not support `diff` or `pattern`.
- Start the incident query with the alert window vs a baseline window of equal length.

## Log anomaly detection
```bash
aws logs create-log-anomaly-detector --log-group-arn-list "$LG_ARN" \
  --evaluation-frequency FIFTEEN_MIN --anomaly-visibility-time 21
aws logs list-anomalies --anomaly-detector-arn "$DET"
```
- Trains on the past two weeks of log events (training can take up to 15 minutes), then analyses incoming logs and flags significant fluctuations as anomalies. `--anomaly-visibility-time` accepts 7 to 90 days.
- Anomalies can be suppressed temporarily or permanently, and alarms can be created for log anomaly detectors.

## Triage flow
1. Pattern query over affected services' log groups for the alert window, compare to baseline.
2. Open the top new/increased pattern, pull samples, note a request id or trace id.
3. Pivot with `filter @message like /<id>/` across groups or follow the trace id.

## Gotchas
- Combine `pattern` with `filter`, `parse` and `sort`: filter first to the relevant groups and level (`filter level = "ERROR"`).
- JSON logs: run patterns on the message field (`pattern msg`) or a `parse`-extracted field rather than the whole JSON object for meaningful templates.
- Cost is per GB scanned like any Logs Insights query; narrow time and groups.

## Verify
- [ ] Saved query exists per service for "patterns, compare to last week".
- [ ] Anomaly detector enabled on critical log groups with alerts routed.

## Checked
Checked 2026-10-27 against the live CloudWatch Logs docs (current release) and the botocore logs 2014-03-28 model.
- pattern command page: @pattern, @ratio, @sampleCount, @severityLabel, token forms, valid inputs, combination with filter, parse and sort; Pattern analysis page: Patterns tab with event ratio and log samples.
- diff command page: previous range and previousDay, previousWeek, previousMonth modifiers; query syntax page: Infrequent Access class does not support pattern, diff or unmask.
- Log anomaly detection page: two-week training, up to 15 minutes, suppression, alarms; botocore: create-log-anomaly-detector (evaluationFrequency enum includes FIFTEEN_MIN, anomalyVisibilityTime 7 to 90) and list-anomalies --anomaly-detector-arn.
- Removed unconfirmed claims: the @visualization field, percentage-change marking in the Compare view and the combined pattern-then-diff query.

Method: documentation only; no commands were run.
