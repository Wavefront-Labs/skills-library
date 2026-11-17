---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-attribute-projection
name: scim-attribute-projection
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-attribute-projection, scim-filtering-paging, attributes, excludedattributes, projection, returned, search-post, payload-size, identity-protocols]
level: practitioner
status: docs-checked
description: "Reduce SCIM payloads with attributes and excludedAttributes, handle returned=always and request attributes, and the .search POST form."
sources:
  - https://www.rfc-editor.org/rfc/rfc7644#section-3.4.2
  - https://www.rfc-editor.org/rfc/rfc7643
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# attributes and excludedAttributes projection

Goal: fetch only what you need.

Method: `GET /Users?attributes=userName,emails.value` returns the minimum set of attributes plus those requested, overriding the default set. `excludedAttributes=groups,photos` returns the default set minus the listed attributes and has no effect on attributes whose schema `returned` setting is `always` (for example `id`). The two query parameters are mutually exclusive. Attributes with `returned: request` appear in a query only when named in `attributes`. The parameters apply to any operation that returns a resource, including single GET.

`POST /Users/.search` with a `SearchRequest` body (`schemas:["urn:ietf:params:scim:api:messages:2.0:SearchRequest"]`, `attributes`, `excludedAttributes`, `filter`, `sortBy`, `sortOrder`, `startIndex`, `count`) lets a client query without passing parameters on the URL.

Gotchas:
- A GET filter on personal data can leak through browser history and server logs; RFC 7644 says clients SHOULD query with POST in that case.
- `attributes` and `excludedAttributes` use standard attribute notation (for example `name.givenName`).

Verify: compare payload size with and without `excludedAttributes`.

## Checked
2026-11-02. Confirmed against RFC 7644 (3.4.2.5, 3.4.3, 3.9, 7.5.2) and RFC 7643 (2.2 `returned` keywords, 3.1 `id`). Removed: the claim that `schemas` is returned always (RFC names `id` only), the "large groups" advice, and the "exclude members" gotcha, which the RFCs do not state.
Method: documentation only; no commands were run.
