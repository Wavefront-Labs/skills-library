---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.write-alias-rollover
name: write-alias-rollover
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, write-alias-rollover]
level: advanced
status: docs-checked
description: "Use is_write_index and the rollover API with conditions to cycle indices behind an alias."
sources:
  - https://www.elastic.co/docs/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-without-data-streams
  - https://www.elastic.co/docs/manage-data/data-store/aliases
  - https://www.elastic.co/docs/manage-data/lifecycle/index-lifecycle-management/rollover
  - https://www.elastic.co/docs/reference/elasticsearch/index-lifecycle-actions/ilm-rollover
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Write alias and rollover

**Goal:** time- or size-based index rotation without data streams.
- Bootstrap an initial index and make it the write index: `PUT logs-000001 {"aliases":{"logs":{"is_write_index":true}}}`. Its name must match the template's index pattern and end with a number; on rollover that number is incremented to name the new index.
- `POST logs/_rollover {"conditions":{"max_age":"7d","max_docs":10000000,"max_primary_shard_size":"50gb"}}` (the ILM `rollover` action accepts `max_age`, `max_docs` and `max_primary_shard_size`; the manual API's condition list was not in the pages read). In the ILM tutorial, rollover creates the next numbered index, makes it the write index and makes the previous one read-only.
- `is_write_index` makes Elasticsearch route write requests for the alias to that index; an alias pointing at several indices without it rejects writes, and an alias that points to one index without it treats that index as the write index. Send writes to the alias.
- Automate with ILM (see the ILM skills): set `index.lifecycle.name` and `index.lifecycle.rollover_alias` in the index template. Do not also put the same alias in the template's `aliases` section (duplicate alias error). Data streams are recommended for new projects.
- Failure mode: an index name that does not match `^.*-\d+` fails the ILM rollover action; more than one write index for an alias is an error.

## Verify
- [ ] After rollover `GET logs/_alias` shows the new index as write index.

## Scope
The Elasticsearch documentation was checked; OpenSearch (ISM) behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch docs pages ILM tutorial without data streams, Aliases, Rollover, Fix ILM errors and the rollover action reference. Confirmed: all statements above except as noted. Removed: "condition names vary by version", "bootstrapping an alias name that equals an existing index name" (not stated), and the OpenSearch ISM reference and source root.

Method: documentation only; no commands were run.
