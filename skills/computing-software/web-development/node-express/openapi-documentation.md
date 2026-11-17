---
id: computing-software.web-development.node-express.openapi-documentation
name: openapi-documentation
category: computing-software
field: web-development
product: node-express
tags: [rest-api, openapi, api-documentation, swagger, contract-testing, api-design]
level: practitioner
status: docs-checked
description: "Documenting REST APIs with OpenAPI 3.1: design-first vs code-first, reusable components, examples, security schemes, linting, rendering docs and generating clients."
sources:
  - https://spec.openapis.org/oas/v3.1.1.html
  - https://learn.openapis.org/
  - https://redocly.com/docs/cli/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenAPI documentation

## 1. Design-first or code-first
- **Design-first**: write `openapi.yaml`, review it like code, then implement and validate requests/responses against it (request validators and mock servers exist for most stacks). Best for public/partner APIs.
- **Code-first**: generate the spec from annotations or types in your framework. Fast, but the spec drifts toward implementation detail.

## 2. Skeleton (3.1)
```yaml
openapi: 3.1.0
info: { title: Orders API, version: 2.3.0 }
servers: [{ url: https://api.example.com/v2 }]
security: [{ bearerAuth: [] }]
paths:
  /orders/{orderId}:
    get:
      operationId: getOrder
      summary: Get an order
      parameters: [{ $ref: "#/components/parameters/OrderId" }]
      responses:
        "200": { description: The order, content: { application/json: { schema: { $ref: "#/components/schemas/Order" }, examples: { paid: { $ref: "#/components/examples/PaidOrder" } } } } }
        "404": { $ref: "#/components/responses/NotFound" }
components:
  securitySchemes: { bearerAuth: { type: http, scheme: bearer, bearerFormat: JWT } }
  parameters: { OrderId: { name: orderId, in: path, required: true, schema: { type: string, pattern: "^ord_[a-z0-9]+$" } } }
  responses: { NotFound: { description: Not found, content: { application/problem+json: { schema: { $ref: "#/components/schemas/Problem" } } } } }
```
3.1 aligns schemas with JSON Schema 2020-12.

## 3. Quality
- Unique, stable `operationId`s (client method names).
- Descriptions for every operation and field (units, formats, enums meaning), realistic `examples`.
- Document errors, pagination, rate limit headers, idempotency headers, auth scopes.
- Lint the spec in CI (Redocly CLI documents API linting) with rules for naming, descriptions, security on every operation.
- Detect breaking changes between spec versions in PRs.

## 4. Use it
- Render docs from the spec with a documentation renderer.
- Generate clients/SDKs from the spec.
- Contract tests: validate responses against the spec in integration tests.

## Verify
Spec linting passes in CI; responses validate against the spec; docs render with examples for every operation.

## Checked
2026-10-28 Confirmed on the OpenAPI 3.1.1 specification (schema objects follow JSON Schema Draft 2020-12; operationId) and Redocly CLI docs (API linting). The Stoplight Spectral page returned 404 and was dropped from sources. Removed: named code generators, linters other than the Redocly mention, diff tool, doc renderers, client generators and contract-testing tools (not on fetched pages), and the nullable detail.
Method: documentation only; no commands were run.
