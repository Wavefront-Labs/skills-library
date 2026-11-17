---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-patch-operations
name: scim-patch-operations
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-patch-operations, scim-patch, patchop, add, remove, replace, operations, path, identity-protocols]
level: practitioner
status: docs-checked
description: "Build PATCH bodies with schemas PatchOp and Operations array: op add/remove/replace, path, value, and the rules per attribute type."
sources:
  - https://www.rfc-editor.org/rfc/rfc7644#section-3.5.2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PATCH add, remove and replace semantics

Goal: change only what you mean.

Body: `{"schemas":["urn:ietf:params:scim:api:messages:2.0:PatchOp"],"Operations":[{"op":"replace","path":"active","value":false},{"op":"add","path":"emails","value":[{"value":"a@example.com","type":"work"}]},{"op":"remove","path":"phoneNumbers[type eq \"fax\"]"}]}`.
Rules: `op` is `add`, `remove` or `replace`. `add` on a single-valued attribute replaces the value, on a multi-valued attribute adds a new value, and on a missing attribute adds it. `replace` on a multi-valued attribute without a filter replaces all values; with a `valuePath` filter it replaces the matching records. `remove` requires a `path` (otherwise 400 `noTarget`); with a path to a multi-valued attribute and no filter it removes all values. For `add` and `replace`, `path` is optional and `value` then holds the attributes. Operations are applied in order and the request is atomic: if one fails, the original resource is restored.

Gotchas:
- Setting a value's `primary` to true makes the server reset `primary` to false on the others.
- Group membership: `add` to `members` adds a value; `replace` on `members` replaces the whole list; adding an existing member changes nothing and succeeds.
- Groups can be very large, so RFC 7644 recommends PATCH support to avoid sending the whole resource.
- Success is 200 with the resource, or 204; 200 is mandatory if `attributes` was given.

Verify: patch a multi-valued attribute and GET the result.

## Checked
2026-11-02. Confirmed against RFC 7644 sections 3.5 and 3.5.2 (3.5.2.1 to 3.5.2.3). Removed: "op should be lowercase but tolerate Add/Replace" (the RFC lists only the three lowercase values and says nothing about tolerance).
Method: documentation only; no commands were run.
