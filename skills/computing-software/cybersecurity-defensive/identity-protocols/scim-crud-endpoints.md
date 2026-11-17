---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-crud-endpoints
name: scim-crud-endpoints
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-crud-endpoints, scim-protocol-crud, scim, crud, post, put, delete, status-codes, application/scim+json, location, identity-protocols]
level: practitioner
status: docs-checked
description: "Use /Users and /Groups with POST, GET, PUT, PATCH and DELETE, correct 201, 200, 204, 409 and 404 responses, Location header and content type."
sources:
  - https://www.rfc-editor.org/rfc/rfc7644
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCIM endpoints, methods and status codes

Goal: implement or call SCIM correctly.

- Content type `application/scim+json`; the RFC notes some implementations informally use `application/json`.
- `POST /Users` creates: 201 with the resource in the body, a `Location` header and `meta.location`; 409 with `scimType` `uniqueness` on a conflict such as a duplicate `userName`.
- `GET /Users/{id}`: 200 or 404. `GET /Users?filter=...` returns a ListResponse.
- `PUT /Users/{id}` replaces the resource and must not be used to create one; success is 200 with the whole resource. Omitted `readWrite` attributes may be cleared or defaulted by the server; send `null` or `[]` to clear explicitly.
- `PATCH /Users/{id}` partial update (servers SHOULD support it); 200 with the resource, or 204 unless `attributes` was requested (then 200).
- `DELETE /Users/{id}`: 204. A server may not delete permanently but MUST return 404 for later operations on that resource.
- `/Me` aliases the authenticated subject (optional; servers may answer 501 or redirect with 308).

Gotchas:
- A deleted user's `userName` SHOULD NOT cause a 409 on a later create.
- `id` is issued by the server and must be stable and non-reassignable.
- Failed PUT or PATCH on a missing resource returns 404 (PUT never creates).

Verify: create, read, update, delete a user with curl and confirm each status code.

## Checked
2026-11-02. Confirmed against RFC 7644 sections 3.1, 3.3, 3.5.1, 3.5.2, 3.6, 3.11, 3.12 and 8.1 and RFC 7643 section 3.1. Removed: `active:false` as a general practice, the "POST may return 201 even if retries duplicate" gotcha, and "servers usually accept application/json".
Method: documentation only; no commands were run.
