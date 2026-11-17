---
id: computing-software.data-engineering.streaming-architecture.event-design-and-envelopes
name: event-design-and-envelopes
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, event-design, event-envelope, cloudevents, event-notification, event-carried-state-transfer, domain-events, partition-keys, schema-registry]
level: advanced
status: draft
description: "Design streaming events: notification vs state-carrying vs delta events, envelope metadata (CloudEvents), keys and ordering, naming and versioning, and size and PII limits."
sources:
  - https://martinfowler.com/articles/201701-event-driven.html
  - https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
  - https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/index.html
  - https://microservices.io/patterns/data/transactional-outbox.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Event design and envelopes

**Goal:** events that consumers can process correctly without calling back to the producer, that evolve without breaking anyone, and that can be routed, traced and deduplicated.

## 1. Choose the event style
| Style | Payload | Pros | Cons |
|---|---|---|---|
| Event notification | "order 123 changed" + id | tiny, decoupled | consumers call back → load + race conditions |
| Event-carried state transfer (state/snapshot) | full current entity state | consumers self-sufficient, compacted topics work, replay rebuilds state | larger messages, changes harder to see |
| Delta / domain event | what happened (`OrderShipped` with shipment details) | expresses business intent, good for workflows | consumers must apply deltas in order; rebuilding state needs full history |
Common combination: domain events for business processes + a compacted **state topic** per entity for data integration and analytics.

## 2. Envelope
Separate metadata from payload. CloudEvents is a ready-made standard:
```json
{
  "specversion": "1.0",
  "id": "5f0c9a2e-4b1d-4e0f-9a41-2d9d3c1b7e10",
  "source": "/orders-service",
  "type": "com.acme.order.shipped.v1",
  "time": "2026-10-16T09:12:44.123Z",
  "subject": "order/123",
  "datacontenttype": "application/json",
  "dataschema": "https://schemas.acme.com/order-shipped/1",
  "traceparent": "00-...",
  "data": {"order_id": 123, "carrier": "DHL", "shipped_at": "2026-10-16T09:12:40Z"}
}
```
In Kafka, put envelope fields in **headers** (CloudEvents Kafka binding, binary mode) or in the value (structured mode); be consistent per topic.
Must-haves: unique `id` (dedup), `type` with version, event `time` (when it happened), `source`, correlation/trace id.

## 3. Keys and ordering
- Message key = the entity whose events must stay ordered (`order_id`). Kafka orders per partition only; same key → same partition.
- Don't key by something with heavy skew (a tenant with 50% of traffic) without a plan.
- Include a per-entity sequence/version number so consumers can detect gaps or reordering.

## 4. Naming and versioning
- Topic per event type or per entity stream: `<domain>.<entity>.<event>` e.g. `sales.order.shipped`, plus `sales.order.state` for snapshots.
- Event types are past-tense facts (`OrderShipped`), not commands (`ShipOrder`).
- Schemas in a registry; backward-compatible changes only (add optional fields with defaults). Breaking change = new type/version (`...shipped.v2`) running in parallel until consumers migrate.

## 5. Content rules
- Self-contained: include the IDs and the attributes consumers need for the common case.
- Keep messages small (KBs; Kafka default max ~1 MB). Large blobs → store in object storage, send a reference ("claim check").
- PII: include only what consumers are authorised for; tokenise or reference sensitive fields; remember events are hard to erase once replicated (crypto-shredding per subject key if erasure is required).
- Publish reliably from services with the **transactional outbox** pattern, not dual writes.

## Verify
- [ ] Every event type has a registered schema, owner, key, and version.
- [ ] Consumers can dedupe on `id` and order by entity sequence.
- [ ] A schema change PR runs the compatibility check.
