---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.idempotent-consumer
name: idempotent-consumer
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, messaging-patterns, idempotent-consumer, inbox-pattern, deduplication, message-id, processed-messages-table]
level: practitioner
status: draft
description: "Implement the idempotent consumer (inbox) pattern: message IDs, processed-message table in the same transaction, natural idempotency, retention and concurrency."
sources: ["https://microservices.io/patterns/communication-style/idempotent-consumer.html", "https://learn.microsoft.com/azure/architecture/reference-architectures/containers/aks-mission-critical/mission-critical-data-platform", "https://docs.aws.amazon.com/powertools/python/latest/utilities/idempotency/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Idempotent consumer (inbox)

## Why
At-least-once delivery means duplicates after retries, consumer crashes and redrives.

## Recipe (inbox table)
```sql
CREATE TABLE inbox (consumer text, message_id text, processed_at timestamptz DEFAULT now(),
  PRIMARY KEY (consumer, message_id));
```
In **one database transaction**:
1. `INSERT INTO inbox(consumer, message_id) VALUES ($1,$2) ON CONFLICT DO NOTHING` - if 0 rows,
   it's a duplicate: ack and skip.
2. Apply the business change.
3. Commit; then ack the message.

## Alternatives
- **Natural idempotency**: upserts keyed by business ID, setting absolute state ("status=SHIPPED")
  instead of relative changes ("balance += 10"), version checks.
- **Idempotency libraries**: AWS Lambda Powertools idempotency (DynamoDB-backed, payload hashing).
- **Downstream APIs**: pass idempotency keys (payments).

## Design points
- Message ID must be stable across redeliveries (producer-assigned, not broker delivery tag).
- Retention: keep inbox rows longer than max redelivery window; purge older rows.
- Concurrency: unique constraint handles two consumers racing.

## Gotchas
- Recording processed ID outside the business transaction (crash between them = loss or duplicate).
- Side effects outside the DB (emails) need their own dedup.

## Verify
- [ ] Replaying the same message N times yields one effect.
