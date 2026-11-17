---
id: computing-software.database-administration.dragonfly.dflycluster-config-push
name: dflycluster-config-push
category: computing-software
field: database-administration
product: dragonfly
tags: [dflycluster-config, dflycluster-myid, slot-ranges, cluster-mode]
level: advanced
status: docs-checked
description: "Collect node IDs with DFLYCLUSTER MYID and push an identical JSON topology to every Dragonfly cluster node with DFLYCLUSTER CONFIG."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/cluster-mode.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run on the admin port of each node.

1. `DFLYCLUSTER MYID` on each node returns its unique ID.
2. Build the configuration, a JSON array with one entry per primary:

```json
[
  {
    "slot_ranges": [ { "start": 0, "end": 8191 } ],
    "master": { "id": "...", "ip": "...", "port": "..." },
    "replicas": [ { "id": "...", "ip": "...", "port": "..." } ]
  }
]
```

`ip` and `port` are what clients should use to reach the node. The docs example splits slots 0-8191 and 8192-16383 across two masters with one replica each.

3. Send the same string to **all nodes** with `DFLYCLUSTER CONFIG`. It takes a JSON-encoded string parameter.

Rules:

- Nodes do not verify each other's config, so every node must receive identical configuration.
- Resend the configuration after a restart and on any change (adding or removing nodes, changing hostnames).
- Once configured, a node handles only its slots; keys it does not own are deleted.
- The repository script `tools/cluster_mgr.py` is cited as a reference for local setup.

## Checked

2026-11-04. Confirmed in the Cluster Mode page (MYID, CONFIG with a JSON-encoded string, configuration format and example slot split, identical config on all nodes, resend after restart, key deletion, `cluster_mgr.py`). Nothing removed.

Method: documentation only; no commands were run.
