---
id: computing-software.ai-ml-engineering.mastra.setup-storage-backends
name: setup-storage-backends
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, storage, libsql, postgres, composite-storage, domains, persistence, production]
level: practitioner
status: docs-checked
description: "Configure Mastra storage: libSQL locally, PostgreSQL or MongoDB in production, instance vs agent-level storage, MastraCompositeStore domain routing, retention."
sources:
  - https://mastra.ai/docs/storage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: persist Mastra runtime state (memory, workflows, observability, evals, schedules) in the right backend.

## Why and when
Storage keeps state across restarts and shares it across processes. The default in-memory store is fine for tests and short experiments but loses data on exit.

## Domains
Storage is split into domains an adapter implements: `memory`, `workflows` (snapshots for suspend/resume), `observability` (traces, spans, metrics, logs, feedback), `scores`, `datasets`, `experiments`, `backgroundTasks`, `schedules`, `threadState`. Adapter support varies by domain (see the storage overview reference).

Backend choice by data shape: `memory` needs a transactional DB (libSQL, PostgreSQL, MongoDB); `observability` is high-volume telemetry, so use a dedicated store or an OLAP backend such as ClickHouse or DuckDB; `workflows` needs a reliable persistent DB; `schedules` needs an adapter that implements the schedules domain.

## Local
```typescript
export const mastra = new Mastra({
  storage: new LibSQLStore({ id: 'mastra-storage', url: 'file:./mastra.db' }),
})
```
Structures are created on first use. When running `mastra dev` beside your app, use an absolute path (`file:/absolute/path/to/your/project/mastra.db`) because relative `file:` paths resolve per process working directory.

## Production
Use a managed database with backups, monitoring and pooling; PostgreSQL is the suggested default (`new PostgresStore({ id, connectionString: process.env.DATABASE_URL })`; MongoDB uses `MongoDBStore` with `uri` and `dbName`). Keep local file databases out of multi-process production. Configure retention on the adapter or composite store and call `storage.prune()` from a scheduler or maintenance job.

## Instance-level vs agent-level
Instance-level storage (on `Mastra`) is shared by every runtime feature. Agent-level storage is set on a `Memory` instance and overrides only that agent's memory data, giving an isolated boundary or a different backend:

```typescript
memory: new Memory({ storage: new PostgresStore({ id: 'support-agent-storage', connectionString: process.env.SUPPORT_AGENT_DATABASE_URL }) })
```

## Composite storage
`MastraCompositeStore` (from `@mastra/core/storage`) routes domains to different backends:

```typescript
storage: new MastraCompositeStore({
  id: 'composite-storage',
  default: new LibSQLStore({ id: 'default-storage', url: 'file:./mastra.db' }),
  domains: { workflows: new WorkflowsPG({ connectionString: process.env.DATABASE_URL }) },
})
```
`WorkflowsPG` is from `@mastra/pg`. The same mechanism can route `observability` to an analytics backend.

## Checked
Method: 2026-11-08 read the cited Mastra storage page in full (served as markdown) and compared each claim. All claims matched; no content changes.
