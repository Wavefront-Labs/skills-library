---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-patch-filter-paths
name: scim-patch-filter-paths
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-patch-filter-paths, scim-patch, patch-path, value-filter, emails, sub-attribute, urn-path, members, identity-protocols]
level: advanced
status: docs-checked
description: "Target a single multi-valued entry with path filters like emails[type eq \"work\"].value, sub-attribute paths and extension URN paths."
sources:
  - https://www.rfc-editor.org/rfc/rfc7644#section-3.5.2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PATCH paths with value filters and sub-attributes

Goal: edit one element without replacing the list.

Examples:
- `emails[type eq "work"].value` replace: changes only the sub-attribute of matching records.
- `members[value eq "2819c223-7f76-453a-919d-413861904646"]` remove: removes the matching member.
- `name.givenName` replace.
- `urn:ietf:params:scim:schemas:extension:enterprise:2.0:User:manager` replace with `{"value": "<id>"}`; a replace on a complex attribute leaves unspecified sub-attributes unchanged.
- `replace` with a `valuePath` filter that matches nothing: 400 with `scimType` `noTarget`.

Gotchas:
- In JSON, escape the quotes inside a path string: `"path":"members[value eq \"<id>\"]"`.
- A `replace` on a path that does not exist is treated as `add`.
- Removing a required or read-only attribute returns `mutability`.
- The path grammar is `attrPath / valuePath [subAttr]`; SCIM PATCH does not support array indexing.

Verify: patch work email, leave home email unchanged.

## Checked
2026-11-02. Confirmed against RFC 7644 sections 3.5.2 (paths, Figures 7 and 8, remove and replace rules) and 3.12. Removed: "filter no match with add adds the element", "filters only support attribute comparison", "servers implement filters unevenly", and `invalidValue` for removing a required attribute (RFC says `mutability`).
Method: documentation only; no commands were run.
