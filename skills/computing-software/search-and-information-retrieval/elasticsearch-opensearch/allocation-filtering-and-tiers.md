---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.allocation-filtering-and-tiers
name: allocation-filtering-and-tiers
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, allocation-filtering-and-tiers, es-allocation]
level: advanced
status: docs-checked
description: "Place shards on specific nodes with allocation filters, drain a node, and use Elasticsearch data tier preference."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings
  - https://www.elastic.co/docs/reference/elasticsearch/index-settings/shard-allocation
  - https://www.elastic.co/docs/manage-data/lifecycle/data-tiers
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings
  - https://docs.opensearch.org/latest/install-and-configure/configuring-opensearch/cluster-settings/
  - https://docs.opensearch.org/latest/api-reference/cat/cat-allocation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Allocation filtering and data tiers

**Goal:** place shards on specific hardware.
- Drain a node: `PUT _cluster/settings {"persistent":{"cluster.routing.allocation.exclude._name":"node-3"}}`. Built-in attributes are `_name`, `_host_ip`, `_publish_ip`, `_ip`, `_host`, `_id` and `_tier`; wildcards are allowed in values.
- Per index, with a custom node attribute set in the node config (`node.attr.box_type: hot`): `PUT my-index/_settings {"index.routing.allocation.require.box_type": "hot"}`. The filter types are `include`, `exclude` and `require`.
- A node must satisfy all `require` filters, none of the `exclude` filters, and at least one `include` filter at the same time.
- Elasticsearch data tiers use the node roles `data_content`, `data_hot`, `data_warm`, `data_cold` and `data_frozen`. The index setting `index.routing.allocation.include._tier_preference` picks the tier (default `data_content`, or `data_hot` for new data stream indices) and accepts an ordered list such as `data_cold,data_warm,data_hot`.
- Remove the exclusion after maintenance by setting it to `null` through the cluster settings API; setting `_tier_preference` to `null` removes the tier preference and does not restore the default.
- Failure mode: conflicting rules (and a conflicting `_tier_preference`) can leave shards unassigned; use the cluster allocation explain API.

## Verify
- [ ] The node to retire reports zero shards in `GET _cat/allocation?v` (the `shards` column).

## Checked
Date: 2026-11-07
- Elasticsearch cluster-level shard allocation settings page, read from the filtering section to the end: persistent `exclude._ip` decommission example, `include`/`require`/`exclude.{{attribute}}`, built-in attribute list including `_name`, wildcard example.
- Elasticsearch index-level shard allocation page, read in full: `index.routing.allocation.include/require/exclude`, the three-rule combination text, `node.attr` custom attributes.
- Elasticsearch data tiers page, read in full: `_tier_preference` defaults, ordered list example, `null` behaviour, troubleshooting via the allocation explain API.
- Elasticsearch cluster update settings page (searched): "reset ... by assigning them a null value". `data_frozen` is confirmed as a node role in the allocation explain API role list, not on the data tiers page. OpenSearch cluster settings page (searched): `cluster.routing.allocation.include/require/exclude.<attribute>`; the tier content is Elasticsearch-only. `_cat/allocation`: OpenSearch page `GET /_cat/allocation?v` and Elasticsearch cat allocation page (`shards` column) read in part.
- Removed: the claim that the skill's tier text applies to OpenSearch; the `box_type` attribute is a placeholder custom attribute.
Method: documentation only; no commands were run.
