---
id: computing-software.web-development.node-express.api-versioning-and-deprecation
name: api-versioning-and-deprecation
category: computing-software
field: web-development
product: node-express
tags: [rest-api, api-versioning, deprecation, sunset-header, breaking-changes, api-design]
level: practitioner
status: docs-checked
description: "Versioning HTTP APIs and retiring old versions: URL vs header vs date-based versions, additive non-breaking changes, Deprecation and Sunset headers, and migration communication."
sources:
  - https://www.rfc-editor.org/rfc/rfc8594
  - https://datatracker.ietf.org/doc/rfc9745/
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/410
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API versioning and deprecation

## 1. Avoid needing versions
Most changes can be **additive and backward compatible**: new optional fields, new endpoints, new optional params, new enum values (only if clients were told to tolerate unknown values). Clients must ignore unknown fields (tolerant reader).
Breaking changes: removing/renaming fields, changing types/formats, making optional params required, changing defaults, changing error codes or auth, changing pagination/ordering semantics.

## 2. Strategies
| Strategy | Example | Notes |
|---|---|---|
| URL major version | `/v1/orders`, `/v2/orders` | simplest, cache-friendly, visible; coarse |
| Header/media type | `Accept: application/vnd.acme.v2+json` | clean URLs; harder to test in a browser |
| Date-based pinned version | a version header holding a date | fine-grained; server keeps transformation layers per change |
| Query param | `?api-version=2024-05-01` | explicit, easy |
Pick one per API and document it. Internally, keep one current implementation and translate old versions at the edges (request/response transformers) instead of forking code.

## 3. Deprecation lifecycle
1. Announce in changelog, docs, email to affected consumers (identify them from logs/API keys).
2. Mark responses:
```
Deprecation: @1767225600                       (RFC 9745, date it became deprecated)
Sunset: Wed, 30 Jun 2027 23:59:59 GMT          (RFC 8594, when it stops working)
Link: <https://developer.example.com/migrate-v2>; rel="deprecation"; type="text/html"
```
The `Deprecation` value is a Unix timestamp prefixed with `@`; `Sunset` is an HTTP date. Both RFCs make the headers informational: clients not interpreting them keep working.
3. Mark in OpenAPI (`deprecated: true`) so SDKs and docs flag it.
4. Monitor usage per consumer; reach out to stragglers.
5. Brownouts before sunset (scheduled short periods returning errors) to surface hidden dependents.
6. Remove; return `410 Gone` with a body linking to migration docs. Pick the notice window to match your contracts/SLAs.

## 4. Guard against accidental breaks
Diff the OpenAPI spec for breaking changes in CI, add consumer-driven contract tests, and snapshot-test response shapes.

## Checked

2026-11-01. Confirmed in RFC 9745 (`Deprecation: @<timestamp>`, `rel="deprecation"` link) and RFC 8594 (`Sunset` single HTTP-date, informational), MDN 410 Gone. Removed: Stripe and Azure specifics, typical window figures, tool names.

Method: documentation only; no commands were run.

## Verify
Old-version consumers keep working until the announced sunset; deprecated endpoints emit headers; usage dashboard per version trends to zero before removal.
