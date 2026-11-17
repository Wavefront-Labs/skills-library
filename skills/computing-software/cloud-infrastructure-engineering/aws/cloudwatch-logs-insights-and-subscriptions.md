---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-logs-insights-and-subscriptions
name: cloudwatch-logs-insights-and-subscriptions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch-logs, logs-insights, subscription-filter, log-retention, log-groups, log-class, infrequent-access, data-protection-policy, kinesis-firehose, cross-account-logs, metric-filters, live-tail, log-anomaly-detection, structured-logging, json-logs, export-to-s3]
level: practitioner
status: docs-checked
description: "Run CloudWatch Logs well: retention and log classes, structured JSON logging, Logs Insights queries that find the problem, subscription filters to Firehose/Lambda, and data protection policies."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch_Logs_Log_Classes.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/SubscriptionFilters.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html", "https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutSubscriptionFilter.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudWatch Logs — retention that does not surprise finance, queries that find the request

**Goal:** every log group has a retention and class, logs are structured JSON, Insights
answers "what happened to request X" in seconds, and anything needing long-term or
external analysis streams out via subscriptions.

## 1. Groups, retention, classes
- Default retention is **never expire**. Set it everywhere:
  `aws logs put-retention-policy --log-group-name /aws/lambda/x --retention-in-days 30`,
  and enforce it with automation that applies a default when a group is created
  (retention is a per-group setting; `put-account-policy` has no retention policy type).
- **Log classes**: `STANDARD` (full features) vs `INFREQUENT_ACCESS` (lower ingestion price only; no Live Tail, metric filters, subscription filters, field indexing, anomaly detection or embedded metric format, and no GetLogEvents/FilterLogEvents; data protection masking is supported). Chosen at
  creation, cannot be changed. Use IA for chatty debug/audit logs you query rarely.
- Standard and Infrequent Access differ in ingestion price only (see the pricing page for rates): cut volume at the source (log level,
  sampling) as well as setting retention.
- Naming: `/<env>/<service>/<component>`; Lambda/ECS create groups automatically — pre-create
  them in IaC with retention and KMS key so the defaults never apply.
- KMS encryption with a customer key via `associate-kms-key`; the key policy must allow
  `logs.<region>.amazonaws.com`.

## 2. Structured logging
- Emit one JSON object per line with `level`, `msg`, `requestId`/`traceId`, `service`,
  plus EMF for metrics. Insights auto-parses JSON into fields; plain text needs `parse`.
- Lambda: enable **JSON log format** (`LoggingConfig: {LogFormat: JSON, ApplicationLogLevel: INFO}`)
  and route to a custom group (`LogGroup`).

## 3. Logs Insights queries you will reuse
```sql
-- errors by message, last hour
fields @timestamp, @message | filter level = "ERROR" | stats count(*) as n by msg | sort n desc | limit 20
-- one request across services (query multiple groups)
fields @timestamp, service, msg | filter requestId = "abc-123" | sort @timestamp asc
-- Lambda duration p99
filter @type = "REPORT" | stats pct(@duration, 99) as p99 by bin(5m)
-- parse unstructured nginx
parse @message /(?<ip>\S+) - - \[(?<ts>[^\]]+)\] "(?<method>\S+) (?<path>\S+)[^"]*" (?<status>\d+)/ | stats count(*) by status
-- 5xx count by path
filter status >= 500 | stats count(*) as n by path | sort n desc
```
- Select up to 50 log groups per query (the `SOURCE` command, CLI and API only, selects more);
  narrow the time range first — cost is per GB scanned.
- Save queries (`put-query-definition`); `unmask` requires permission when data protection is on.
- **Live Tail** for watching deploys; **anomaly detection** per group flags new error patterns automatically.
- Natural-language query generation exists in the console; verify what it wrote.

