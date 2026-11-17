---
id: computing-software.web-development.node-express.idempotency-keys-and-safe-retries
name: idempotency-keys-and-safe-retries
category: computing-software
field: web-development
product: node-express
tags: [rest-api, idempotency-keys, retries, payments, api-design, distributed-systems]
level: practitioner
status: verified
description: "Making POST endpoints safe to retry with Idempotency-Key headers: storing request fingerprints and responses, concurrency locking, expiry, and client retry behaviour."
sources:
  - https://docs.stripe.com/api/idempotent_requests
  - https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/
  - https://brandur.org/idempotency-keys
  - https://www.rfc-editor.org/rfc/rfc9110#name-idempotent-methods
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Idempotency keys and safe retries

Networks fail after the server commits but before the client sees the response. Without idempotency, the client's retry charges the card twice.

## 1. Method semantics
GET, PUT, DELETE are idempotent by definition (same effect if repeated) - design them so. POST and PATCH aren't; make them safe with an **Idempotency-Key** header (IETF draft, Stripe convention).

## 2. Server algorithm
```
POST /payments
Idempotency-Key: 5f0c7a52-3c8e-4b0a-9f39-2a6f0f0b9d11
```
The IETF draft (`draft-ietf-httpapi-idempotency-key-header`, revision 07 of October 2025, expired 18 April 2026 and still a draft) writes the value as a quoted structured-field string (`Idempotency-Key: "8e03978e-..."`) and says a missing key on an operation that requires it SHOULD get 400, an in-flight duplicate 409, and the same key with a different payload 422; Stripe sends it unquoted.
1. Require the key on unsafe endpoints that create side effects (or accept optionally). Validate format (UUID).
2. Look up `(account_id, key)`:
   - **Not found**: insert a row `{ key, request_fingerprint (hash of method+path+body), status: "in_progress", locked_at }` in the same DB with a unique constraint - this is the lock.
   - **Found, completed**: return the stored status code and body verbatim (also for stored errors 4xx; storing 5xx is a design choice: Stripe replays even 500 responses for the same key, while not storing them lets the client retry the work).
   - **Found, in progress**: return 409 Conflict (concurrent duplicate) - client retries later.
   - **Fingerprint differs**: 422 - key reused with a different payload.
3. Perform the operation; write side effects and the stored response **in the same transaction** where possible. For external calls (payment provider), pass your key downstream (Stripe accepts its own Idempotency-Key) and record progress steps (recovery points).
4. Expire keys after a window (Stripe API v1: keys can be removed once at least 24 h old; keys are up to 255 characters); document it.

```sql
CREATE TABLE idempotency_keys (
  account_id bigint, key text, fingerprint text, status text, response_code int, response_body jsonb,
  created_at timestamptz default now(), PRIMARY KEY (account_id, key));
```

## 3. Client behaviour
- Generate one key per logical operation (UUIDv4), persist it with the pending action (so a page reload reuses it), reuse on every retry.
- Retry on network errors/timeouts/5xx/409 with exponential backoff and jitter; never on other 4xx.

## 4. Other idempotency tools
- Natural keys + unique constraints (`order_number`), upserts (`INSERT ... ON CONFLICT DO NOTHING`).
- Conditional requests: `If-Match` ETags for updates (412 on mismatch).
- Message consumers: dedupe by message id (outbox/inbox tables) since queues deliver at least once.

## Verify
Test: fire the same request twice concurrently and sequentially - one side effect, identical responses; same key + different body -> 422; key expiry job runs.
