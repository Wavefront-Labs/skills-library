---
id: computing-software.software-engineering.api-design.openapi-components-and-references
name: openapi-components-and-references
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, openapi, openapi-refs, components, ref, json-schema, reuse, openapi-3-1]
level: practitioner
status: docs-checked
description: "Structure OpenAPI 3.1 documents with components and $ref: reusable schemas, parameters and responses, split files, and 3.1 reference rules."
sources: ["https://spec.openapis.org/oas/v3.1.0"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenAPI components and `$ref`

## Layout
```yaml
openapi: 3.1.0
paths:
  /orders/{orderId}:
    get:
      parameters: [{ $ref: '#/components/parameters/OrderId' }]
      responses:
        '200': { description: OK, content: { application/json: { schema: { $ref: '#/components/schemas/Order' } } } }
        '404': { $ref: '#/components/responses/NotFound' }
components:
  parameters:
    OrderId: { name: orderId, in: path, required: true, schema: { type: string } }
  responses:
    NotFound: { description: Not found, content: { application/problem+json: { schema: { $ref: '#/components/schemas/Problem' } } } }
  schemas:
    Order: { type: object, required: [id], properties: { id: { type: string } } }
```
Reusable: schemas, responses, parameters, examples, requestBodies, headers, securitySchemes, links, callbacks, pathItems.
Objects in `components` have no effect on the API until something outside `components` references them.

## Splitting files
Relative references (`$ref: './schemas/order.yaml'`, or `definitions.yaml#/Pet`) resolve against the referring document as base URI. Bundle into one file for publishing if your tools handle only single documents.

## 3.1 notes
- The 3.1 Schema Object is a superset of JSON Schema Draft 2020-12; the schema `example` keyword is deprecated in favour of `examples`.
- A Reference Object (`$ref` in a place that takes a Reference Object) may carry sibling `summary` and `description`, which override the referenced component's; any other sibling property is ignored. This differs from a Schema Object containing a `$ref` keyword, which is a schema and may have other keywords.
- Keys under every `components` map must match `^[a-zA-Z0-9\.\-_]+$`.
- Circular references are a risk for naive tooling; test your generator.

Verify: lint the document with your linter and confirm there are no unresolved refs, and that the bundled output has no remaining relative file refs.

## Checked
2026-11-08. Confirmed in the OpenAPI 3.1.0 specification (Components Object and Reference Object sections read in full; the Schema Object `example` text searched). The JSON Schema structuring page was dropped from sources (not read). Removed: the `redocly bundle` and lint commands, the `nullable`/type-array statement, the claim that 3.0 ignores `$ref` siblings, and the claim that circular refs are legal (none in the sources).
Method: documentation only; no commands were run.
