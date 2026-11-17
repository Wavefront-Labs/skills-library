---
id: computing-software.cybersecurity-defensive.application-security.openapi-schema-validation
name: openapi-schema-validation
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [schema-validation, openapi, json-schema, api-security, mass-assignment, positive-security-model]
level: practitioner
status: docs-checked
description: "Enforce OpenAPI schemas on API requests and responses: strict types, additionalProperties false, bounds, gateway vs in-app validation, and testing the contract."
sources: ["https://spec.openapis.org/oas/v3.1.0", "https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html", "https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenAPI schema validation

A positive security model: the OpenAPI document says exactly what is allowed, and anything else is rejected
before business logic runs. It blocks mass assignment, type confusion and many injection payloads, and makes
excessive data exposure visible.

## Write schemas that constrain
```yaml
components:
  schemas:
    UpdateProfile:
      type: object
      additionalProperties: false          # rejects "isAdmin": true (mass assignment)
      required: [displayName]
      properties:
        displayName: {type: string, minLength: 1, maxLength: 64, pattern: "^[A-Za-z0-9 ._-]+$"}
        age:         {type: integer, minimum: 13, maximum: 130}
        email:       {type: string, maxLength: 254}
```
- `additionalProperties: false` on every request object (a JSON Schema keyword used in the OpenAPI Schema Object).
- Bounds on every string (`maxLength`), array (`maxItems`) and number; enums for closed sets.
- Path and query parameters typed too.
- Response schemas: validate in tests (or in non-prod at runtime) to catch fields leaking (password hashes,
  internal flags).

## Where to enforce
- **In the app** with a validator generated from or bound to the spec. Binding to explicit DTOs rather than ORM entities is the mass-assignment fix even without a spec.
- **At the gateway** or WAF with schema enforcement. Good first line, but keep app validation because internal callers bypass the gateway.

## Lint and test the spec
- Lint the spec with an OpenAPI linter and an API-security ruleset to flag missing bounds, missing `additionalProperties`, unauthenticated operations.
- Contract fuzzing from the spec to send boundary values and confirm the API rejects invalid input with 4xx, never 5xx.

## Gotchas
- Spec drift: if the spec is hand-maintained, undocumented endpoints skip validation. Generate spec from code
  or fail CI when routes lack a spec entry.
- Regex `pattern` with nested quantifiers can cause ReDoS in the validator.
- Validation errors should not echo the full payload back.

## Verify
Sending an extra property, an over-long string and a wrong type to a write endpoint all return 400; spec lint and contract
tests run in CI.

## Checked
2026-10-28. Confirmed against official pages: the additionalProperties keyword (OpenAPI Specification 3.1.0) and the mass-assignment framing (OWASP API3:2023, OWASP REST Security Cheat Sheet).
Removed or rewritten: the unevaluatedProperties note, format email/uuid, a unicode-class regex, named validator libraries and gateway products, and the Spectral and Schemathesis commands (none appear in the fetched pages).
Method: documentation only; no commands were run.
