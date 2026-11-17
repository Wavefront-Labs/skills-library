---
id: computing-software.cloud-infrastructure-engineering.zot.graphql-search-api
name: graphql-search-api
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, graphql, search-api, global-search, referrers-query, graphql-playground]
level: practitioner
status: docs-checked
description: "Query Zot's search extension over GraphQL at /v2/_zot/ext/search: supported queries, a curl call, paging arguments, and the debug-only playground."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/graphql.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Endpoint: POST `/v2/_zot/ext/search` with `Content-Type: application/json`. Requires the search extension. Replies are JSON. Send the query as the value of a `query` key in a JSON body:

```
curl -X POST -H "Content-Type: application/json" --data '{ "query": "{ ImageListForCVE (id:\"CVE-2002-1119\") { Results { Name Tags } } }" }' http://localhost:8080/v2/_zot/ext/search
```

Submit with curl or Postman to `http://localhost:8080/v2/_zot/ext/search`.

Queries (inputs): `ImageListForDigest` (digest), `ImageListForCVE` (CVE id), `CVEListForImage` (image), `ImageListWithCVEFixed` (repo or image, CVE id), `RepoListWithNewestImage`, `ExpandedRepoInfo` (repo), `ImageList` (repo), `GlobalSearch` (query), `DerivedImageList` and `BaseImageList` (image), `Image` (image), `Referrers` (repo, digest, type). The page table's spelling of two names differs from the samples, so follow the samples.

Paging: `requestedPage: {limit, offset, sortBy}`, for example `sortBy: SEVERITY` or `ALPHABETIC_ASC`.

Details on `Image`: `LastPullTimestamp` may be the sentinel `1970-01-01T00:00:00Z` when pull stats are unavailable; `IsDeletable` may be `null` when delete permission is not evaluated.

Playground: `/v2/_zot/debug/graphql-playground#`, only in a `binary-debug` build or with the `debug` label.

## Checked

Whole page skimmed for endpoint, query table, playground and Image field notes. Dropped the unsupported MetaDB label and added the JSON body form.

Method: docs-checked 2026-11-09 against zot docs articles/graphql.md.
