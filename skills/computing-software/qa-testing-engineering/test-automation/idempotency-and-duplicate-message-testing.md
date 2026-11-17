---
id: computing-software.qa-testing-engineering.test-automation.idempotency-and-duplicate-message-testing
name: idempotency-and-duplicate-message-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [idempotency-testing, duplicate-messages, at-least-once-delivery, idempotency-key, reliability-testing]
level: advanced
status: verified
description: "Test idempotency of APIs and consumers: repeated requests with idempotency keys, duplicate and out-of-order messages, concurrent duplicates and replay after crash."
sources:
  - https://docs.stripe.com/api/idempotent_requests
  - https://www.rfc-editor.org/rfc/rfc9110#name-idempotent-methods
  - https://www.istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Idempotency and duplicate message testing

**Goal:** prove that retries and at-least-once delivery never cause double charges, duplicate orders or corrupted state.

## API idempotency
- HTTP semantics (RFC 9110 section 9.2.2: PUT, DELETE and the safe methods such as GET are idempotent); POST is idempotent only if designed so (idempotency keys).
- **Same key, same body twice:** second call returns the original response (same status and body, often a replay header) and no new side effect.
- **Same key, different body:** expect a clear error (Stripe's docs say it compares incoming parameters to the original request and errors if they differ; a concurrent request using the same key gets 409 Conflict).
- **Concurrent duplicates:** fire both requests at the same instant (`curl ... & curl ... & wait` or a k6 batch). Exactly one side effect; a race usually reveals a check-then-insert without a unique constraint (reproduced with two simultaneous curl calls against a local test server: select-then-insert stored 2 rows, a unique constraint stored 1).
- **Key expiry:** after the retention window the key is accepted as new; document it (Stripe v1 prunes keys that are at least 24 hours old).
- **Retry after timeout:** server finished but client timed out, client retries with the same key: no duplicate.

## Message consumer idempotency
- Publish the same message twice (same message ID): one effect. Inspect DB state, emitted events and external calls (stub request counts).
- **Out of order:** deliver update v2 before v1; final state must be v2 (version or timestamp checks).
- **Crash between effect and ack:** kill the consumer after the DB commit but before ack; the redelivered message must be detected (dedup table, unique constraint, or upsert).
- **Poison message:** malformed message goes to the dead-letter queue after N attempts without blocking the partition.

```bash
for i in 1 2; do curl -s -X POST https://api.example/payments -H "Idempotency-Key: qa-123" -d @pay.json & done; wait
# then count rows for the key with your database client: select count(*) from payments where client_ref='qa-123'   -- expect 1
```

## Verify
For each side-effecting endpoint and consumer, the duplicate, concurrent-duplicate and crash-redelivery tests show exactly one effect.
