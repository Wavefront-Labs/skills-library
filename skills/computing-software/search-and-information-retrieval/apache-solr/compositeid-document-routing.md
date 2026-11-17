---
id: computing-software.search-and-information-retrieval.apache-solr.compositeid-document-routing
name: compositeid-document-routing
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [doc-routing, document-routing, compositeid-router, route-parameter, shard-key, implicit-router]
level: advanced
status: docs-checked
description: "Route documents to shards in SolrCloud with the compositeId router: shard_key!doc_id prefixes, /num bits, _route_ at query time, and the implicit router with router.field."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/solrcloud-shards-indexing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# compositeid-document-routing

`compositeId` is the default router. A prefix in the document id sets the hash, so documents with the same prefix land on the same shard.

- Two routing levels are supported in the prefix.
- `shard_key/num!document_id` uses `num` bits of the shard key hash. `IBM/3!12345` takes 3 bits from the key and 29 from the id, spreading that tenant over 1/8 of the shards.
- At query time pass the prefix, with its bit count, in `_route_`, for example `q=solr&_route_=IBM/3!`, to query only those shards.

`implicit` router, chosen at collection creation: define `router.field`, and a field in each document identifies its shard. You manage which shards exist.

Use routing to co-locate a tenant's documents; the guide notes this may improve query performance by avoiding queries to every shard. SPLITSHARD with `split.key` can isolate a route key later.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide SolrCloud Shards and Indexing and Shard Management pages: compositeId as default router, the prefix and `!` rule, up to 2 routing levels, `/num` bits with the `IBM/3!12345` example, `_route_` with and without bits, the implicit router with `router.field`, and `split.key`. Removed the collapse and join co-location claim and the tenant skew warning, which the pages do not state.

Method: documentation only; no commands were run.
