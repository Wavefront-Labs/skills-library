---
id: computing-software.database-administration.yugabytedb.read-restart-errors
name: read-restart-errors
category: computing-software
field: database-administration
product: yugabytedb
tags: [read-restart, clock-skew, hybrid-time, deferrable, yb-read-after-commit-visibility, ysql-output-buffer-size]
level: advanced
status: docs-checked
description: "Diagnose and mitigate YSQL read restart errors caused by clock skew, using retries, DEFERRABLE transactions, read visibility settings and the output buffer."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/transactions/read-restart-error.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/transactions/distributed-txns.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Read restart errors

Read restart errors (`ERROR:  Query error: Restart read required`) protect the read-after-commit-visibility guarantee: any read should see all data committed before it was issued, even with clock skew between nodes. They occur in snapshot-based isolation (repeatable read and read committed) when a record's commit timestamp falls in (T1, T1 + max_clock_skew], where T1 is the read time. The read cannot tell whether the record is visible and cannot just advance its read time after returning rows from an older snapshot, so it restarts with the advanced time. They are most likely for a SELECT with a large output while concurrent writes match it.

Mitigations, per the page:
1. **Highly accurate clocks** (NTP keeps the skew low and bounded; the skew is always inside the `max_clock_skew_usec` bound).
2. **Application retry logic** is the best long-term approach, and a retry mechanism is strongly recommended anyway for transaction conflicts and infrastructure failures.

Short-term options:
3. **SERIALIZABLE READ ONLY DEFERRABLE** for background reads avoids read restart errors entirely, at the cost of waiting out `max_clock_skew_usec` (default 500 ms) before reading. Use `SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL SERIALIZABLE READ ONLY DEFERRABLE` or `BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE READ ONLY DEFERRABLE`.
4. `SET yb_read_after_commit_visibility TO deferred` does the same wait for any isolation level and for statements that write; it cannot be set inside a transaction block (set it before BEGIN, per session, or with ALTER ROLE or ALTER DATABASE). Read-write SERIALIZABLE transactions and single-row fast-path writes do not face restarts, so they do not wait. From 2026.1.3, deferred also applies to DDL statements that read user tables (when transactional DDL is disabled, the default).
5. **Larger `ysql_output_buffer_size`** lets the server retry internally while the output has not been flushed to the client: for all statements in a Read Committed block, the first statement in a Repeatable Read block, and standalone statements. The tradeoff is more memory per YSQL backend and a higher out-of-memory risk. It does not help COPY (the application must retry it) or DML in the middle of a REPEATABLE READ transaction (roll back and retry the transaction).
6. `SET yb_read_after_commit_visibility TO relaxed` only affects pure reads and gives up the read-after-commit-visibility guarantee; use it with caution when neither latency nor memory can be traded.

The system configuration page says YugabyteDB shuts down a YB-TServer or YB-Master that detects skew larger than `--max_clock_skew_usec` (500 ms by default), and the metrics page treats `hybrid_clock_skew` above 500 ms as a consistency risk, so monitor it.

## Checked

2026-11-04. Confirmed against the Read restart error page (guarantee, ambiguity window, error text, troubleshooting list, DEFERRABLE, yb_read_after_commit_visibility deferred and relaxed, ysql_output_buffer_size retry scope and limits, 2026.1.3 DDL note), the system configuration page (skew shutdown threshold) and the Raft and distributed system metrics page (hybrid_clock_skew). Reordered the mitigations to the page's order: the skill listed internal retry first and called DEFERRABLE a one-time wait. Removed the reference to a separate clock-sync skill and the chrony-sizing wording.

Method: documentation only; no commands were run.
