---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-attribute-characteristics
name: scim-attribute-characteristics
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-attribute-characteristics, scim-schema, scim, attribute-characteristics, mutability, returned, uniqueness, caseexact, multivalued, identity-protocols]
level: practitioner
status: docs-checked
description: "Interpret SCIM attribute definitions: type, multiValued, required, caseExact, mutability, returned, uniqueness and subAttributes."
sources:
  - https://www.rfc-editor.org/rfc/rfc7643
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCIM attribute characteristics

Goal: read a schema and implement attributes correctly.

- `type`: string, boolean, decimal, integer, dateTime, reference, complex (the Schema `type` keywords); binary is a core data type in RFC 7643 section 2.3.
- `multiValued`, `required`, `caseExact` (the server uses it when evaluating filters; `userName` is case insensitive in the core schema).
- `mutability`: `readOnly`, `readWrite` (default), `immutable` (may be set at creation or by PUT replacement, never updated after), `writeOnly` (such as `password`).
- `returned`: `always` (such as `id`), `never` (password), `default` (the default), `request` (returned in a query only when named in `attributes`).
- `uniqueness`: `none` (default), `server` (unique within the SCIM endpoint or tenancy), `global`.
- `referenceTypes` (a resource type name, `external` or `uri`), `canonicalValues` (suggested values).

Gotchas:
- The `password` attribute is `writeOnly` with `returned: never`; the server MUST NOT return it in any form.
- A PUT that includes a readOnly attribute has those values ignored, not rejected.
- `userName` is required, must be unique and is case insensitive, so duplicate detection must ignore case.

Verify: GET /Schemas and read the attributes for urn:ietf:params:scim:schemas:core:2.0:User.

## Checked
2026-11-02. Confirmed against RFC 7643 sections 2.2, 2.3, 4.1.1, 7 and RFC 7644 section 3.5.1. Removed: "Servers must never return password" as a standalone line (kept in the RFC's wording) and the unqualified "set at creation only" description of `immutable`.
Method: documentation only; no commands were run.
