---
id: computing-software.search-and-information-retrieval.apache-solr.shard-splitting
name: shard-splitting
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [shard-split, splitshard, shard-splitting, hash-ranges, split-key, shard-management]
level: advanced
status: docs-checked
description: "Split a SolrCloud shard online with SPLITSHARD: hash-range halves, ranges, split.key, numSubShards, splitMethod rewrite or link, splitByPrefix, disk space needs and async."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/shard-management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# shard-splitting

`/admin/collections?action=SPLITSHARD&collection=techproducts&shard=shard1` (v2: `POST /api/collections/techproducts/shards` with `{"split":{"shard":"shard1"}}`).

Behavior:
- Splits one shard into two new shards by dividing the hash range into equal partitions; the parent keeps its data but re-routes requests to the sub-shards. No downtime; the shard keeps accepting queries and indexing during the split.
- New shards get as many replicas, of the same types, as the parent.
- A soft commit is issued automatically, so no explicit commit is needed.
- Only for collections created with `numShards` (hash-based routing).
- With `splitMethod=rewrite` (default), the parent leader's node needs more than twice the index size in free disk.
- Run it with `async` to avoid timeouts.

Controls:
- `ranges`: comma-separated hex ranges, for example `0-1f4,1f5-3e8,3e9-5dc`, for uneven splits.
- `split.key`: isolate a route key in its own sub-shard; `shard` is then optional.
- `numSubShards` (not with `ranges` or `split.key`), `splitFuzz` (below 0.5) to vary range sizes, `splitByPrefix` to pick split points from compositeId prefix distribution.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Shard Management page (SPLITSHARD): the v1 and v2 request forms, two equal hash-range partitions, no downtime, replicas of the same types, automatic soft commit, `numShards` collections only, `splitMethod` rewrite (default) and link, more than twice the index size free for rewrite, `async`, `ranges`, `split.key`, `numSubShards`, and the fuzz limit below 0.5. Corrected the fuzz parameter name to `splitFuzz`, the name on the page.

Method: documentation only; no commands were run.
