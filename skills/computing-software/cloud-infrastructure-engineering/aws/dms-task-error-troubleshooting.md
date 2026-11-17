---
id: computing-software.cloud-infrastructure-engineering.aws.dms-task-error-troubleshooting
name: dms-task-error-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dms, dms-troubleshooting, task-logs, table-errors, cdc-latency, replication-task]
level: advanced
status: docs-checked
description: "Troubleshoot AWS DMS tasks: task and table state, logging components and severity, common source/target errors, tables in error, CDC latency, and resuming safely."
sources: ["https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Troubleshooting.html", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Monitoring.html", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TaskSettings.Logging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DMS task troubleshooting

## 1. Where to look
```bash
aws dms describe-replication-tasks --filters Name=replication-task-arn,Values=<arn> \
  --query 'ReplicationTasks[].{s:Status,stop:StopReason,err:LastFailureMessage,pct:ReplicationTaskStats.FullLoadProgressPercent}'
aws dms describe-table-statistics --replication-task-arn <arn> \
  --query 'TableStatistics[?TableState!=`Table completed`].{t:TableName,state:TableState,err:ValidationState}'
```
CloudWatch Logs group `dms-tasks-<replication-instance>` (enable `Logging.EnableLogging`
in task settings). Raise detail per component temporarily:
```json
"Logging": {"EnableLogging": true, "LogComponents": [
  {"Id": "SOURCE_CAPTURE", "Severity": "LOGGER_SEVERITY_DEBUG"},
  {"Id": "TARGET_APPLY", "Severity": "LOGGER_SEVERITY_DEBUG"},
  {"Id": "SOURCE_UNLOAD", "Severity": "LOGGER_SEVERITY_DEFAULT"},
  {"Id": "TARGET_LOAD", "Severity": "LOGGER_SEVERITY_DEFAULT"}]}
```
Debug severity writes much more to the log; revert after the investigation.

## 2. Common errors
| Error / symptom | Cause | Fix |
|---|---|---|
| Endpoint test fails | Security group, route or TLS settings | Allow the replication instance to reach the source/target ports, then re-test the endpoint connection |
| MySQL binary logging or retention errors | Binary log retention too short on RDS/Aurora | `call mysql.rds_set_configuration('binlog retention hours', 24);` (the troubleshooting page's example) |
| PostgreSQL `ReplicationSlotDiskUsage` grows and `restart_lsn` stops advancing | Long transactions with logical replication enabled: changes over 4 MB per transaction spill to disk | Avoid long transactions; split them into smaller ones |
| Oracle supplemental logging missing | DMS leaves supplemental logging off by default | Set the endpoint extra connection attribute `addSupplementalLogging=Y`, or enable it on the database |
| `Table Error` in table statistics | A WHERE clause does not reference a primary key column and supplemental logging is not on for all columns | Turn on supplemental logging for all columns of the table |
| Duplicate records on a target table without a primary key | Reload or CDC overlap into a table with no key | Follow the "Duplicate records" section: `TargetTablePrepMode` `DO_NOTHING` (and validation off) as that page describes |
| Task slows or fails with resource pressure | Replication instance short of CPU, memory, swap or IOPS | Check those instance metrics; use a larger instance or fewer parallel tasks |

## 3. CDC latency
Compare `CDCLatencySource` (reading the source) with `CDCLatencyTarget` (applying to the
target). If both are high, investigate source latency first. A transaction that has begun
but not committed keeps `CDCLatencySource` growing until it commits.
`CDCIncomingChanges` is the number of change events waiting to be applied to the target.
The SORTER caches backlog to disk or a swap file when `SOURCE_CAPTURE` outruns
`TARGET_APPLY`, a common cause of running out of replication-instance storage.

## 4. Recovering
- Resume: `start-replication-task --start-replication-task-type resume-processing`.
- Reload one table: `reload-tables --table-to-reload SchemaName=sales,TableName=orders`.
- Restart CDC from a position: `start-replication-task --cdc-start-position <position>`;
  the troubleshooting page describes using logged position information as the starting
  point for CDC-only replication.

## Verify
- [ ] All tables `Table completed` (full load).
- [ ] CDC latency under the cutover threshold for a sustained period.
- [ ] Debug logging reverted to default severity after investigation.

## Checked

2026-10-28. Confirmed against AWS documentation: log group name, logging components and severities, supplemental logging and Table Error causes, binlog retention call, CDCLatency metrics, TargetTablePrepMode; CLI flags via the botocore model.
Removed: unsupported error rows (SQL Server MS-CDC, rds.logical_replication, LOB and parallel-load setting names), serverless DCU line, Validated state.
Method: documentation only; no commands were run.
