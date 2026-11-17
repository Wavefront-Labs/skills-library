---
id: computing-software.messaging-and-integration.debezium.sqlserver-capture-job-agent-tuning
name: sqlserver-capture-job-agent-tuning
category: computing-software
field: messaging-and-integration
product: debezium
tags: [sql-server, cdc, capture-job, latency]
level: advanced
status: docs-checked
description: "Tune pollinginterval, maxtrans and maxscans with sys.sp_cdc_change_job to balance SQL Server CPU load and CDC latency."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/sqlserver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The SQL Server capture job reads the transaction log and writes change tables. Each scan adds CPU load on the host, but scanning more often lowers latency, so tuning is a trade-off. The parameters live in `msdb.dbo.cdc_jobs` and are changed with `sys.sp_cdc_change_job`.

Most relevant parameters:

- `pollinginterval`: seconds between log scan cycles. Default `5`. Higher means less load and more latency; `0` means no wait.
- `maxtrans`: maximum transactions per scan cycle. Default `500`. After that many, the job pauses for `pollinginterval`. Lower means less load and more latency.
- `maxscans`: limit on scan cycles for capturing the full log contents. Default `10`. If `continuous` is `1`, the job pauses for `pollinginterval` before resuming. Lower means less load and more latency.

Run `sys.sp_cdc_change_job` with new values for the parameter you want to change; the Debezium docs defer the exact procedure to the SQL Server documentation.

Monitor database metrics to know when the server can no longer support the capture agent's activity. There is always a small gap between commit and the change appearing in the change table, and that gap is the floor on Debezium latency.

Gotcha: speeding up the capture job cannot reduce latency below what your hardware allows, and can hurt transactions at peak.

Debezium-side counterpart: `max.iteration.transactions` (default `500`) bounds transactions per streaming iteration to reduce memory; `0` uses the current maximum LSN.

Check: compare end-to-end lag before and after each single change.

## Checked

2026-11-08. Confirmed against the Debezium page connectors/sqlserver (read in part: the capture job agent sections and the max.iteration.transactions property): pollinginterval default 5, maxtrans default 500, maxscans default 10, msdb.dbo.cdc_jobs, sys.sp_cdc_change_job and the load versus latency trade-off. Nothing removed.

Method: documentation only; no commands were run.
