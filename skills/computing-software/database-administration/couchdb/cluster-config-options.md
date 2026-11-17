---
id: computing-software.database-administration.couchdb.cluster-config-options
name: cluster-config-options
category: computing-software
field: database-administration
product: couchdb
tags: [cluster, config, q-n, placement, seedlist, reconnect-interval]
level: practitioner
status: docs-checked
description: "The [cluster] settings q, n, placement, seedlist and reconnect_interval_sec, with defaults and the n values the setup wizard assigns."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/cluster.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All in the `[cluster]` section:

- `q`: default shards for new databases. Default `2`. For a few large, heavily accessed databases, or many CPU cores, consider `4` or `8`. Can be overridden per database at creation.
- `n`: replicas of each document. CouchDB places only one replica per node. The setup wizard gives a single node `n = 1`, two nodes `n = 2`, larger clusters `n = 3`. Do not set it above 3.
- `placement`: comma-delimited `zone_name:#` list (such as `metro-dc-a:2,metro-dc-b:1`). Overrides `n`. Not set by default.
- `seedlist`: comma-delimited node names to contact when joining a cluster. With a seedlist, `/_up` returns 404 until the node has reached one member and replicated up-to-date `_nodes`, `_dbs` and `_users`.
- `reconnect_interval_sec` (added 3.3): how often to try reconnecting to disconnected nodes; 25% random jitter applies.

```ini
[cluster]
q = 2
n = 3
seedlist = couchdb@node1.example.com,couchdb@node2.example.com
```

## Checked

2026-11-04. Confirmed against the CouchDB config/cluster page ([cluster]): q default 2 and the 4 or 8 advice, n and the wizard values, do-not-exceed-3 advice, placement format and override of n, seedlist with the _up 404 behaviour, reconnect_interval_sec jitter. Nothing removed.

Method: documentation only; no commands were run.
