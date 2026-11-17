---
id: computing-software.software-engineering.api-design.request-validation-against-openapi
name: request-validation-against-openapi
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, request-validation, openapi, json-schema, input-validation, problem-details]
level: practitioner
status: gated
description: "Validate every request against the OpenAPI/JSON Schema contract at the edge, return precise 400/422 problem details, and keep business validation separate."
sources: ["https://github.com/cdimascio/express-openapi-validator", "https://json-schema.org/understanding-json-schema", "https://www.rfc-editor.org/rfc/rfc9457", "https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validating requests against the schema

## Two layers
1. **Contract/syntactic**: types, required fields, formats, lengths, enums, unknown fields. Do it
   generically from the OpenAPI spec at the edge, before handlers run.
2. **Semantic/business**: "end_date after start_date", "SKU exists", "user may do this". In the
   domain layer, returning 422 or 409.

## Contract validation options
| Stack | Tool |
|---|---|
| Node/Express | `express-openapi-validator` (validates requests, optionally responses) |
| Fastify | built-in JSON Schema per route (Ajv) |
| Python | FastAPI/Pydantic models (spec generated from code); `openapi-core` for spec-first |
| Java | Spring `@Valid` + Bean Validation; `swagger-request-validator` for spec-first |
| .NET | DataAnnotations/FluentValidation; minimal API filters |
| Gateway | Kong/Apigee/AWS API Gateway request validators, Envoy + schema filters |

`express-openapi-validator` was run (v. current): an unknown body field returned 400 with `must NOT have additional properties` and `?limit=abc` returned 400, but with one request that broke three rules it reported only the first error, so report-all needs extra configuration (check its `allErrors`-style options in its README, not confirmed here). Tools for Java, .NET and gateways in the table were not run (gated: unconfirmed, source is paywalled or blocked).

## Schema tightness
- `additionalProperties: false` on request bodies (reject unknown fields).
- `maxLength` on every string, `maxItems` on arrays, `minimum/maximum` on numbers, `pattern` for ids.
  Unbounded inputs are DoS and storage-abuse vectors.
- `format: date-time`, `email`, `uuid`: Ajv 8 throws `unknown format "email" ignored in schema` at compile time unless `ajv-formats` is registered (and silently skips them with `strict: false`); with `ajv-formats` an invalid email failed validation (run).
- Query/path params validated and coerced too (`?limit=abc`).
- Body size limit at the server (`express.json({limit:'100kb'})` returned 413 for a 200 KB body and 200 for a tiny one (run); nginx `client_max_body_size` was not run (gated: unconfirmed, source is paywalled or blocked)).

## Error response (RFC 9457)
```json
HTTP/1.1 400 Bad Request
Content-Type: application/problem+json
{"type":"https://api.example.com/problems/validation","title":"Invalid request","status":400,
 "errors":[{"pointer":"/items/0/quantity","detail":"must be >= 1"},
           {"pointer":"/email","detail":"must be a valid email"}]}
```
Report **all** errors with JSON Pointers to the field, not just the first.

## Verify
Contract fuzzing (Schemathesis 4.32: `schemathesis run openapi.yaml --url http://localhost:8000`; `--base-url` is rejected as "No such option" in that version) finds inputs that
crash handlers or are accepted despite violating the schema.
