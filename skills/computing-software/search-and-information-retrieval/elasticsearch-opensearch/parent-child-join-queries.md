---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.parent-child-join-queries
name: parent-child-join-queries
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, parent-child-join-queries]
level: advanced
status: docs-checked
description: "Model parent/child documents with the join field: mapping, mandatory routing, restrictions, global ordinals cost, and when to denormalize instead."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/parent-join
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parent-child join field

**Goal:** independently updatable child documents in one index, used only when denormalizing does not fit.
- Mapping: `"my_join_field":{"type":"join","relations":{"question":"answer"}}`. Multiple children: `"question":["answer","comment"]`. Parent documents are indexed with `"my_join_field":"question"`; children with `{"name":"answer","parent":"1"}`.
- Children must be on the parent's shard, so route them: `PUT my-index/_doc/3?routing=1`. The same routing is needed to get, delete or update a child. For a grandchild, route by the greatest ancestor (the grandparent).
- Restrictions: one join field mapping per index; an element has many children but one parent; you can add a new relation to an existing join field; you can add a child to an existing element only if that element is already a parent.
- Related queries and features: `has_child`, `has_parent`, `parent_id` (for example `{"parent_id":{"type":"answer","id":"1"}}`), the children aggregation, and inner hits. The join creates a field named like `my_join_field#question` holding the parent id, usable in aggregations and scripts.
- Cost: every join field, `has_child` or `has_parent` query adds significant query-time overhead and can trigger global ordinals. Elasticsearch says the join only makes sense for a one-to-many relation where one side greatly outnumbers the other (products and offers), and recommends denormalizing otherwise. Multiple relation levels are discouraged.
- Global ordinals are built eagerly on refresh by default, which can lengthen refresh. If the join field is used rarely and writes are frequent, set `"eager_global_ordinals":false` (then the first join query pays the rebuild latency).
- Check join heap with `GET _stats/fielddata?human&fields=my_join_field#question`.
- Failure mode: omitting `routing` on a child breaks the same-shard requirement.

## Verify
- [ ] `has_child` with a matching answer returns the parent question.
- [ ] `_search` hits for children show `_routing` equal to the parent id.

## Checked
2026-11-08. Confirmed against the Elasticsearch join field type page: mapping and indexing syntax, mandatory routing and grandchild routing, restrictions, `#` parent-id field, parent_id query example, performance warnings, global ordinals behaviour, `eager_global_ordinals`, fielddata stats command.
Removed: the claim that join queries are slower than nested (the page compares to denormalizing, not nested), the OpenSearch root source (OpenSearch join page returned no content), and unconfirmed-cluster boilerplate. OpenSearch behaviour was not checked here.
Method: documentation only; no commands were run.
