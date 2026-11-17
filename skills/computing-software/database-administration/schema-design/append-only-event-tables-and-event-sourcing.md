---
id: computing-software.database-administration.schema-design.append-only-event-tables-and-event-sourcing
name: append-only-event-tables-and-event-sourcing
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, event-sourcing, append-only, event-store, projections, schema-patterns]
level: practitioner
status: verified
description: "Design append-only event tables and event-sourced stores: event schema, per-stream ordering with optimistic concurrency, projections, snapshots, versioning and retention."
sources:
  - https://martinfowler.com/eaaDev/EventSourcing.html
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
  - https://www.postgresql.org/docs/current/ddl-constraints.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Append-only event tables and event sourcing

## Append-only event table (audit/analytics)
```sql
CREATE TABLE events (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  stream_id uuid NOT NULL,              -- aggregate id (order, account)
  stream_version int NOT NULL,          -- 1,2,3... per stream
  event_type text NOT NULL,             -- 'OrderPlaced'
  schema_version smallint NOT NULL DEFAULT 1,
  payload jsonb NOT NULL,
  metadata jsonb NOT NULL DEFAULT '{}', -- causation/correlation ids, actor
  occurred_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (stream_id, stream_version));
REVOKE UPDATE, DELETE ON events FROM app_role;        -- enforce append-only (app_role must exist; the table owner is not restricted)
```

## Optimistic concurrency per stream
The writer loads stream version N, decides, and appends N+1:
```sql
INSERT INTO events (stream_id, stream_version, event_type, payload) VALUES ($1, $2 + 1, 'OrderPaid', $3);
```
A concurrent writer appending the same version hits the unique constraint → reload and retry. No row locks held during business logic.

## Event sourcing
State = fold of events; current-state tables are **projections** rebuilt from events.
- Projections updated synchronously in the same transaction (simple, consistent) or asynchronously by a consumer reading `id > last_processed` (scales; eventual consistency). Beware: sequence values are taken when the row is inserted, not when it commits (the PostgreSQL sequence docs note that `nextval` values are not reclaimed on abort and cannot give gapless numbering), so a reader using `id > n` can skip late-committing rows; use a transaction-ordered position (logical decoding/outbox, or poll with a safety lag).
- **Snapshots** every N events per stream speed up loading long streams.
- **Versioning**: events are immutable; evolve with new event types or `schema_version` + upcasters in code. Never rewrite history casually.

## Retention and deletion
Append-only conflicts with erasure duties: keep personal data out of payloads (references only) or encrypt per subject (crypto-shredding). Partition by time and archive old partitions to cheaper storage.

## When not to event-source
CRUD domains without audit/temporal requirements gain mostly complexity. Often an append-only audit table next to normal tables (or CDC) is enough.

## Performance
- Index `(stream_id, stream_version)` (the unique constraint) for loading streams; BRIN on `occurred_at` for time scans.
- Large payloads: keep jsonb compact; consider storing big blobs elsewhere.

## Verify
Rebuild a projection from scratch in staging and compare with the live projection (row counts and checksums); concurrent append test produces unique-violation retries, never duplicates.
