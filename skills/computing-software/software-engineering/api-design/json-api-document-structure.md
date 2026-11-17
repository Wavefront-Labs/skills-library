---
id: computing-software.software-engineering.api-design.json-api-document-structure
name: json-api-document-structure
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, json-api, jsonapi, resource-objects, relationships, included, sparse-fieldsets, media-type]
level: practitioner
status: docs-checked
description: "Build JSON:API 1.1 documents: resource objects, relationships, compound documents, links, errors, the media type and status codes."
sources: ["https://jsonapi.org/format/", "https://jsonapi.org/recommendations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON:API document structure

Media type: `application/vnd.api+json` (clients must not add parameters other than the registered `ext` and `profile`). Servers answer 415 for bad Content-Type parameters and 406 for bad Accept.

## Resource document
```json
{
  "data": {
    "type": "articles",
    "id": "1",
    "attributes": { "title": "Hello" },
    "relationships": {
      "author": { "links": { "related": "/articles/1/author" }, "data": { "type": "people", "id": "9" } }
    },
    "links": { "self": "/articles/1" }
  },
  "included": [ { "type": "people", "id": "9", "attributes": { "name": "Dana" } } ]
}
```
- Every resource has `type` and `id` (id optional only when a client creates a new resource).
- Top level must contain `data`, `errors` or `meta`; `data` and `errors` never coexist.
- Query parameters are reserved: `include=author,comments.author`, `fields[articles]=title`, `sort=-created,title`, `page[...]`, `filter[...]` (filter semantics are left open).
- Create: `POST` returns `201` and should include a `Location` header (which must match `links.self` if both are present); `204` with no body is allowed if the server changed nothing about the resource. Update with `PATCH`; omitted attributes keep their current values (never read as null). Delete returns `200` with a document or `204`.
- Errors: `{"errors":[{"status":"422","source":{"pointer":"/data/attributes/title"},"title":"Invalid"}]}`.

## Gotchas
- Same-named fields across attributes and relationships are not allowed; `type` and `id` cannot be attribute names.
- Compound documents must have full linkage: included resources must be reachable from primary data.
- The spec reserves the `page` and `filter` query parameter families but does not define a pagination strategy or filtering syntax; document yours.
- `included` must not hold two resource objects with the same `type` and `id`, and must be absent when there is no top-level `data`.
- With `include=comments.author`, intermediate resources (the comments) must come back too, to keep full linkage.

Verify: use a library test helper and check `GET /articles?include=author&fields[articles]=title` returns only requested fields and an `included` array.

## Checked
2026-11-08. Confirmed in the jsonapi.org format page (searched by section, not read end to end): media type parameters and 415, `data`/`errors` not coexisting, full linkage, no duplicate type/id in `included`, `include` as comma and dot separated paths, reserved `page` and `filter` families, 201/Location, 204 rules, PATCH omitted-attribute rule. Recommendations page not re-read beyond a phrase check. Removed the unverified suggestion to validate against a JSON Schema. Corrected Location (SHOULD) and delete status (200 or 204).
Method: documentation only; no commands were run.
