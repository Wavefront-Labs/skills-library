---
id: computing-software.cloud-infrastructure-engineering.aws.transfer-family-logging-and-monitoring
name: transfer-family-logging-and-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, transfer-family, transfer-logging, structured-logging, sftp, cloudwatch-logs, eventbridge]
level: practitioner
status: docs-checked
description: "Monitor Transfer Family servers and connectors: structured JSON logs to CloudWatch Logs, useful Logs Insights queries, metrics and alarms, workflow logs and EventBridge events."
sources: ["https://docs.aws.amazon.com/transfer/latest/userguide/structured-logging.html", "https://docs.aws.amazon.com/transfer/latest/userguide/metrics.html", "https://docs.aws.amazon.com/transfer/latest/userguide/eventbridge.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transfer Family logging and monitoring

## Structured logs
```bash
aws transfer update-server --server-id s-0123 \
  --structured-log-destinations arn:aws:logs:<REGION>:<ACCOUNT_ID>:log-group:/aws/transfer/s-0123
```
- All servers support structured logging, which AWS recommends for new and existing servers: logs arrive as JSON and
  CloudWatch Logs Insights discovers the JSON fields automatically.
- Console-created servers have logging enabled by default; change it later with `UpdateServer`
  (`StructuredLogDestinations`).
- A log group can be shared across several Transfer Family resources, which lets you manage retention in one place.
- Look at a sample event in your log group before writing Logs Insights queries; use the documented log schema for field names.
- Workflows without a structured log destination need a logging role on the server they are attached to.

## Metrics and alarms (AWS/Transfer)
- `BytesIn`, `BytesOut`, `FilesIn`, `FilesOut` per server. For SFTP/FTP/FTPS they are emitted every 5 minutes while a
  connection is established, with 0 when nothing transferred, so an alarm on `FilesIn` can catch a missing partner file.
- Workflow metrics such as `OnUploadExecutionsStarted` and `OnUploadExecutionsFailed`: alarm on failures.

## EventBridge
Transfer Family events use `source: aws.transfer`; rules can match on `detail-type`. Events cover SFTP/FTPS/FTP servers,
workflows and SFTP connectors (connector events are delivered on a durable basis).

## Audit
CloudTrail records Transfer Family API calls.

## Verify
- [ ] Log group receives events for a test login and upload.
- [ ] Missing-file alarm tested by skipping a test upload.

## Checked

2026-10-28. Confirmed against the Transfer Family User Guide pages structured-logging, log-server-manage, metrics, eventbridge and webapp-cloudtrail: structured JSON logging recommended for all servers, StructuredLogDestinations, shared log groups, metric names and 5-minute reporting, workflow metric names, `aws.transfer` event source and detail-type matching.
Removed: the log event type list, Logs Insights queries and field names (log schema page not fetched), per-user log stream and LoggingRole transition claims, connector metrics, Step Functions routing, and made-up account IDs. The prose-only `sources` were replaced with real URLs.
Method: documentation only; no commands were run.
