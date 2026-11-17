---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-interop-troubleshooting
name: scim-interop-troubleshooting
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-interop-troubleshooting, scim-operations-security, troubleshooting, provisioning-logs, attribute-mapping, conflict, identity-protocols]
level: practitioner
status: docs-checked
description: "Diagnose failing SCIM provisioning against RFC 7643/7644: 409 uniqueness, scimType errors, userName and externalId rules, filters and ListResponse."
sources:
  - https://www.rfc-editor.org/rfc/rfc7644
  - https://www.rfc-editor.org/rfc/rfc7643
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCIM provisioning troubleshooting

Goal: find why users do not sync, by comparing the client's request and your response with the RFCs.

Steps:
1. Reproduce with curl against the endpoint using the same token. `GET /ServiceProviderConfig` describes the features the service provider supports, including its `filter` capability (RFC 7644 sections 3.4.2.2 and 4).
2. Read the IdP provisioning log for the request body and the response; compare the HTTP status and the `scimType` in the error body (RFC 7644 section 3.12). Error types for status 400 include `invalidFilter`, `tooMany`, `uniqueness`, `mutability` and `invalidSyntax`.
3. Check the mapped attributes: a User MUST include a non-empty `userName`, which MUST be unique across all of the service provider's Users, is case insensitive and is REQUIRED (RFC 7643 section 4.1.1).
4. 409 on create: RFC 7644 section 3.3 requires 409 with `scimType` `uniqueness` for a conflict such as a duplicate `userName`. Match or merge the earlier record. RFC 7644 section 3.6 says a deleted resource SHOULD NOT count in conflict calculation, so a create reusing a deleted user's `userName` should not fail with 409.
5. `externalId` is issued by the provisioning client and the server does not enforce its uniqueness (RFC 7643 section 3.1); a filter on `externalId` is how a client can locate its own resources.
6. Filter probes: a filter the server cannot parse or support should return 400 `invalidFilter`; one that yields far too many results may return 400 `tooMany` (RFC 7644 section 3.4.2.1). A query with no match must return 200 with `totalResults` 0, and unrecognised query parameters SHOULD be ignored rather than rejected.
7. Pagination: `totalResults` can exceed the number of resources in the page; `startIndex` is 1-based and `startIndex` and `itemsPerPage` are required when partial results are returned (RFC 7644 section 3.4.2).

Gotchas:
- Responses use the media type `application/scim+json`.
- Vendor-specific behaviour (test connection, quarantine, retry timing, scoping filters) is documented by each IdP, not by the RFCs; read the vendor's provisioning docs for it.

Verify: provision one test user and trace the request and response against the rules above.

## Checked

2026-11-09. Read RFC 7644 sections 3.3, 3.4.2 (incl. 3.4.2.1, 3.4.2.2), 3.6, 3.12 and 4, and RFC 7643 sections 3.1 and 4.1.1. Removed: quarantine, test-connection, initial-cycle timing, slow group lookup and IdP scoping-filter claims (vendor behaviour, not stated in the sources), and the RFC 7642 source (not read).
Method: documentation only; no commands were run.
