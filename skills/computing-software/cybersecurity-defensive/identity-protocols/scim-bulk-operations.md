---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-bulk-operations
name: scim-bulk-operations
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-bulk-operations, scim-bulk-discovery, scim-bulk, bulkid, failonerrors, maxoperations, maxpayloadsize, bulkrequest, identity-protocols]
level: advanced
status: docs-checked
description: "Send many operations in one POST /Bulk request, cross-reference new resources with bulkId, honour failOnErrors, maxOperations and maxPayloadSize."
sources:
  - https://www.rfc-editor.org/rfc/rfc7644#section-3.7
  - https://www.rfc-editor.org/rfc/rfc7643
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bulk operations and bulkId references

Goal: provision in batches.

Request: `POST /Bulk` with `schemas:["urn:ietf:params:scim:api:messages:2.0:BulkRequest"]`, `failOnErrors: 2`, `Operations:[{"method":"POST","path":"/Users","bulkId":"qwerty","data":{...}},{"method":"POST","path":"/Groups","bulkId":"g1","data":{"members":[{"type":"User","value":"bulkId:qwerty"}]}}]`. `method` is POST, PUT, PATCH or DELETE; `bulkId` is required when `method` is POST; `path` is a resource type endpoint for POST and a specific resource for the others. The response (`BulkResponse`) lists per-operation `status`, `location` and the same `bulkId`. Without `failOnErrors` the server continues as far as it can and disregards partial failures; `failOnErrors` is the number of errors the server accepts before failing the remaining operations. Limits come from `bulk.maxOperations` and `bulk.maxPayloadSize` in ServiceProviderConfig.

Gotchas:
- The server replaces `bulkId:qwerty` with the permanent resource id once created. It MUST try to resolve circular cross-references but MAY stop and return 409.
- A server may reorder operations as long as the client's intent is preserved.
- Bulk is an optional feature; check `bulk.supported`.
- Exceeding either limit returns 413 and the error body names the limit exceeded.

Verify: send a bulk with one bad op and read statuses.

## Checked
2026-11-02. Confirmed against RFC 7644 section 3.7 (3.7.1 to 3.7.4) and RFC 7643 section 5 (`bulk`). Removed: "operations are not transactional" wording (replaced by the RFC's continue-on-error rule), "circular references fail" (RFC says MAY return 409), "resolves in order", and "many IdPs do not use Bulk".
Method: documentation only; no commands were run.
