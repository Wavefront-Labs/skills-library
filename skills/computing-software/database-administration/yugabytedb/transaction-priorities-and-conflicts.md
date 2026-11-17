---
id: computing-software.database-administration.yugabytedb.transaction-priorities-and-conflicts
name: transaction-priorities-and-conflicts
category: computing-software
field: database-administration
product: yugabytedb
tags: [transactions, transaction-priority, conflict-resolution, select-for-update, yb-transaction-priority-lower-bound]
level: advanced
status: docs-checked
description: "Tune YSQL transaction priority bounds to decide which transaction wins a conflict, and what the high-priority bucket for SELECT FOR UPDATE means."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/transactions/transaction-priorities.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Transaction priorities and conflicts

This applies to YSQL with the Fail-on-Conflict concurrency control policy: transactions are assigned priorities that help decide which one is aborted on conflict. Priorities are chosen randomly from the applicable bucket and can be steered per session.

Session parameters (real values in [0, 1]; the same bounds apply to both buckets):
- `yb_transaction_priority_lower_bound`
- `yb_transaction_priority_upper_bound`

The page's example sets both bounds to 0.4 and 0.6 and, separately, to 1 to get the highest priority. `yb_get_current_transaction_priority()` returns a priority (9 decimal places) with its bucket, Normal or High; for the highest possible priority it returns `Highest priority transaction`. The value is 0.000000000 until a real transaction starts, which for a read-only transaction does not happen until a write occurs. All single-shard transactions have priority 1 in the normal bucket.

There are two buckets. A transaction whose first statement takes an explicit row lock with SELECT FOR UPDATE, FOR SHARE or FOR NO KEY UPDATE gets its priority from the high-priority bucket; all other transactions use the normal bucket. Any high-bucket priority can abort any normal-bucket priority: for example a high-bucket 0.1 can abort a normal-bucket 0.9.

Guidance:
- Set the bounds before beginning the transaction, as in the page's example.
- Internally the buckets map to a uint64 space: normal is 0 to uint32_t_max-1 and high is uint32_t_max to uint64_t_max, with the [0, 1] range mapped proportionally for each.
- Priorities are random draws within the applicable bucket and your bounds, so narrowing the bounds narrows the range of the draw.

## Checked

2026-11-04. Confirmed against the Transaction priorities page (Fail-on-Conflict scope, two buckets, FOR UPDATE, FOR SHARE and FOR NO KEY UPDATE trigger, high bucket beats normal bucket, the two session parameters and range, single-shard priority 1, yb_get_current_transaction_priority output, 0 until a real transaction starts, internal uint64 mapping). Corrected: the page does not say the lower priority always loses (priority only helps decide), and a high-bucket transaction beats any normal-bucket one regardless of the numbers. Removed: the retry-logic guidance and the advice on narrow short-lived high-priority sessions, which the page does not give.

Method: documentation only; no commands were run.
