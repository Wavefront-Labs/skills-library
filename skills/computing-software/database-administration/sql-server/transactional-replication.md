---
id: computing-software.database-administration.sql-server.transactional-replication
name: transactional-replication
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, transactional-replication, distributor, publication, log-reader-agent, distribution-agent, tracer-tokens, replication-monitor]
level: advanced
status: docs-checked
description: "Set up and operate SQL Server transactional replication: distributor, publications and subscriptions, latency monitoring with tracer tokens, and fixing common agent errors."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/replication/transactional/transactional-replication
  - https://learn.microsoft.com/en-us/sql/relational-databases/replication/monitor/measure-latency-and-validate-connections-for-transactional-replication
  - https://learn.microsoft.com/en-us/sql/relational-databases/replication/troubleshoot-tran-repl-errors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transactional replication

Copies published data from a publisher to subscribers: an initial snapshot, then incremental changes.

## Architecture
Publisher -> **Log Reader Agent** reads the log, writes commands to the `distribution` database
-> **Distribution Agent** applies them at subscribers (runs at the Distributor for push subscriptions and at the Subscriber for pull subscriptions). The Snapshot Agent prepares the initial snapshot files.

## Set up
Use the New Publication and New Subscription wizards in SSMS, or the replication stored procedures and RMO (see the Learn replication documentation for the procedure names and parameters).

## Monitor latency
```sql
-- publisher, publication database
EXEC sys.sp_posttracertoken @publication = N'appdb_pub';
EXEC sys.sp_helptracertokenhistory @publication = N'appdb_pub', @tracer_id = <id>;
```
A tracer token is written to the publication database's log and followed through the Log Reader Agent, distribution database and Distribution Agent, so it measures each hop and validates the connections. Replication Monitor and Transact-SQL can both post and read tokens.

## Troubleshooting
See the Troubleshoot transactional replication errors page for specific error numbers and fixes. If an agent is not available on the server you are investigating, check the other server (agents run on the publisher or subscriber depending on push or pull).

## Verify
Tracer token end-to-end latency within target and the agents are running.

## Checked

2026-10-28. Confirmed against Microsoft Learn (transactional replication, measure latency and validate connections, troubleshoot transactional replication errors): Snapshot Agent, Log Reader Agent and Distribution Agent roles, Distribution Agent runs at the Distributor for push and at the Subscriber for pull, tracer tokens with sp_posttracertoken and sp_helptracertokenhistory measuring latency and validating connections, agents can be on either server. Removed unconfirmed: the T-SQL setup outline and parameters, primary key rule, backup initialisation, writable-subscriber and not-HA statements, log_reuse_wait_desc, pending-commands procedure, error number table, DDL and truncate and AG gotchas.

Method: documentation only; no commands were run.
