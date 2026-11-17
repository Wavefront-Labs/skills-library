---
id: computing-software.software-engineering.api-design.openapi-oneof-and-discriminator
name: openapi-oneof-and-discriminator
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, openapi, oneof-discriminator, polymorphism, discriminator, anyof, allof, json-schema]
level: practitioner
status: docs-checked
description: "Model polymorphic payloads in OpenAPI with oneOf, allOf and the discriminator object, including mapping values and the generator pitfalls."
sources: ["https://spec.openapis.org/oas/v3.1.0", "https://json-schema.org/understanding-json-schema/reference/combining"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# oneOf, allOf and `discriminator`

## Pattern: tagged union
```yaml
components:
  schemas:
    Pet:
      oneOf:
        - $ref: '#/components/schemas/Cat'
        - $ref: '#/components/schemas/Dog'
      discriminator:
        propertyName: petType
        mapping:
          cat: '#/components/schemas/Cat'
          dog: '#/components/schemas/Dog'
    Base:
      type: object
      required: [petType]
      properties: { petType: { type: string } }
    Cat:
      allOf:
        - $ref: '#/components/schemas/Base'
        - type: object
          properties: { lives: { type: integer } }
```
`oneOf` means the data must validate against exactly one subschema; `anyOf` against one or more; `allOf` against all of them. JSON Schema's own docs warn that `allOf` is not object-oriented inheritance: each instance must independently be valid against every `allOf` subschema.

## Rules and gotchas
- `propertyName` is required; that property must be present in the payload. The discriminator is legal only next to `oneOf`, `anyOf` or `allOf`, and inline schemas are not considered, so list `$ref` schemas.
- All possible schemas must be listed explicitly in `oneOf`/`anyOf`. To avoid repeating the discriminator, it may sit on a parent schema that the others compose with `allOf`.
- Without `mapping`, the value must equal the component schema name; add a `mapping` (values are schema names or references) to decouple wire values from schema names. Mapping keys are strings.
- If the value matches no implicit or explicit mapping, no schema can be determined and validation should fail.
- With `oneOf`, the spec describes the discriminator as a hint that can shortcut validation and schema selection; with `anyOf` it can remove ambiguity when several schemas fit one payload. A payload matching two `oneOf` branches fails plain `oneOf` validation, so make branches distinguishable.
- Test the generated client round trip for each branch before committing to a shape (generator behaviour varies; this skill did not verify any generator).

Verify: validate one sample per branch plus one invalid sample with a JSON Schema validator and confirm only the invalid one fails, then regenerate your SDK and deserialise each sample.

## Checked
2026-11-08. Confirmed in the OpenAPI 3.1.0 specification (Discriminator Object section read in full; the rest of the page searched) and the JSON Schema "combining" page (`allOf`, `anyOf`, `oneOf` semantics, `allOf` is not inheritance). Removed: the claim that selected schemas must declare the property required (the spec's example does, but does not require it), the `const` suggestion, and the statement that many generators handle `oneOf` poorly (not in the sources).
Method: documentation only; no commands were run.
