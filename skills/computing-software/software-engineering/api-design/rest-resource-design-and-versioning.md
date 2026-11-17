---
id: computing-software.software-engineering.api-design.rest-resource-design-and-versioning
name: rest-resource-design-and-versioning
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, rest, http-api, resource-modelling, http-status-codes, pagination, cursor-pagination, keyset-pagination, idempotency, idempotency-key, rfc-9457, problem-details, rfc-7807, versioning, backward-compatibility, breaking-changes, openapi, oasdiff, spectral, etag, if-match, optimistic-concurrency, rate-limiting, deprecation-header, sunset-header, software-engineering]
level: practitioner
status: docs-checked
description: "Design HTTP/REST APIs that last: resource modelling, correct status codes, token pagination, idempotency keys, RFC 9457 errors, compatible evolution and deprecation headers."
sources:
  - https://www.rfc-editor.org/rfc/rfc9110
  - https://www.rfc-editor.org/rfc/rfc9457
  - https://www.rfc-editor.org/rfc/rfc9745
  - https://www.rfc-editor.org/rfc/rfc8594
  - https://www.rfc-editor.org/rfc/rfc7396
  - https://google.aip.dev/158
  - https://google.aip.dev/180
  - https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REST resource design and versioning

**Goal:** design endpoints that are predictable, safe to retry, cheap to page through, and that can evolve without breaking clients you cannot see.

## 1. Model resources, not procedures
- Nouns in plural collections, ids underneath: `GET /orders`, `GET /orders/{order_id}`, `POST /orders`, `PATCH /orders/{order_id}`. Nest only for true ownership, max one level; otherwise filter: `GET /items?order_id=...`.
- Ids are opaque strings, not auto-increment integers that leak volume and invite enumeration.
- Actions that are not CRUD become either a state field (`PATCH {"status":"cancelled"}`) or a custom verb. Pick one convention.
- Long-running work: `202 Accepted` and a `Location` to poll.
- One field casing across the API.

## 2. Status codes that mean something
RFC 9110 defines these classes; use them consistently.
| Situation | Code |
|---|---|
| Read OK / update returning body | 200 |
| Created (with `Location` header) | 201 |
| Accepted for async processing | 202 |
| Success, no body (DELETE) | 204 |
| Malformed / failed validation | 400 (or 422 for semantic errors; be consistent) |
| Not authenticated / authenticated but forbidden | 401 / 403 |
| Not found | 404 |
| State conflict, duplicate | 409 |
| Precondition (`If-Match`) failed | 412 |
| Server fault / bad upstream / unavailable | 500 / 502 / 503 |

Never return 200 with an error body: it defeats proxies, retry policies and dashboards.

## 3. Errors: RFC 9457 Problem Details
Serve `Content-Type: application/problem+json`:
```json
{"type":"https://example.com/problems/insufficient-funds",
 "title":"Insufficient funds","status":409,
 "detail":"Balance 30.00 is less than 50.00",
 "instance":"/payments/pay_123"}
```
Consumers must use the `type` URI as the problem type's primary identifier; `title` and `detail` are human text. `type` defaults to `about:blank` when absent. RFC 9457 obsoletes RFC 7807.

## 4. Pagination: tokens, not offsets
Google AIP-158: collection requests take an optional `page_size` and `page_token`; responses carry `next_page_token`.
- If `page_size` is unspecified the API picks and documents a default; above the maximum it coerces down; a negative value is an `INVALID_ARGUMENT` error.
- If the user changes `page_size` on later pages, the service honours the new size.
- Keep the token opaque so its format can change later.

## 5. Idempotency for unsafe retries
GET, PUT and DELETE are idempotent by definition (RFC 9110); POST is not. The IETF httpapi `Idempotency-Key` header (an Internet-Draft, not an RFC; check its status) lets clients send a key on non-idempotent requests; the draft describes an optional idempotency fingerprint generated from request payload data, so a reused key with a different request can be detected.

Use `ETag` with `If-Match` on PUT/PATCH for optimistic concurrency; a mismatch returns `412`.

## 6. Versioning and compatible evolution
- AIP-180: new components (methods, messages, fields, enum values) may be added in the same major version, and removing a component is a backwards-incompatible change.
- Enum values need care: client code may not handle new values gracefully, so document enums as open-ended from day one.
- Don't mint a v2 for anything you can add compatibly.
- Retiring: the `Deprecation` header (RFC 9745) carries the deprecation date; add `Sunset` (RFC 8594) for the date the resource is expected to become unresponsive, which must not be earlier than the deprecation date. Track per-client usage before removal.

## Gotchas
- JSON Merge Patch (RFC 7396) cannot set a member to `null` as a value, because `null` means delete the member; decide how nullable fields are handled and document it.
- Cursor tokens that embed filters must be rejected if the filters change between calls.

## Verify
- [ ] Every endpoint is a noun resource; ids are opaque strings.
- [ ] No error path returns 2xx; errors are `application/problem+json` with a stable `type`.
- [ ] List endpoints use opaque tokens with a server-enforced maximum page size.
- [ ] Side-effecting POSTs accept `Idempotency-Key`.
- [ ] Deprecated surfaces emit `Deprecation`/`Sunset` and usage is tracked per client.

## Checked
2026-11-01. Confirmed in RFC 9457 (members, `application/problem+json`, `about:blank` default, obsoletes 7807),
RFC 9745 and RFC 8594 (Deprecation and Sunset ordering), Google AIP-158 (page size and token rules),
AIP-180 (additions and removals, enum caution), the IETF idempotency-key draft (Internet-Draft; fingerprint) and
RFC 7396. Status code names are those of RFC 9110. Removed unconfirmed claims: ULID/UUIDv7 ids, the
`:cancel` custom verb, RFC 3339 and money advice, 429 and `Retry-After`, the keyset SQL, token signing, page-size
numbers, idempotency TTL and in-flight conflict rules, the Stripe-style versioning, OpenAPI tool commands and
the 404-versus-403 and backoff gotchas. The merge-patch null point is paraphrased from RFC 7396.
Method: documentation only; no commands were run.
