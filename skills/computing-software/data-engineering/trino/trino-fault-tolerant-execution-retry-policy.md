---
id: computing-software.data-engineering.trino.trino-fault-tolerant-execution-retry-policy
name: trino-fault-tolerant-execution-retry-policy
category: computing-software
field: data-engineering
product: trino
tags: [fault-tolerant-execution, retry-policy, query-retry, task-retry, deduplication-buffer]
level: advanced
status: docs-checked
description: "Choose and enable the Trino QUERY or TASK retry policy, connector support, buffer limits, retry delays and per-task attempt limits."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/fault-tolerant-execution.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino fault tolerant execution retry policy

Fault-tolerant execution (FTE) lets Trino retry whole queries or individual tasks after worker failures, spooling intermediate exchange data so another worker can reuse it. It does not retry user errors such as unparseable SQL. It is off by default: set `retry-policy` to `QUERY` or `TASK`.

```properties
retry-policy=QUERY
```

Connectors that do not support retries fail with "This connector does not support query retries". Documented support: BigQuery, Delta Lake, Hive, Iceberg, MariaDB, MongoDB, MySQL, Oracle, PostgreSQL, Redshift, SQL Server.

Policies:
- `QUERY`: retry the whole query; recommended when the workload is many small queries. By default FTE does not cover result sets over 32MB (`exchange.deduplication-buffer-size`, default `32MB`, held in coordinator memory); an external exchange manager is strongly recommended for larger results.
- `TASK`: retry tasks individually; requires an exchange manager; recommended for large batch queries. It may add latency to high-volume short queries, so use a dedicated cluster. With `TASK`, set `task.low-memory-killer.policy` to `total-reservation-on-blocked-nodes` if you have manually configured the affected properties.

Other properties: `retry-policy.allowed` (default `NONE`, `QUERY`, `TASK`), `fault-tolerant-execution.exchange-encryption-enabled` (default `true`; data is encrypted with a random per-query key discarded afterward).

Retry limits: `query-retry-attempts` (4, QUERY only), `task-retry-attempts-per-task` (4, TASK only), `retry-initial-delay` (`10s`), `retry-max-delay` (`1m`), `retry-delay-scale-factor` (`2.0`). The session property `retry_policy` is meant mainly for deactivating with `NONE`, since switching modes is untested.

## Checked

2026-11-04. Read against the Trino docs page `admin/fault-tolerant-execution.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
