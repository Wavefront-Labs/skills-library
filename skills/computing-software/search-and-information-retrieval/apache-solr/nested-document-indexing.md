---
id: computing-software.search-and-information-retrieval.apache-solr.nested-document-indexing
name: nested-document-indexing
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [nested-documents, nest-path, child-documents, root-field, nest-parent]
level: advanced
status: docs-checked
description: "Index nested parent and child documents in Solr with _nest_path_, _root_ and _nest_parent_, avoid anonymous children, and prepare for block join queries and the child transformer."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/indexing-nested-documents.html
  - https://solr.apache.org/guide/solr/latest/indexing-guide/partial-document-updates.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nested-document-indexing

Nested documents bind a root document to children (for example a product with SKUs and manuals). The top-most parent is the root document. Indexed relationships usually query much faster than query-time joins.

Schema pieces:
- Define `_nest_path_` as `<fieldType name="_nest_path_" class="solr.NestPathField"/>` plus a matching field. It lets the `[child]` transformer rebuild the nesting; without it children come back as a flat list.
- Optionally define `_nest_parent_` (string, indexed, stored) to keep parent ids.
- Without `_nest_path_`, give every document a field that lets a filter isolate parents.

Send children as named keys inside the parent JSON. Indexing children anonymously with `_childDocuments_` works but is not recommended.

SolrCloud: all documents of a block live on one shard, routed by the root id. When updating a child, send `_route_` with the root id or use compositeId prefix routing, and put the root id in `_root_`.

Search with the block join parsers and attach results with `[child]`.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Indexing Nested Documents and Partial Document Updates pages: root document and speed versus query-time joins, `NestPathField` and the flat-list behaviour without it, `_nest_parent_` definition, `_childDocuments_` being not recommended, routing child updates by root id with `_route_` or compositeId prefixes, and `_root_` on child updates. Removed the claim that anonymous children must not be used with `_nest_path_`, which the pages do not state.

Method: documentation only; no commands were run.
