---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-service-provider-config
name: scim-service-provider-config
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-service-provider-config, scim-bulk-discovery, serviceproviderconfig, schemas, resourcetypes, discovery, capabilities, authenticationschemes, identity-protocols]
level: practitioner
status: docs-checked
description: "Discover server capabilities at /ServiceProviderConfig, /Schemas and /ResourceTypes: patch, bulk, filter, changePassword, sort, etag and authenticationSchemes."
sources:
  - https://www.rfc-editor.org/rfc/rfc7644
  - https://www.rfc-editor.org/rfc/rfc7643
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ServiceProviderConfig, Schemas and ResourceTypes

Goal: make a client adapt to the server.

- `GET /ServiceProviderConfig`: `patch.supported`, `bulk{supported,maxOperations,maxPayloadSize}`, `filter{supported,maxResults}`, `changePassword.supported`, `sort.supported`, `etag.supported`, `authenticationSchemes[{type,name,description,specUri,documentationUri}]` (`type` is `oauth`, `oauth2`, `oauthbearertoken`, `httpbasic` or `httpdigest`).
- `GET /ResourceTypes`: each type's `endpoint`, `schema` URN and `schemaExtensions`.
- `GET /Schemas` (and `/Schemas/<schema URI>`): all supported schemas with attribute definitions, including extensions.
The service provider SHOULD make `authenticationSchemes` publicly accessible without prior authentication, with appropriate security considerations.

Gotchas:
- Don't rely on a feature the server declares unsupported (for example PATCH).
- Query parameters such as filtering, sorting and pagination SHALL be ignored on `/Schemas` and `/ResourceTypes`; if a `filter` is supplied the server SHOULD answer 403.
- A single ResourceType or Schema is returned as one object; multiple come as a ListResponse.

Verify: fetch all three and compare to observed behaviour.

## Checked
2026-11-02. Confirmed against RFC 7644 section 4 and RFC 7643 sections 5 to 7. Removed: "these endpoints do not require a resource-specific permission", and "real servers often misreport" (not in the RFCs). The earlier source anchor `#section-3.7` was replaced by the whole RFC 7644.
Method: documentation only; no commands were run.
