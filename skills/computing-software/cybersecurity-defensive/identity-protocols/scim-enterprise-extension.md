---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-enterprise-extension
name: scim-enterprise-extension
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-enterprise-extension, scim-schema, enterprise-user, extension, custom-schema, manager, employeenumber, urn, identity-protocols]
level: advanced
status: docs-checked
description: "Add attributes with the enterprise extension (employeeNumber, department, manager) or custom schema URNs and declare them in schemas and /Schemas."
sources:
  - https://www.rfc-editor.org/rfc/rfc7643
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enterprise User extension and custom schemas

Goal: carry HR attributes through SCIM.

Method: list the URN in `schemas` and nest the attributes under it:
`"schemas": ["urn:ietf:params:scim:schemas:core:2.0:User", "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"]`, with `"urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {"employeeNumber": "...", "costCenter": "...", "organization": "...", "division": "...", "department": "...", "manager": {"value": "<user id>", "$ref": "...", "displayName": "..."}}`.
A custom extension is declared like the enterprise one: its URN is a `Schema` resource `id` returned from `/Schemas`, and it is listed under `schemaExtensions` (with `required` true or false) on the resource type from `/ResourceTypes`.

Gotchas:
- PATCH paths for extension attributes are prefixed with the schema URN, for example `urn:ietf:params:scim:schemas:extension:enterprise:2.0:User:employeeNumber`; adding such an attribute also adds the URN to `schemas`.
- `manager.value` is the `id` of the manager's SCIM User, not an employee number; `manager.displayName` is readOnly.
- If an extension is `required: true` for the resource type, every resource of that type must include it and its required attributes.

Verify: POST with the extension and confirm it is returned in GET.

## Checked
2026-11-02. Confirmed against RFC 7643 sections 4.3, 6 and 7 and RFC 7644 section 3.5.2. Removed: the claim that `urn:ietf:params:scim:schemas:extension:<org>:2.0:User` is a reserved style and the advice to use `urn:example:...`, and the "make them optional" advice, which the RFC does not state as such.
Method: documentation only; no commands were run.
