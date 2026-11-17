---
id: computing-software.qa-testing-engineering.test-case-design.equivalence-partitioning-api-parameters-and-enums
name: equivalence-partitioning-api-parameters-and-enums
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [api-parameter-partitions, enum-partitions, equivalence-partitioning, api-testing, openapi]
level: practitioner
status: docs-checked
description: "Partition API parameters and enums: types, required/optional/null, enum members, unknown values, pagination and query combos, mapped to expected status codes."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://swagger.io/specification/
  - https://www.rfc-editor.org/rfc/rfc9110.html#name-status-codes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Applying EP to API parameters and enums

**Goal:** cover each request field's classes of values with expected responses, derived from the OpenAPI contract.

## Partitions per parameter
| Aspect | Partitions | Typical expected result |
|---|---|---|
| Presence | present, absent (required vs optional), `null`, empty string | 400/422 for missing required |
| Type | correct, wrong JSON type (`"5"` vs `5`), array vs object | 400/422 |
| Enum | each member that changes behaviour, unknown value, wrong case `"ACTIVE"` vs `"active"` | 422 for unknown |
| Range/length | valid, below min, above max (`maxLength` and other JSON Schema keywords in the schema) | 422 |
| Format | `date-time`, `uuid`, `email` valid vs malformed | 400/422 |
| Location | path, query, header, body each validated | 404 vs 400 for bad path IDs |
| Authorisation | own resource, other tenant's, no token | 200 / 403 or 404 / 401 |
| Unknown fields | extra property | ignored or rejected, per the schema and the API's documented policy |

## Enums specifically
- Each enum member is its own partition only if behaviour differs; group members with identical handling.
- Test forward compatibility: what does a client do when the server returns a new enum value? Spec it.
- Response enums are output partitions; make sure each is produced by some test.

## Building the set
1. Export parameters from the OpenAPI schema; one table row per parameter.
2. Valid partitions combined into a few happy-path requests (each-choice); each invalid partition in its own request.
3. Assert status code, error body shape and that no side effect happened.
4. Automate negative cases with schema-based generators as a complement.

## Gotchas
- 500 for any invalid input is a defect; validation should return 4xx.
- Path parameter partitions: non-existent ID, malformed ID, other tenant's ID should not leak existence (404 rather than 403 if policy says so).
- Query arrays (`?status=a&status=b`) and duplicates behave differently per framework.

## Verify
Every schema parameter has valid and invalid partitions with an expected status, and no invalid partition returns 5xx.

## Checked

2026-10-28 Confirmed against: RFC 9110 (400, 401, 403, 404 and 422 Unprocessable Content status codes); OpenAPI specification (`maxLength`, `date-time` format as JSON Schema). Removed or generalised: `additionalProperties: false`, RFC 9457, and the Schemathesis name (not found in the fetched pages), and `minimum` as a named schema keyword.

Method: documentation only; no commands were run.
