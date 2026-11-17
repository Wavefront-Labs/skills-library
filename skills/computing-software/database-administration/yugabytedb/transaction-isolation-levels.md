---
id: computing-software.database-administration.yugabytedb.transaction-isolation-levels
name: transaction-isolation-levels
category: computing-software
field: database-administration
product: yugabytedb
tags: [transactions, isolation-levels, serializable, snapshot-isolation, read-committed, ysql, ycql]
level: practitioner
status: docs-checked
description: "Which isolation levels YSQL and YCQL support, how they map to PostgreSQL names, and the cluster flag that controls Read Committed."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/transactions/isolation-levels.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/yb-tserver.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Transaction isolation levels

YSQL supports three levels:
- **Serializable**
- **Snapshot**, which maps to the SQL Repeatable Read level
- **Read Committed**, which sees all data committed before each statement and internally handles read restart and conflict errors, so the client does not normally see them

As in PostgreSQL you can specify Read Uncommitted for YSQL, but it behaves the same as Read Committed. YCQL supports only Snapshot isolation, using `BEGIN TRANSACTION`.

Read Committed is supported only if the yb-tserver flag `--yb_enable_read_committed_isolation` is true (the flag needs a restart to change). The default is false, in which case Read Committed falls back to the stricter Snapshot isolation, and so do YSQL Read Committed and Read Uncommitted; the effective YSQL default is then Snapshot. For new universes on v2025.2 or later deployed with yugabyted, YugabyteDB Anywhere or YugabyteDB Aeon it is true by default.

Operational notes:
- DocDB uses three lock types: serializable read, serializable write and snapshot isolation write (also taken by Read Committed transactions). Serializable read locks block writers but not other readers; serializable write locks block readers but not other serializable writers, so concurrent blind writes are allowed under Serializable; snapshot isolation write locks block all other readers and writers.
- Locks can be taken at several granularities (tablet, key prefix, row, column; YCQL goes below column level), using strong and weak locks so conflicts between granularities are detected cheaply.
- Conflict handling under Fail-on-Conflict uses transaction priorities; see the transaction priorities skill.

## Checked

2026-11-04. Confirmed against the Isolation levels page (three levels and their mapping, YCQL Snapshot only, Read Uncommitted behaviour, the flag and its v2025.2 default, fallback to Snapshot, lock types and granularities) and the yb-tserver reference (yb_enable_read_committed_isolation default false, restart needed, fallback text). Removed: the claim that enabling the flag on a cluster changes existing sessions and that higher isolation means more conflicts to retry, and the IntentsDB storage note, none of which appear on the cited pages.

Method: documentation only; no commands were run.
