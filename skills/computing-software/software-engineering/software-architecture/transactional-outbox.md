---
id: computing-software.software-engineering.software-architecture.transactional-outbox
name: transactional-outbox
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, distributed-data, transactional-outbox, outbox-pattern, dual-write, debezium, change-data-capture]
level: practitioner
status: verified
description: "Avoid dual-write bugs by writing messages to an outbox table in the same DB transaction and relaying them via polling or CDC (Debezium); ordering, cleanup and dedupe."
sources:
  - https://microservices.io/patterns/data/transactional-outbox.html
  - https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html
  - https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-outbox-cosmos
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transactional outbox

## The dual-write problem
```python
db.save(order); db.commit()
broker.publish(OrderPlaced(order.id))   # crash here -> event lost; publish first -> DB may roll back
```
You cannot atomically commit to a database and a message broker without distributed transactions.

## Pattern
1. In the **same local transaction** as the business change, insert the message into an `outbox` table.
2. A separate **relay** reads unpublished outbox rows and publishes them to the broker, then marks them sent (or deletes them).
```sql
CREATE TABLE outbox (
  id            uuid PRIMARY KEY,
  aggregate_type text NOT NULL,
  aggregate_id  text NOT NULL,
  type          text NOT NULL,
  payload       jsonb NOT NULL,
  created_at    timestamptz NOT NULL DEFAULT now(),
  published_at  timestamptz
);
CREATE INDEX outbox_unpublished ON outbox (created_at) WHERE published_at IS NULL;
```

## Relay options
- **Polling publisher:** `SELECT ... WHERE published_at IS NULL ORDER BY created_at LIMIT 100 FOR UPDATE SKIP LOCKED`, publish, update. Simple; adds DB load and latency (poll interval). `SKIP LOCKED` (a `FOR UPDATE` option in PostgreSQL's SELECT) lets several relay instances run without double-processing the same rows.
- **Transaction log tailing (CDC):** Debezium reads the WAL/binlog and its Outbox Event Router SMT routes rows to topics by the aggregate-type column, keyed by the aggregate-id column. The SMT's default column names are `id`, `aggregatetype`, `aggregateid`, `type` and `payload` (default `route.by.field=aggregatetype`, topic `outbox.event.${routedByValue}`); the table above uses `aggregate_type`/`aggregate_id`, so set `route.by.field` and `table.field.event.key` (and the other `table.field.event.*` options) to match, or rename the columns. Low latency, no polling; needs Kafka Connect and logical replication setup. Debezium's outbox blog post inserts and removes the row in the same transaction when using CDC, because the connector reads the append-only log, not the table.
- (The DDL, partial index and polling query were run on PostgreSQL via PGlite.) Libraries: Spring Modulith event publication registry, MassTransit/NServiceBus outbox, Eventuate Tram, Wolverine.

## Guarantees and gotchas
- Delivery is **at least once**: the relay can crash after publishing but before marking. Consumers must dedupe (store processed message ids - the "inbox" pattern - or make handlers idempotent).
- Ordering: publish in `created_at`/sequence order per aggregate; use the aggregate id as the partition key. Parallel relays break global order - only per-key order is realistic.
- Cleanup: delete or archive published rows (partition by day and drop old partitions) or the table bloats.
- Monitor relay lag (oldest unpublished row age) and alert.

## Verify
- [ ] Kill the relay mid-batch: after restart all events arrive (some duplicated, none lost).
- [ ] Roll back a business transaction: no outbox row, no event.
- [ ] Alert fires when oldest unpublished row exceeds threshold.
