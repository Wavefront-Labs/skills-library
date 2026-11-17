---
id: computing-software.database-administration.cockroachdb.troubleshoot-lock-contention
name: troubleshoot-lock-contention
category: computing-software
field: database-administration
product: cockroachdb
tags: [lock-contention, insights-page, select-for-update-nowait, historical-reads, randomized-anchor-key]
level: advanced
status: docs-checked
description: "Find and reduce CockroachDB lock contention: use the DB Console Insights page, historical reads, SELECT FOR UPDATE NOWAIT, and kv.transaction.randomized_anchor_key.enabled."
sources:
  - https://www.cockroachlabs.com/docs/stable/troubleshoot-lock-contention
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: identify which transactions wait on which, then remove avoidable conflicts.

Identify: set `application_name` per connection or service (the tutorial uses `SET application_name = 'Transaction 1';`) so contention is attributable. In the DB Console Insights page choose Workload Insights, then Transaction Executions, and widen the time interval (for example Past 6 Hours). Transactions flagged High Contention are listed; open the Latest Transaction Execution ID to see the waiting statement and the blocking transaction.

Remediation options, each trading functionality for less locking:
- Historical reads for tolerant read-only work:
```sql
BEGIN AS OF SYSTEM TIME '-30s';
SELECT * FROM t2 WHERE k=4;
COMMIT;
```
They run below closed timestamps, never wait or block, and are served by the nearest replica; only use them if data about as old as `follower_read_timestamp()` is acceptable.
- Fail fast for hot update keys:
```sql
BEGIN;
SELECT * FROM t2 WHERE k=4 FOR UPDATE NOWAIT;
UPDATE t2 SET v=4034 WHERE k=4;
COMMIT;
```
An early error is better than failing at `COMMIT` when a surge of updates targets the same key.
- Randomize transaction anchor keys: when large batched `UPDATE`/`INSERT` workloads colocate transaction records on one range and its leaseholder becomes a hotspot for intent resolution, try `SET CLUSTER SETTING kv.transaction.randomized_anchor_key.enabled = true;`. It only changes where transaction records live, not which user rows are touched. Enable only after confirming transaction-record hotspotting, compare metrics, and revert with `= false` if it does not help.

Principle from the page: locking conflicts are unavoidable under concurrency; remediate only when they cause a significant response-time or throughput hit.

Verify: after the change, the Insights page no longer flags High Contention for the workload.

## Checked
2026-11-03. Confirmed on the lock contention page: Insights > Workload Insights > Transaction Executions with a longer interval such as Past 6 Hours, `BEGIN AS OF SYSTEM TIME '-30s'`, `FOR UPDATE NOWAIT`, `kv.transaction.randomized_anchor_key.enabled` guidance (enable only after confirming transaction-record hotspots, compare metrics, revert with `= false`). Removed: the p99 latency verify claim.
Method: documentation only; no commands were run.
