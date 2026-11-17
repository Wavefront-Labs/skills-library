---
id: computing-software.data-engineering.kestra.purge-tasks
name: purge-tasks
category: computing-software
field: data-engineering
product: kestra
tags: [purge, purgeexecutions, purgelogs, purgestorage, retention, dry-run]
level: practitioner
status: docs-checked
description: "Control Kestra data growth with PurgeExecutions, PurgeLogs, PurgeKV, PurgeStorage and PurgeFiles, including level-based log retention and dry runs."
sources:
  - https://kestra.io/docs/administrator-guide/purge
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tasks:

- `PurgeExecutions`: deletes execution records from the database and their associated storage files.
- `PurgeLogs`: removes execution logs and non-execution logs (for example trigger logs) in bulk. If you have configured an external log data store that does not support purge, `PurgeLogs` is a no-op for logs; manage retention directly in that backend.
- `PurgeKV`: deletes expired keys globally for a specific namespace.
- `PurgeStorage`: removes orphaned execution files from internal storage, meaning files that exist on disk but whose execution records are no longer in the database.
- `PurgeFiles` (`io.kestra.plugin.core.namespace.PurgeFiles`): purges old versions of namespace files.
- Enterprise Edition also includes `PurgeAuditLogs`.

`PurgeExecutions`, `PurgeLogs` and `PurgeKV` replace the legacy `io.kestra.plugin.core.storage.Purge` task. `PurgeStorage` is a newer addition for orphaned files the other tasks cannot reach.

```yaml
tasks:
  - id: purge_executions
    type: io.kestra.plugin.core.execution.PurgeExecutions
    endDate: "{{ now() | dateAdd(-1, 'MONTHS') }}"
    purgeLog: false

  - id: purge_debug_logs
    type: io.kestra.plugin.core.log.PurgeLogs
    endDate: "{{ now() | dateAdd(-1, 'WEEKS') }}"
    logLevels:
      - DEBUG
```

The page's example flow chains several `PurgeLogs` tasks with shorter windows for verbose levels (all logs older than 1 month, DEBUG older than 1 week, TRACE older than 1 day) on an `@daily` schedule. Error stacktraces are often logged at DEBUG level, so the DEBUG purge also removes them.

Key properties:

- `PurgeLogs`: `purgeExecutionLogs` and `purgeNonExecutionLogs` both default to `true`; set one to `false` to exclude that type. `batchSize` splits deletion into batches; by default all matching rows are deleted in a single transaction. Outputs include `executionLogsCount` and `nonExecutionLogsCount` alongside `count`.
- `PurgeStorage`: `dryRun` defaults to `true`. `namespace` matching is recursive (`company` also reaches `company.team`); omitting `namespace` purges across every namespace under the tenant (requires tenant-admin access). `flowId` is supported but requires `namespace`. Outputs: `scannedCount`, `purgedCount`, `deletedFilesCount` (0 when `dryRun: true`).
- `PurgeKV`: `expiredOnly`, `namespaces`, `includeChildNamespaces`.
- `PurgeFiles`: `namespaces`, `includeChildNamespaces`, `filePattern`, and `behavior` (for example `type: version` with `before`) to keep or delete versions.

Expired key-value pairs can also be deleted automatically via `kestra.kv.purge-expired` (`enabled`, `initial-delay`, `fixed-delay`, `batch-size`) instead of a scheduled flow; see the page for its defaults.

Caveats:

- Purge tasks permanently delete data; test in non-production environments first. Always run `PurgeStorage` with `dryRun: true` and review the counts before switching to `false`.
- UI deletion is a soft deletion (data is hidden but retained); purge tasks perform hard deletion.
- Purge tasks do not affect Kestra's internal queues; queue retention is managed separately in the Runtime and Storage configuration (JDBC) or the Enterprise and Advanced configuration (Kafka).
- With isolated remote worker groups using dedicated storage, run a worker-group-scoped `PurgeExecutions` with `purgeExecution: false` and `purgeStorage: true` before the primary purge to prevent orphaned files. `PurgeStorage` with a `workerSelector` cleans up orphans that already exist.
- In Enterprise Edition, sub-namespaces with their own dedicated storage are not reached by recursive namespace scoping; target them explicitly.

## Checked

2026-11-04. Confirmed against "Delete old executions, logs, and files to reclaim storage" (administrator-guide/purge): task list and descriptions, legacy task replacement, example flow, property defaults, outputs, namespace scoping, isolated worker group strategy, soft versus hard deletion, queues note. Fixed: the skill said all four tasks replace the legacy `Purge` task, but the page says only PurgeExecutions, PurgeLogs and PurgeKV do. Removed: "UI deletion" and other wording not stated as written; `PurgeFiles` and the KV auto-purge setting added from the page.
Method: documentation only; no commands were run.
