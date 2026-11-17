---
id: computing-software.software-engineering.api-design.hypermedia-links-and-link-header
name: hypermedia-links-and-link-header
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, rest, hateoas, link-header, rfc-8288, hypermedia, pagination-links]
level: practitioner
status: docs-checked
description: "Add hypermedia links (RFC 8288 Link header or HAL-style _links) for pagination, related resources and available actions, at the level of HATEOAS that pays off."
sources: ["https://www.rfc-editor.org/rfc/rfc8288", "https://datatracker.ietf.org/doc/html/draft-kelly-json-hal", "https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hypermedia links (HATEOAS / Link header)

**Pragmatic goal:** clients follow server-provided URLs for navigation (next page, related
resource, action) instead of building them, so the server can change URL shapes.

## Link header (RFC 8288)
```
Link: <https://api.example.com/items?cursor=abc>; rel="next",
      <https://api.example.com/items>; rel="first"
```
- Pagination rels used by GitHub's REST API: `prev`, `next`, `first`, `last`; it omits `prev` on the first page and `last` when it cannot be calculated.
- Relation types are either registered names or extension relation types, which RFC 8288 requires to be URIs.
- Parse the header with a library rather than a regex.

## In-body links (HAL style)
```json
{"id": "o1", "status": "pending",
 "_links": {"self": {"href": "/orders/o1"},
            "cancel": {"href": "/orders/o1/cancel"},
            "customer": {"href": "/customers/c7"}}}
```
HAL (draft-kelly-json-hal) puts links under `_links`, each with an `href`; the HTTP method is not part of HAL, so document it per relation.
Action links only present when allowed (no `cancel` once shipped) let UIs drive buttons from
the server's state machine instead of duplicating rules.

## How far to go
Full HATEOAS (clients discover everything from the root) is rarely realised: generated SDKs
hard-code paths anyway. Worth doing: pagination links, `self`, related-resource links, and
state-dependent action links. Skip: link relations for every field, custom hypermedia formats.

## Gotchas
- Behind proxies, emit URLs with the public scheme and host (or documented relative links).
- Links must carry the same filter/sort parameters as the current request.
- Don't make clients depend on a `last` link you can't compute cheaply with cursors (GitHub omits it when it cannot be calculated).

## Checked
2026-11-01. Confirmed: RFC 8288 extension relation types are URIs; GitHub pagination docs (Link header rels prev/next/first/last, omitted when unavailable); HAL draft `_links`/`href`. Removed: registered-rel list including deprecation/sunset, CORS and HEAD claims, library names, HAL `method` key, X-Forwarded header names.
Method: documentation only; no commands were run.
