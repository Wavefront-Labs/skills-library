---
id: computing-software.software-engineering.api-design.idempotency-and-pagination
name: idempotency-and-pagination
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, idempotency, idempotency-key, retries, pagination, cursor-pagination, optimistic-locking, etag, concurrent-writes, http-methods, at-least-once-delivery]
level: advanced
status: verified
description: "Design idempotent write APIs with idempotency keys so client retries can't double-charge, and cursor pagination that stays correct under concurrent writes."
sources: ["https://docs.stripe.com/api/idempotent_requests", "https://www.rfc-editor.org/rfc/rfc9110", "https://relay.dev/graphql/connections.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Idempotency and pagination — correct under retries and concurrent writes

**Goal:** a client that retries a timed-out write never double-applies it, and a
client paginating a list never sees duplicates or gaps caused by concurrent writes.

## 1. Retries are inevitable; design for them, don't hope they don't happen
A client times out waiting for a response — it genuinely cannot tell whether the
server received and processed the request or not. The client's only safe move is to
retry; the server's job is to make that retry harmless.
```
POST /charges
Idempotency-Key: 7d3c9f1a-...
```
Server stores `(idempotency_key) -> (response, status)` on first processing;
any retry with the same key returns the stored response without re-executing the
side effect (charging a card, sending an email). Key scoping matters: scope to the
resource/endpoint and typically the caller/account, not globally, and expire keys
after a bounded window (Stripe's API v1 docs: keys can be removed once they are at least 24 hours old, a reused pruned key makes a new request, and reusing a key with different parameters is an error) so the storage doesn't grow
unbounded and so a key can eventually be reused on legitimate purpose. Store the key
atomically with the side effect (same DB transaction) — storing it after the side
effect leaves a window where a retry during that gap double-executes.

## 2. HTTP method semantics are a form of idempotency contract
`GET`, `PUT`, `DELETE` are specified as idempotent (RFC 9110 section 9.2.2: PUT, DELETE and the safe methods are idempotent) (repeating has the same effect as
doing it once) — `PUT /users/5 {name: "Alice"}` twice leaves the same end state.
`POST` is **not** idempotent by the spec — `POST /charges` twice is two charges,
which is exactly why POST endpoints that create side effects need the explicit
Idempotency-Key mechanism above; relying on "well PUT would be idempotent" doesn't
apply to POST without that extra mechanism.

## 3. Optimistic concurrency for "read, modify, write" races
```
GET /doc/5           -> ETag: "v7"
PUT /doc/5
If-Match: "v7"       -> 412 Precondition Failed if the doc changed since
```
Without this, two concurrent editors' writes race and one silently overwrites the
other (last-write-wins, with no warning). A version field (or ETag) the client must
echo back on write turns a silent lost-update into a detectable 412/409 the client
can resolve (refetch, merge, re-prompt the user) — this is the API-level equivalent
of a DB's optimistic locking column.

## 4. Cursor (keyset) pagination stays correct under concurrent writes; offset does not
```
GET /items?limit=20&cursor=eyJpZCI6MTAyMzR9
```
Offset pagination (`page=3&limit=20`) computes position by counting rows — if an item
is inserted/deleted before the current offset between page requests, the client sees
a duplicate or misses an item entirely. A cursor encodes a stable anchor (typically
the sort key's value of the last item seen, e.g. `id > 10234`), so a page is defined
relative to actual data, not a shifting count — inserts/deletes elsewhere in the list
don't perturb pages already fetched or in flight.
Checked in SQLite (60 rows, newest first, page size 20): after one insert at the top, offset page 2 repeated id 41 from page 1; the `id < last_id` cursor repeated nothing. With rows tied on `ts`, `where ts > last_ts` skipped the tied row id 5 while `(ts, id) > (last_ts, last_id)` returned it (verified on the tuple comparison form SQLite supports).

## 5. Designing the cursor itself
- Encode it opaquely (base64 a JSON payload of sort-key values), not as a raw
  row ID — this lets you change the underlying implementation later without
  breaking clients who might otherwise parse/construct cursors themselves.
- Include enough of the sort key to break ties: if sorting by `created_at` alone and
  two rows share a timestamp, paginating by timestamp alone can skip or repeat one of
  them — compound cursor (`created_at`, `id`) resolves ties deterministically.
- Validate cursor input server-side (it's still client-supplied data) — a malformed
  or tampered cursor should 400, not crash the query.

## Gotchas
- An idempotency key that only dedupes at the HTTP layer (a reverse proxy cache) but
  not at the business-logic layer misses retries that differ slightly at the
  transport level (different connection) but are logically the same client retry.
- Returning a different status code on the idempotent replay (e.g. 201 first time,
  200 on replay) can break clients that pattern-match on status — document and keep
  it consistent.
- `DELETE` is "idempotent" in the sense that repeating it leaves the same end state
  (resource gone), but many implementations return 404 on the second call and treat
  that as an error — decide and document whether a repeat DELETE returns 200/204
  idempotently or 404, and keep clients informed either way.

## Verify
- [ ] Every POST endpoint with a side effect (charge, send, create-with-external-effect)
      accepts and honors an idempotency key, tested by sending the same request twice.
- [ ] A concurrent-write race on an update endpoint was tested (two writers, one
      should get a conflict response) rather than assumed safe.
- [ ] List endpoints use cursor pagination with a compound, tie-breaking sort key, not
      bare offset/limit, for any list that can mutate while being paginated.
- [ ] Cursors are opaque and validated server-side, not raw client-constructable IDs.

Related: computing-software.software-engineering.api-design.rest-resource-design-and-versioning,
computing-software.software-engineering.api-design.graphql-schema-design
