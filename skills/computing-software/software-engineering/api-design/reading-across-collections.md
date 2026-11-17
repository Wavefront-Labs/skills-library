---
id: computing-software.software-engineering.api-design.reading-across-collections
name: reading-across-collections
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, aip-159, reading-across-collections, wildcard-parent, list-filtering, resource-names]
level: practitioner
status: docs-checked
description: "List child resources across all parents with AIP-159 wildcard parents (publishers/-/books) and report unreachable parents per AIP-217."
sources: ["https://google.aip.dev/159", "https://google.aip.dev/217"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading across collections (AIP-159)

Nested collections (`/projects/{p}/tasks`) force clients to loop over every parent to find "all my open tasks". AIP-159 lets a service accept a wildcard `-` (hyphen) as the parent in a standard List method:

```
GET /v1/projects/-/tasks?filter=...
```
(Google's own example is `GET /v1/publishers/-/books?filter=...`; the filter expression here is illustrative.)

## Rules (AIP-159)
- Support is optional ("APIs may"), and the method must explicitly document that it is supported.
- The URI pattern must still be specified with `*` and permit the collection to be specified; a pattern must not hard-code the `-` character.
- Resources in the response must use their **canonical name** with the real parent identifiers (`projects/p3/tasks/t9`), never `projects/-/...`.
- List across collections may be offered whether or not child identifiers are unique. Services must not support it on Get requests if child resources might collide. If a child ID is unique across parents, a Get with `-` as the parent (`GET .../publishers/-/books/{book}`) may be allowed, and the response still carries the canonical name.
- Cross-parent requests should not support `order_by`; if they do, the field must document that ordering is best effort, because cross-parent requests make ordering ambiguous, especially when a parent is hard to reach.

## Unreachable parents (AIP-217)
If listing across parents can partly fail (for example a location is down), the response must say so rather than silently omit data:
- The response message includes a `repeated string unreachable` field (should be named `unreachable`), annotated `UNORDERED_LIST` field behavior.
- It holds service-relative resource names (for example `projects/example123/locations/us-east1`), not full names, URIs or bare IDs, and may mix locations and individual resources.
- The response must not carry other information about why they were unreachable. The service must let the caller make a more specific request (for example a Get or List on the unreachable parent) to receive an error with details, and must allow repeating the call with more restrictive parameters.
- If one unreachable parent means no data can be returned by definition (listing under a single unreachable parent), fail the whole request with an error.
- On paged calls, name unreachable resources on each page that meets them, and document a maximum number of names per response.
- Existing APIs that return an error by default must keep that default and add a `bool return_partial_success` request field together with `unreachable` in the response. Setting it to true when the request scope is finer than the API can report on should return `INVALID_ARGUMENT`.
- Clients must surface the unreachable list to users.

## When not to
If the cross-parent query is a reporting need, offer an export or a search endpoint instead of forcing it through List.

## Checked
2026-11-08. Read in full: AIP-159 and AIP-217 (google.aip.dev). Corrected: the draft said only List accepts `-` (AIP-159 allows Get when IDs are unique) and that pagination should order by a global key (AIP-159 says order_by should not be supported or is best effort). Removed unsupported claims: Search accepts `-`, authorization filtering and ACL joins, index design, tenancy behaviour, and the third source AIP-122 (not read for this skill).
Method: documentation only; no commands were run.
