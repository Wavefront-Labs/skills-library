---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.idempotency
name: idempotency
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, distributed-systems-design, idempotency, idempotency-keys, exactly-once-processing, deduplication, safe-retries, conditional-writes, at-least-once-delivery]
level: practitioner
status: draft
description: "Make APIs and message handlers idempotent so retries are safe: idempotency keys, response replay, dedupe stores with TTL, conditional writes, natural idempotency."
sources: ["https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/", "https://docs.stripe.com/api/idempotent_requests", "https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Idempotent operations

Every distributed operation will be retried somewhere (client, SDK, queue redelivery). Make the
second execution a no-op that returns the same result.

## APIs: idempotency keys
1. Client sends `Idempotency-Key: <uuid>` on mutating requests (IETF draft header; Stripe model).
2. Server, in one transaction: insert `(key, request_hash, status=in_progress)` with unique
   constraint → perform operation → store response → `status=done`.
3. Repeat with same key: return the stored response (same status code/body). Same key with a
   different request body → `422`/`409`. Concurrent duplicate while in progress → `409` with retry hint.
4. Keep keys for longer than the client's retry window (e.g. 24 h), then expire (TTL).

## Message handlers
- Dedupe on message id/business key in a table with TTL, inside the same transaction as the side effect.
- Or design naturally idempotent operations: `SET status = 'shipped' WHERE id = ? AND status = 'packed'`;
  upserts keyed by business id; conditional writes (DynamoDB `ConditionExpression`, ETag `If-Match`).
- External side effects (emails, payments): pass your idempotency key to the provider (most payment APIs accept one).

## Gotchas
- Dedup outside the transaction: crash between side effect and recording → duplicate.
- Using timestamps or random ids generated server-side per attempt as "keys" — they change on retry.
- FIFO/exactly-once broker features (SQS FIFO dedupe window 5 minutes, Kafka idempotent producer)
  help but don't cover your DB side effects.

## Verify
- [ ] Replay the same request/message 3× in tests: one side effect, identical responses.
