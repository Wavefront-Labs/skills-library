---
id: computing-software.software-engineering.api-design.batch-and-bulk-operations
name: batch-and-bulk-operations
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, pagination, batch-operations, bulk-api, aip-231, partial-failure, atomicity]
level: practitioner
status: docs-checked
description: "Design batch API operations: batchGet/batchCreate/batchDelete (AIP-231/233/235), atomic vs partial success, per-item failures and generic JSON batching."
sources:
  - https://google.aip.dev/231
  - https://google.aip.dev/233
  - https://google.aip.dev/235
  - https://learn.microsoft.com/en-us/graph/json-batching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch and bulk operations

Clients making hundreds of single calls waste round trips. Offer batch methods where clients genuinely operate on many items. All AIP batch methods are optional ("APIs may support").

## Typed batch methods (Google AIP-231, 233, 235)
```
GET  /v1/publishers/p1/books:batchGet?names=publishers/p1/books/1&names=publishers/p1/books/2
POST /v1/publishers/p1/books:batchCreate   {"requests": [{"book": {...}}, {"book": {...}}]}
POST /v1/publishers/p1/books:batchDelete   {"names": ["publishers/p1/books/1"]}
```
- URIs end with `:batchGet`, `:batchCreate` or `:batchDelete`; Get uses GET with no body, Create and Delete use POST (Delete must not use the DELETE verb) with body `"*"`. The URI path is the resource's collection; `-` may be accepted as a wildcard parent when the operation spans parents.
- Request shape: a `parent` (optional for top-level resources; if set it must match the parent of every item) plus a repeated `names` (Get and Delete) or repeated `requests` (Create); the field comment must document the maximum, and the AIP examples use 1000 items. Empty `names` should return `INVALID_ARGUMENT`.
- BatchGet: response order must match the order of `names`; the operation must be atomic (all succeed or all fail), and if any location is down it must fail; it should not paginate. For partial failures use List (AIP-132). Filter-based matching must not be supported in BatchDelete.
- Fields that must be unique per item (client-provided IDs, etags) cannot be hoisted to the batch level.

## Atomic vs partial success (AIP-233, AIP-235)
- A synchronous batch Create or Delete must be atomic. An asynchronous one (returns a `google.longrunning.Operation`) may be atomic or partial.
- Choose by the complexity of ensuring atomicity (simple database pass-through suggests atomic, complex resources suggest partial) and the end-user experience (is it acceptable for a large batch to fail on a few bad entries?).
- Partial success on an Operation: the metadata message includes `map<int32, google.rpc.Status> failed_requests`, keyed by the request's index, with errors mirroring the singular standard method. Transient errors that server retries may still fix are not reported there. If every request fails, set `Operation.error` with code `Aborted`.
- An existing API adopts partial success only by keeping its atomic default and adding a `bool return_partial_success` request field; a synchronous API cannot adopt it (a new version returning an Operation is needed), because a plain OK means "all succeeded" to existing clients.

## Generic batching (Microsoft Graph JSON batching)
One `POST https://graph.microsoft.com/v1.0/$batch` with a `requests` array; each item has a required string `id` (unique in the batch, else 400), `method`, relative `url`, and optional `headers` and `body` (headers with `Content-Type` are required when a body is sent). Graph limits a batch to 20 requests.
- The response has a `responses` array; items can come back in a different order, so correlate on `id`. Each item has its own `status`.
- The batch response status is typically 200 or 4xx: 400 if the batch itself is malformed, otherwise 200, which does not mean the individual requests succeeded. Clients must check every item.
- `dependsOn` sequences requests; a request whose dependency failed fails with 424 (Failed Dependency). Graph advises a batch be fully sequential or fully parallel.
- Each request is evaluated individually against throttling limits and fails with 429 if it exceeds them.
- Generic batching loses per-endpoint semantics, which makes it harder to rate-limit and cache (author's assessment).

## Verify
- [ ] Tests for atomic rollback on one bad item, or per-item errors in partial mode.
- [ ] Oversized batch is rejected, and the rate limiter counts items.

## Checked
2026-11-08. Read in full: AIP-231, AIP-233, AIP-235 and the Microsoft Graph JSON batching page. Removed: the `batchUpdate` example (AIP-234 not read), the sample partial-result JSON and 207 Multi-Status commentary, a 100-1000 item cap range, `Idempotency-Key` on batch writes, the bulk-job section (Salesforce Bulk API and Shopify claims: the Salesforce page fetched as a 1,365-character stub and Shopify was never cited), and the atomic-versus-partial comparison table. See the bulk-export-and-import-jobs skill for async jobs.
Method: documentation only; no commands were run.
