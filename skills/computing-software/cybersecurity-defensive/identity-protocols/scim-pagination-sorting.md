---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-pagination-sorting
name: scim-pagination-sorting
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-pagination-sorting, scim-filtering-paging, pagination, startindex, count, totalresults, itemsperpage, sortby, sortorder, identity-protocols]
level: practitioner
status: docs-checked
description: "Page SCIM lists with 1-based startIndex and count, read totalResults and itemsPerPage, sort with sortBy and sortOrder, and avoid skipped records."
sources:
  - https://www.rfc-editor.org/rfc/rfc7644#section-3.4.2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pagination and sorting (startIndex and count)

Goal: enumerate large directories reliably.

Request: `GET /Users?startIndex=1&count=100&sortBy=userName&sortOrder=ascending`. `startIndex` is 1-based (a value below 1 is read as 1). `count` is the desired maximum per page (a negative value is read as 0). The response is a ListResponse: `schemas:["urn:ietf:params:scim:api:messages:2.0:ListResponse"]`, `totalResults`, `startIndex`, `itemsPerPage`, `Resources`. To continue, set `startIndex` past the last returned item (the RFC example: after 10 results with `startIndex=1`, request `startIndex=11`).

Gotchas:
- `count=0` returns no resources except `totalResults`.
- The server MUST NOT return more than `count`, though it MAY return fewer; if `count` is unspecified the server sets the maximum.
- Pagination is not stateful: clients MUST be prepared for inconsistent results, because resources can change between requests.
- `sortOrder` defaults to ascending when `sortBy` is given. Sorting is optional (`sort.supported`). The server caps results per response via `filter.maxResults`.

Verify: page through a list that changes mid-scan and dedupe by id.

## Checked
2026-11-02. Confirmed against RFC 7644 sections 3.4.2.3 and 3.4.2.4 (Tables 6 and 7, Figure 3) and RFC 7643 section 5. Removed: the "loop until startIndex + itemsPerPage > totalResults" termination rule, the "order by a stable attribute" advice, and the "pagination hints" wording, none of which the RFCs state.
Method: documentation only; no commands were run.
