---
id: computing-software.database-administration.pgbouncer.query-and-transaction-timeouts
name: query-and-transaction-timeouts
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, query-timeout, idle-transaction-timeout, transaction-timeout, timeouts]
level: advanced
status: docs-checked
description: "query_timeout, idle_transaction_timeout and transaction_timeout, their per-user overrides and the advice to pair with server statement_timeout."
sources:
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: cut off long queries and transactions at the pooler.

- `query_timeout` (default 0.0, disabled): queries running longer are canceled. The docs say to use it only with a slightly smaller server-side statement_timeout, so it applies only to network problems.
- `idle_transaction_timeout` (default 0.0, disabled): a client in the "idle in transaction" state longer than this is disconnected.
- `transaction_timeout` (default 0.0, disabled): a client in the "in transaction" state longer than this is disconnected.

All are in seconds. Each can be overridden per user in [users], where the user value takes priority over the server-level setting:

```
[pgbouncer]
query_timeout = 0
idle_transaction_timeout = 600

[users]
batchuser = query_timeout=3600 idle_transaction_timeout=0
```

These live under the "Dangerous timeouts" heading: setting them can cause unexpected errors. Per-user query_timeout is described as the maximum number of seconds a user query can run for.

Compare with the wait-related timeouts in the client-timeouts skill: query_wait_timeout limits time spent queued, whereas query_timeout limits execution.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: a closing sentence on server_idle_timeout that was off-topic.

Method: documentation only; no commands were run.
