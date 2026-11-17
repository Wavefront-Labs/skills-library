---
id: computing-software.search-and-information-retrieval.qdrant.consistency-guarantees
name: consistency-guarantees
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [consistency, write-ordering, write-consistency-factor, majority]
level: advanced
status: docs-checked
description: "Tune write and read consistency with write_consistency_factor, the consistency read parameter and write ordering."
sources:
  - "https://qdrant.tech/documentation/scaling/consistency-guarantees/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

In a replicated collection, you decide how many replicas must agree.

Writes:

- `write_consistency_factor` on the collection sets how many replicas must confirm a write (default 1).
- The `ordering` request parameter chooses `weak` (the default), `medium` or `strong`. Medium serializes writes through a dynamically elected leader; strong uses the permanent leader, giving strong consistency, but writes may be unavailable if the leader is down.

```http
PUT /collections/{collection_name}/points?ordering=strong&wait=true
```

Reads:

- `consistency` accepts `all`, `majority`, `quorum`, or a number of replicas to query. The default is 1.

```http
POST /collections/{collection_name}/points/query?consistency=majority
```

The `X-Qdrant-Route-Affinity` header (v1.19.0) pins every request carrying the same stable value, such as a user or session ID, to the same replica, so repeated reads stay stable without a multi-replica consistency read.

The docs say the read consistency option is preferred when updates are frequent and the number of replicas is low, and that writes fail if fewer than `write_consistency_factor` replicas are active.

## Checked

2026-11-03. Confirmed on the Qdrant consistency-guarantees page: `write_consistency_factor` default of 1, `ordering` values and semantics, read `consistency` values and default, the route-affinity header. Removed the unconfirmed latency and replication-factor advice.

Method: documentation only; no commands were run.
