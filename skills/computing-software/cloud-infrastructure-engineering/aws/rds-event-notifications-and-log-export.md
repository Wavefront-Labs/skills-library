---
id: computing-software.cloud-infrastructure-engineering.aws.rds-event-notifications-and-log-export
name: rds-event-notifications-and-log-export
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, rds, rds-events, rds-log-export, event-subscription, cloudwatch-logs, slow-query-log]
level: practitioner
status: docs-checked
description: "Get alerted on RDS failovers, reboots and storage events with event subscriptions or EventBridge, and publish engine logs (error, slow query, audit, postgres) to CloudWatch Logs."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Events.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Events.Messages.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Procedural.UploadtoCloudWatch.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDS event notifications and log export

## 1. Events
RDS emits events for instances, clusters, snapshots, parameter groups, security groups,
proxies and blue/green deployments. Categories include `availability`, `backup`,
`configuration change`, `deletion`, `failover`, `failure`, `low storage`, `maintenance`,
`notification`, `recovery`, `restoration`.
```bash
aws rds describe-events --source-type db-instance --source-identifier orders --duration 1440
```

## 2. Event subscriptions (SNS)
```bash
aws rds create-event-subscription --subscription-name prod-db-alerts \
  --sns-topic-arn arn:aws:sns:eu-west-1:111122223333:db-alerts --source-type db-instance \
  --event-categories failover failure "low storage" maintenance availability \
  --source-ids orders billing --enabled
```
Omit `--source-ids` to be notified about the events for that source type for all your RDS
resources. For an encrypted SNS topic, the KMS key policy must give RDS access (see the event
subscription page); SNS subscribers receive every message unless they set a filter policy.

## 3. EventBridge (richer routing)
```json
{"source": ["aws.rds"], "detail-type": ["RDS DB Instance Event", "RDS DB Cluster Event"],
 "detail": {"EventCategories": ["failover", "failure", "low storage"]}}
```
Event IDs appear in `detail.EventID` (for example `RDS-EVENT-0049` Multi-AZ instance failover completed,
`RDS-EVENT-0004` DB instance shutdown, `RDS-EVENT-0007` allocated storage exhausted (category low storage),
`RDS-EVENT-0089` free storage capacity consumed (low storage), `RDS-EVENT-0221` storage-full threshold reached);
look up the IDs for your engine on the event messages page and filter on `detail.EventID` for precise alerts. Route to chat/on-call and
to a Lambda that annotates dashboards.

## 4. Exporting engine logs to CloudWatch Logs
```bash
aws rds modify-db-instance --db-instance-identifier orders \
  --cloudwatch-logs-export-configuration '{"EnableLogTypes":["postgresql","upgrade"]}' --apply-immediately
```
Log types per engine:
Valid values per the RDS API (`CloudwatchLogsExportConfiguration`):
- RDS for PostgreSQL: `postgresql`, `upgrade`, `iam-db-auth-error` (tune `log_min_duration_statement`,
  `log_statement`, `log_connections` in the parameter group).
- RDS for MySQL and MariaDB: `audit`, `error`, `general`, `slowquery`, `iam-db-auth-error`. The error log is on by
  default; audit needs a custom option group with `MARIADB_AUDIT_PLUGIN`; general needs `general_log = 1`; slow
  query needs `slow_query_log = 1`; all need `log_output = FILE` in a custom parameter group.
- RDS for SQL Server: `agent`, `error`; RDS for Oracle: `alert`, `audit`, `listener`, `trace`, `oemagent`.
- Aurora MySQL: `audit`, `error`, `general`, `instance`, `slowquery`, `iam-db-auth-error`; Aurora PostgreSQL:
  `instance`, `postgresql`, `iam-db-auth-error`.
Logs land in `/aws/rds/instance/<id>/<type>` (or `/aws/rds/cluster/...`). CloudWatch Logs keeps data
indefinitely unless you set a retention period, so set one. Export needs the RDS service-linked role.

## 5. Using the logs
Logs Insights for slow queries (MySQL; adjust the parse pattern to the log format you see):
```
fields @timestamp, @message
| parse @message "Query_time: * Lock_time: * Rows_sent: * Rows_examined: *" as qt, lt, rs, re
| filter qt > 2 | sort qt desc | limit 20
```
Metric filters on `FATAL`/`ERROR` lines with alarms. For query-level performance use
Performance Insights / Database Insights rather than log mining.

## Gotchas
- `general` log on busy MySQL is huge and slows the DB; enable briefly.
- Log export costs CloudWatch ingestion; tune verbosity first.
- Without export, logs are rotated on the instance and kept briefly (download via
  `download-db-log-file-portion`).

## Verify
- [ ] Event subscription or EventBridge rule exists for failover/failure/low storage; test with a reboot-with-failover in staging.
- [ ] Log groups receive logs; retention set; slow query threshold documented.

## Checked
Date: 2026-10-27. Sources: RDS User Guide USER_Events.Messages (event IDs and categories), rds-cloud-watch-events
(EventBridge `source`, `detail-type`, `EventID`), USER_LogAccess.Procedural.UploadtoCloudWatch and the MySQL, MariaDB,
PostgreSQL pages; botocore `rds` model (`EnableLogTypes` values per engine). Corrected the log type lists (added
`iam-db-auth-error`, `oemagent`, Aurora lists per engine) and reworded the "low storage" event IDs.
Method: documentation only; no commands were run.
