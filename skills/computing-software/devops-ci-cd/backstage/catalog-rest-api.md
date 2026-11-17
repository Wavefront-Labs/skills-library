---
id: computing-software.devops-ci-cd.backstage.catalog-rest-api
name: catalog-rest-api
category: computing-software
field: devops-ci-cd
product: backstage
tags: [catalog-api, entities-by-query, entity-filters, backstage]
level: advanced
status: docs-checked
description: "Query catalog entities over HTTP with by-query filters, field selection, ordering and pagination."
sources:
  - https://backstage.io/docs/features/software-catalog/software-catalog-api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The catalog backend exposes a REST API at your `backend.baseUrl` plus `/api/catalog`, for example `http://localhost:7007/api/catalog/entities`. Some or all endpoints may accept or require an `Authorization` header with a Bearer token, which should be the Backstage token returned by the identity API.

Main endpoints:

- `GET /entities/by-query` for filtered, paged listing, with `filter`, `fields`, `orderField`, `limit`, `cursor` and full-text options. `POST /entities/by-query` accepts a filter predicate in the body.
- `GET /entities` is deprecated in favour of `GET /entities/by-query`, which has cursor-based pagination.
- `GET /entities/by-name/<kind>/<namespace>/<name>` to fetch one entity, and `/ancestry` to see where it came from.
- `GET /entities/by-uid/<uid>` and `DELETE /entities/by-uid/<uid>`.
- `POST /entities/by-refs` to fetch many by reference.
- `POST /refresh` to schedule a refresh, and `POST /validate-entity` to check a descriptor.
- `GET /locations`, `GET /locations/{id}` and related location routes.

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:7007/api/catalog/entities/by-query?filter=kind=component,spec.lifecycle=production&fields=metadata.name&limit=20"
```

Multiple `filter` parameters are ORed and comma-separated terms within one are ANDed. Use `fields` to trim payloads on large catalogs. The page itself notes that it describes only the commonly used parts of the API, and an OpenAPI spec exists for the full surface.

## Checked

2026-11-03. Confirmed on the Software Catalog API page: the endpoint list (by-query GET and POST, by-name with ancestry, by-uid GET and DELETE, by-refs, refresh, validate-entity, locations), the `orderField`, `fields` and `limit` parameters, filter-set semantics (conditions inside a set are ANDed, sets are ORed), the Bearer token note, the note that only commonly used parts are described, and that the page points to an OpenAPI spec. Fixed: the source URL was a 404 (now the software-catalog-api page); `GET /entities` is documented as deprecated, not merely older. Not run, the example curl uses a placeholder token.

Method: documentation only; no commands were run.
