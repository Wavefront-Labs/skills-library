---
id: computing-software.search-and-information-retrieval.apache-solr.collapse-expand
name: collapse-expand
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [collapse-grouping, collapse-expand, collapsing-qparser, result-grouping, group-head, nullpolicy]
level: advanced
status: docs-checked
description: "Collapse Solr results to one document per group with the collapse post filter, then fetch group members with expand: field, min, max, sort, nullPolicy, hint."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/collapse-and-expand-results.html
  - https://solr.apache.org/guide/solr/latest/query-guide/result-grouping.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# collapse-expand

`fq={!collapse field=group_field}` is a post filter that keeps one document per group. The response format is normal; faceting, highlighting and elevation see only the collapsed set. The collapse field must be a single-valued string, int or float field.

Options: `min`/`max` (field or function) or `sort` choose the group head (at most one of the three; default is highest score); `nullPolicy` handles documents without a value; `hint=top_fc` (string fields only) or `hint=block` (when group values are contiguous blocks, such as `_root_`) for speed.

`expand=true` returns other group members in an `expanded` section, tuned with `expand.rows`, `expand.sort`, `expand.q`, `expand.fq`.

Collapsing runs per shard, not across shards, so co-locate documents of a group with routing. Collapse and expand cannot be used together with result grouping (`group=true`).

Result Grouping (`group.field`, `group.query`, `group.limit`, `group.ngroups`, `group.facet`) is distributed-safe but the guide says collapse and expand is preferable in most cases.

## Checked

2026-11-04. Confirmed against the Collapse and Expand Results page: post filter behaviour, options, `top_fc` and `block` hints, per-shard collapsing, not supported with result grouping, preference over grouping. Nothing removed.

Method: documentation only; no commands were run.
