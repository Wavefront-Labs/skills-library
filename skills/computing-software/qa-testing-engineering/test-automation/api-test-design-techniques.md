---
id: computing-software.qa-testing-engineering.test-automation.api-test-design-techniques
name: api-test-design-techniques
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [api-test-design, api-testing, white-box-testing, negative-testing, rest-api-testing, http-status-codes, idempotency]
level: practitioner
status: docs-checked
description: "Design API tests systematically: per-endpoint partitions, required/optional fields, status codes, auth, idempotency, pagination, error contracts and concurrency."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta-v4-0
  - https://www.rfc-editor.org/rfc/rfc9110
  - https://www.rfc-editor.org/rfc/rfc9457
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API test design

**Goal:** thorough tests for an API endpoint, applying test techniques to the interface itself.


## Per endpoint checklist
1. **Happy path**: valid request, correct status (200/201/204), response schema, persisted state (GET after POST).
2. **Field partitions and boundaries**: each field's valid/invalid partitions and BVA (lengths, ranges); required field missing; null vs absent vs empty; wrong types; extra unknown fields (rejected or ignored as specified).
3. **Auth**: no token (401), expired/invalid token (401), valid token without permission (403), other tenant's resource (404 or 403: no data leak, see `authorization-and-idor-testing`).
4. **Status codes**: 400 vs 422 validation, 404 unknown id, 409 conflict/invalid state, 415 wrong content type, 405 wrong method.
5. **Error contract**: consistent error body (RFC 9457 problem details: `type`, `title`, `detail`, per the RFC's problem-details members), no stack traces.
6. **Idempotency**: PUT/DELETE repeated give the same result; POST with whatever idempotency mechanism the API documents does not create duplicates on retry.
7. **Pagination, filtering, sorting**: first/last/empty page, page size limits, stable sort with ties, filter combinations.
8. **Concurrency**: simultaneous updates (lost update, ETag/If-Match -> 412).
9. **Headers**: caching (`Cache-Control`, `ETag`), CORS for browser clients, content negotiation.
10. **Non-functional**: response time per endpoint, payload size limits.

## Implementation
Any HTTP client in your test framework (Playwright `request`, pytest + httpx, REST Assured, Postman/Newman); schema validation with JSON Schema/OpenAPI (`schemathesis-openapi-testing` for generated cases).

## Gotchas
- Testing only through the UI leaves API-level validation untested; attackers and other clients use the API directly.

## Verify
For each endpoint, a checklist table mapped to tests, with auth and error-contract cases present.

## Checked

2026-11-02. Checked against RFC 9110 (401, 405, 409, 412, 415, 422 semantics; PUT and DELETE are idempotent) and RFC 9457 (problem details members type, title, detail). Removed: the ISTQB CTAL-TTA syllabus section number (the ISTQB page returned a server error, so it was not confirmed), the 429 status (defined in RFC 6585, not fetched) and the specific Idempotency-Key header name (not in RFC 9110). The ISTQB source link is kept but unverified.

Method: documentation only; no commands were run.
