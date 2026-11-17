---
id: computing-software.software-engineering.api-design.preventing-mass-assignment-and-data-exposure
name: preventing-mass-assignment-and-data-exposure
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-security, mass-assignment, excessive-data-exposure, owasp-api-top-10, bopla, dto]
level: practitioner
status: docs-checked
description: "Stop mass assignment and excessive data exposure (OWASP API3 BOPLA) with explicit input and output DTOs, field allow-lists and response schemas."
sources: ["https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/", "https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html", "https://github.blog/2012-03-04-public-key-security-vulnerability-and-mitigation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mass assignment and excessive data exposure

OWASP API Security 2023 merges both into **API3: Broken Object Property Level Authorization**. An endpoint is vulnerable if it exposes properties the user should not read (formerly "Excessive Data Exposure"), or lets the user change, add or delete properties they should not access (formerly "Mass Assignment").

## Mass assignment
Binding request data straight onto a model lets clients set fields they should not:
```
PATCH /users/me  {"display_name": "x", "role": "admin", "account_balance": 1e6}
```
OWASP examples: adding `total_stay_price` to a booking-approval request, or `"blocked": false` to a video description update. In 2012 a GitHub user exploited mass assignment in the public-key update form to add his key to the rails organization; GitHub's post names the root cause as a failure to check incoming form parameters.

Fixes (Mass Assignment Cheat Sheet):
- Prefer dedicated **input DTOs** containing only the fields the caller may edit (for example no `isAdmin` field), and map them explicitly to the entity. Avoid binding client input straight into internal objects where possible.
- If you must bind, allow-list fields: Spring `@InitBinder` with `binder.setAllowedFields(...)`, Mongoose with `_.pick(req.body, safeFields)`, Laravel `$fillable`, Rails Strong Parameters.
- Do not rely on a block-list alone (Spring `setDisallowedFields`, Laravel `$guarded`): a new or overlooked sensitive field stays bindable.
- DTOs and allow-lists restrict writable properties; they do not replace authorization for the object and operation, and a role-gated property (an admin may set `role`, a user may not) still needs a per-property check.
- Review nested objects too: check which inputs the binding mechanism exposes.

## Excessive data exposure
Serialising the whole entity returns everything (`password_hash`, `internal_notes`, other users' emails) and relies on the client to hide it. OWASP scenario #1: a GraphQL "report user" mutation returned the reported user's `fullName` and `recentLocation` to the reporter.
- Avoid generic serialisers such as `to_json()` / `to_string()`; cherry-pick the properties to return, and keep returned structures to the bare minimum for the endpoint.
- Always confirm the user may access each property you expose.
- Add schema-based response validation as an extra layer: define and enforce the data returned by every method (in tests, or at runtime in staging).
- GraphQL lets clients choose properties, so authorize at property level, not only per object.

## Verify
Fuzz each write endpoint with extra privileged fields and assert they are rejected or unchanged; snapshot response field sets and review diffs in code review.

## Checked
2026-11-08. Read in full: OWASP API Security Top 10 2023 page API3, OWASP Mass Assignment Cheat Sheet, and GitHub's 2012 "Public Key Security Vulnerability and Mitigation" post. Removed unsupported specifics: ASP.NET `[Bind]`, Django REST Framework `fields`/`read_only_fields`, Pydantic `extra="forbid"`, rejecting unknown fields with 400, OpenAPI `readOnly` enforcement, `additionalProperties: false` in test schemas, and per-role view classes (none appear on the cited pages; `readOnly` is also absent from the OpenAPI 3.1.0 text). Rails `permit` is kept only as a named mechanism, its code form dropped.
Method: documentation only; no commands were run.