## 4. Subscription filters (stream out)
| Destination | Use |
|---|---|
| **Firehose** | Delivery to the destinations Firehose supports (for example S3) for archive or analysis |
| **Lambda** | Real-time processing in a function in the same account; watch concurrency |
| **Kinesis Data Streams** | Streaming to consumers; the target of a cross-account destination |
| **OpenSearch Service** | Direct subscription to an OpenSearch Service domain |
```bash
aws logs put-subscription-filter --log-group-name /prod/api --filter-name to-firehose \
  --filter-pattern '{ $.level = "ERROR" || $.level = "WARN" }' \
  --destination-arn arn:aws:firehose:…:deliverystream/logs --role-arn arn:aws:iam::…:role/CWLtoFirehose
```
- Up to 5 subscription filters per log group (quota read 2026-10-27; the PutSubscriptionFilter API page still says two) and one account-level filter per Region. Payloads are base64 encoded and gzip compressed, and Kinesis and Lambda destinations can receive `CONTROL_MESSAGE` records, so handle them. The filter pattern selects *which events* leave.
- Cross-account: a **destination** (`put-destination`) in the central account wrapping a
  Kinesis stream, with an access policy allowing source accounts; **account-level
  subscription filters** (`put-account-policy --policy-type SUBSCRIPTION_FILTER_POLICY`)
  apply to all groups at once.
- One-off export: `create-export-task` to S3 (a one-off export of a time range, not a streaming mechanism).

## 5. Data protection
`put-data-protection-policy` with managed identifiers (`EmailAddress`, `CreditCardNumber`,
`AwsSecretKey`…) audits and masks matches at ingestion (Standard and Infrequent Access classes); `logs:Unmask` lets investigators see raw. Also available account-wide.

## 6. Cost control checklist
- Retention ≤ 30–90 d in CloudWatch; archive via subscription to S3 for anything longer.
- Lambda `ApplicationLogLevel: WARN` in prod for noisy functions; sample INFO.
- Consider sending VPC Flow Logs to S3 directly instead of CloudWatch Logs; compare current prices.
- Insights on IA class for debug streams; metric filters stay on standard groups only.
- Monitor `IncomingBytes` per group with a top-N Insights-free dashboard; alarm on daily anomalies.

## Gotchas
- Metric filters, subscriptions and Live Tail do not exist on IA-class groups — pick class deliberately.
- Changing retention does not delete old data instantly; events are removed up to 72 hours after they expire.
- Subscription to Lambda with a pattern matching everything = Lambda concurrency = your log rate.
- Queries time out after 60 minutes: narrow the range; `limit` on `start-query` can reach 100,000 events.
- Nested JSON fields are referenced with dot notation (for example `detail.status`).

## Verify
- [ ] `describe-log-groups --query 'logGroups[?!retentionInDays].logGroupName'` returns nothing.
- [ ] A request id from an ALB 5xx can be followed through ALB → API → DB logs in one Insights query.
- [ ] Subscription delivers an ERROR line to S3 within the Firehose buffer window; an INFO line does not.
- [ ] Data protection masks a test email address (query with and without `unmask`).
- [ ] Monthly `IncomingBytes` per group is on a dashboard and the top group has a known owner.

## Checked
Checked 2026-10-27 against the live CloudWatch Logs docs (current release), the botocore logs 2014-03-28 and lambda 2015-03-31 models.
- Log classes page: Infrequent Access feature table (no Live Tail, metric filters, subscription filters, field indexing, anomaly detection, embedded metric format, GetLogEvents/FilterLogEvents; masking supported), class fixed at creation, ingestion-only price difference. Natural language query assist and anomaly detection are Standard features.
- Subscriptions pages and quotas: destinations (Firehose, Lambda, Kinesis Data Streams, OpenSearch Service), base64 and gzip payloads, CONTROL_MESSAGE records, 5 filters per log group (the PutSubscriptionFilter API page still says two), one account-level filter per Region; PutDestination targets a Kinesis stream; botocore PutAccountPolicy enumerates DATA_PROTECTION, SUBSCRIPTION_FILTER, FIELD_INDEX, TRANSFORMER and METRIC_EXTRACTION policy types (no retention type).
- Data protection page: masking at ingestion, logs:Unmask, both log classes; managed identifier names EmailAddress, CreditCardNumber, AwsSecretKey on the managed identifiers page. KMS page: logs.<region>.amazonaws.com service principal in the key policy.
- Query syntax and StartQuery pages: 50 log groups, SOURCE, 60-minute timeout, limit up to 100,000; discovered fields page: dot notation and @duration. botocore lambda: LoggingConfig LogFormat, ApplicationLogLevel and LogGroup. PutRetentionPolicy: up to 72 hours deletion delay. Logs metrics page: IncomingBytes.
- Removed unconfirmed claims: percentage and dollar figures, 10x cost claim, ECS and EKS logging advice, Lambda requestId remark, audit finding destinations, cold start query field.

Method: documentation only; no commands were run.
