---
id: computing-software.cloud-infrastructure-engineering.aws.reducing-cloudwatch-logs-cost
name: reducing-cloudwatch-logs-cost
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch-logs, logs-cost, infrequent-access-log-class, log-retention, log-ingestion, cost-optimization]
level: practitioner
status: draft
description: "Cut CloudWatch Logs spend: find top ingesting log groups, set retention everywhere, lower log levels, use Infrequent Access class, route bulk logs to S3, and price queries."
sources: ["https://aws.amazon.com/cloudwatch/pricing/", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch_Logs_Log_Classes.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_billing.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reducing CloudWatch Logs cost

## 1. Where the money goes
- **Ingestion** per GB (by far the largest for most accounts); vended logs (VPC Flow Logs,
  Route 53 Resolver, Lambda via tiered pricing...) have volume-tiered rates.
- **Storage** per GB-month after compression (cheap, but forever by default).
- **Logs Insights** per GB scanned; Live Tail per minute; subscription filters and
  metric filters themselves are free but their destinations cost.

## 2. Find the top offenders
```bash
aws cloudwatch get-metric-data --start-time $(date -u -d '-7 days' +%FT%TZ) --end-time $(date -u +%FT%TZ) \
  --metric-data-queries '[{"Id":"q","Expression":"SELECT SUM(IncomingBytes) FROM SCHEMA(\"AWS/Logs\", LogGroupName) GROUP BY LogGroupName ORDER BY SUM() DESC LIMIT 20","Period":604800}]'
```
Cost Explorer: service CloudWatch, usage type `*DataProcessing-Bytes` (ingestion) and
`*TimedStorage-ByteHrs`, grouped by resource with resource-level CUR data.

## 3. Fixes, in order of impact
1. **Reduce volume at source**: drop DEBUG in production (Lambda advanced logging
   controls `ApplicationLogLevel=INFO`, `SystemLogLevel=WARN`), stop logging full request
   bodies, sample high-volume success logs, remove duplicate logging (app + sidecar both
   shipping).
2. **Retention on every group**: none set = kept forever.
```bash
for lg in $(aws logs describe-log-groups --query 'logGroups[?!retentionInDays].logGroupName' --output text); do
  aws logs put-retention-policy --log-group-name "$lg" --retention-in-days 30; done
```
   Enforce with a Config rule (`cw-loggroup-retention-period-check`) or an EventBridge
   rule on `CreateLogGroup` that applies a default.
3. **Infrequent Access log class** for logs kept for audit/occasional search: about half the
   ingestion price; supports Logs Insights queries but not metric filters, subscription
   filters, Live Tail, anomaly detection or data protection. Class is chosen at log group
   creation (create a new group and switch the producer).
4. **Send bulk logs elsewhere**: VPC Flow Logs, ALB, CloudFront logs straight to S3 (cheaper
   delivery) and query with Athena; use Firehose for streaming to S3 when needed.
5. **Query cost**: narrow time ranges, query specific log groups, use field indexes so
   Insights scans less, save frequent queries as metrics (metric filters) rather than
   running scans.

## 4. Guardrails
- Budget alert on CloudWatch service cost; anomaly detection monitor per service.
- Tag log groups by owner (tags propagate in CUR for showback).
- Review new log groups weekly via the top-20 query.

## Gotchas
- Lowering retention deletes old data irreversibly; export to S3 first if compliance needs it.
- Lambda creates log groups automatically without retention; define them in IaC (or use the
  function's `LoggingConfig.LogGroup` pointing to a managed group).
- Vended log pricing changes by volume tier; do not assume flat per-GB costs in estimates.

## Verify
- [ ] No log group without retention (query returns empty).
- [ ] Top 20 groups reviewed; ingestion trending down after source fixes.
- [ ] Audit-only logs moved to IA class or S3.
