---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-error-handling
name: scim-error-handling
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-error-handling, scim-protocol-crud, scim-error, scimtype, invalidfilter, uniqueness, mutability, invalidpath, toomany, identity-protocols]
level: practitioner
status: docs-checked
description: "Return SCIM errors with schema urn:ietf:params:scim:api:messages:2.0:Error, status as a string, scimType (invalidFilter, uniqueness, mutability, invalidValue) and detail."
sources:
  - https://www.rfc-editor.org/rfc/rfc7644
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCIM error responses and scimType

Goal: give clients actionable failures.

Body: `{"schemas":["urn:ietf:params:scim:api:messages:2.0:Error"],"status":"409","scimType":"uniqueness","detail":"..."}`. `status` is the HTTP status as a JSON string (required); `scimType` and `detail` are optional.
`scimType` values listed for 400 responses: `invalidFilter`, `tooMany`, `uniqueness`, `mutability`, `invalidSyntax`, `invalidPath`, `noTarget`, `invalidValue`, `invalidVers` (the requested SCIM protocol version is not supported), `sensitive` (personal information in a request URI). A duplicate on POST uses 409 with `uniqueness`.
Other codes in the RFC table: 307, 308, 401 (authorization header invalid or missing), 403, 404, 409 (version mismatch or duplicate), 412 (resource changed on the server), 413 (bulk limits), 500, 501.

Gotchas:
- `invalidFilter` also applies to a filter comparison the server does not support, such as `gt` on a Boolean.
- A PATCH remove of a required or read-only attribute returns `mutability`; a replace whose filter matches nothing returns 400 `noTarget`.
- PUT is not an upsert (RFC 7644 3.5.1): do not create on a missing id.

Verify: send an invalid filter and confirm scimType invalidFilter.

## Checked
2026-11-02. Confirmed against RFC 7644 sections 3.3, 3.5.1, 3.5.2, 3.12 (Tables 8 and 9). Removed: `Retry-After`, 429 and 503 (not in the RFC), the incorrect 403 for `sensitive` and the incorrect use of `invalidVers` for ETag mismatch, the client retry policy, and the "do not leak internals" advice.
Method: documentation only; no commands were run.
