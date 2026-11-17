---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-logs-putlogevents-streams-and-ingestion-quotas
name: cloudwatch-logs-putlogevents-streams-and-ingestion-quotas
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch-logs, put-log-events, log-streams, ingestion-quotas, log-groups, throttling]
level: practitioner
status: docs-checked
description: "Ship logs to CloudWatch Logs with PutLogEvents correctly: batch size and event limits, time window rules, stream naming, quotas and throttling, and retention per log group."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutLogEvents.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/cloudwatch_limits_cwl.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch_Logs_Log_Classes.html", "https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutRetentionPolicy.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudWatch Logs: PutLogEvents, log streams and ingestion quotas

## Model
Log group (retention, KMS, log class, subscriptions) -> log streams (one per source: instance id,
container id, Lambda execution environment) -> events (timestamp + message).

## PutLogEvents rules
```python
logs.put_log_events(logGroupName="/app/orders", logStreamName=f"{host}/{pid}",
    logEvents=[{"timestamp": int(time.time()*1000), "message": json.dumps(rec)} for rec in batch])
```
- Batch maximum 1,048,576 bytes, computed as sum of UTF-8 message sizes plus 26 bytes per event; maximum 10,000 events per batch.
- Events in a batch must be in chronological order and span no more than 24 hours.
- Timestamps cannot be more than 14 days in the past or 2 hours in the future (or older than the group's retention); such events are rejected (`rejectedLogEventsInfo` in the response, not an exception).
- Sequence tokens are no longer required (ignored); concurrent writers to one stream are allowed.
- Each log event can be at most 1 MB (1,024 KB per the quotas page).

## Quotas
- PutLogEvents is throttled per account per Region (5,000 requests per second default, adjustable, as read on the quotas page on 2026-10-27; the per-stream limit of five requests per second was removed);
  over it returns `ThrottlingException`: batch more and retry with backoff.
- Prefer fewer, larger batches (agents flush every few seconds or at size thresholds).
- `CreateLogStream` (50 per second default) and `DescribeLogStreams` (25 per second default) have far lower limits than PutLogEvents; create streams once per process, never per batch, and never call DescribeLogStreams in a hot path.

## Retention and classes
```bash
aws logs put-retention-policy --log-group-name /app/orders --retention-in-days 30
aws logs create-log-group --log-group-name /app/audit --log-group-class INFREQUENT_ACCESS
```
- Default retention is **never expire** (`delete-retention-policy` restores it): set it on every group (auto-created Lambda groups included). Allowed `retentionInDays` values are a fixed list (1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, 3653); events are removed up to 72 hours after expiry.
- Infrequent Access differs from Standard in ingestion price only, cannot be changed after creation, and lacks metric filters, subscription filters, Live Tail, field indexing, anomaly detection, embedded metric format and GetLogEvents/FilterLogEvents (use Logs Insights).

## Gotchas
- Stream names cannot contain `:` or `*`; use `/` separators.
- Embedded Metric Format (`_aws` JSON) turns log lines into metrics at ingestion.

## Verify
- [ ] Shipper handles `rejectedLogEventsInfo` and `ThrottlingException` with retry.
- [ ] Every log group has retention set (`describe-log-groups --query 'logGroups[?!retentionInDays].logGroupName'` is empty).

## Checked
Checked 2026-10-27 against the live CloudWatch Logs docs (current release).
- PutLogEvents API reference: 1,048,576-byte batch plus 26 bytes per event, 10,000 events, 2-hour future and 14-day past limits, 24-hour span, chronological order, 1 MB per event, sequence token ignored, per-stream limit removed, rejectedLogEventsInfo.
- CreateLogStream API reference: colon and asterisk not allowed in stream names.
- Logs quotas page: PutLogEvents 5,000 per second, CreateLogStream 50, DescribeLogStreams 25, event size 1,024 KB (all adjustable except event size).
- PutRetentionPolicy API reference: allowed retention values and the up-to-72-hour deletion delay; log classes page: feature table.

Method: documentation only; no commands were run.
