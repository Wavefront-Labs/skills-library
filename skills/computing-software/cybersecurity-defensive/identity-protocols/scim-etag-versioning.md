---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-etag-versioning
name: scim-etag-versioning
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-etag-versioning, scim-protocol-crud, etag, if-match, meta.version, 412, optimistic-locking, if-none-match, identity-protocols]
level: advanced
status: docs-checked
description: "Prevent lost updates in SCIM with meta.version ETags, If-Match on PUT, PATCH and DELETE, 412 responses and If-None-Match on GET."
sources:
  - https://www.rfc-editor.org/rfc/rfc7644
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ETags and optimistic concurrency

Goal: safe concurrent edits.

Method: servers that report `etag.supported: true` in ServiceProviderConfig return the ETag in the HTTP header and in `meta.version` (a weak ETag such as `W/"3694e05e9dff590"`; a non-strong validator MUST be marked weak). Clients MAY send `If-Match: W/"..."` on PUT and PATCH so the operation succeeds only if the ETag matches the latest resource; the RFC's DELETE example also sends `If-Match`. A failed precondition is 412 Precondition Failed ("Resource has changed on the server"). `If-None-Match` on GET returns an empty 304 when the resource is unchanged.

Gotchas:
- `invalidVers` is about an unsupported SCIM protocol version, not an ETag mismatch.
- ETag support is optional; check `etag.supported`.

Verify: run two updates from the same version and confirm the second gets 412.

## Checked
2026-11-02. Confirmed against RFC 7644 sections 3.12 (Table 8), 3.14, 3.5.2 and 3.6 examples, and RFC 7643 sections 3.1 (`meta.version`) and 5 (`etag`). Removed: the `invalidVers` hint for 412 (wrong), "version changes on group membership changes", and the PATCH fallback advice.
Method: documentation only; no commands were run.
