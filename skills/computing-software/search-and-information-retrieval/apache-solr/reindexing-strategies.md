---
id: computing-software.search-and-information-retrieval.apache-solr.reindexing-strategies
name: reindexing-strategies
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [reindexing, reindex-collection, schema-change, major-upgrade, delete-by-query]
level: advanced
status: docs-checked
description: "Decide when a Solr change requires reindexing and how to do it safely: delete everything and verify no segments remain, or reindex to a new collection and switch an alias."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/reindexing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# reindexing-strategies

Reindex means delete the existing index and re-ingest the whole corpus from the system of record. Lucene has no schema; Solr's schema is only a rulebook applied at index time, so existing documents never change.

Reindex after: changing field or field type properties; changing the index-time analysis chain (a query-only analyzer change needs none); changing `luceneMatchVersion`, `codecFactory` or update request processors; upgrading to a new major version. Request handler, search component, node and replica changes, and shard splits do not need it.

Strategies:
1. Delete all with `{"delete":{"query":"*:*"}}` to `/update`, then confirm index segments are gone in every shard and replica (a zero document count is not enough), then re-ingest.
2. SolrCloud only: index into a new collection with the new schema, then point an alias at it and later delete the old collection. This allows rollback. If all fields are stored, `REINDEXCOLLECTION` can copy data across.

An index first written by a Solr version more than one major version older cannot be opened.

## Checked

Checked 2026-11-09 against the full Reindexing page of the Solr Reference Guide: changes that require reindexing, upgrades, delete-all and new-collection strategies, changes that do not need it. The collection-management source was not read and was dropped.

Method: docs-checked 2026-11-09 against the Reindexing page (raw ref-guide source); no commands were run.
