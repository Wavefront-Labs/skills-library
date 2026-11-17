---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-raft-peer-recovery
name: consul-raft-peer-recovery
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, raft-recovery, peers-json, outage-recovery]
level: advanced
status: docs-checked
description: "Restore Consul leadership after losing quorum using the peers.json manual recovery, when no usable backup exists."
sources: ["https://developer.hashicorp.com/consul/tutorials/operate-consul/recovery-outage", "https://developer.hashicorp.com/consul/commands/operator/raft"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Losing a majority of servers leaves no leader ("No cluster leader" errors on Raft calls). The tutorial says the fastest and easiest recovery is to build a fresh cluster and restore a backup from the old one; use `peers.json` only when no backup is available or it is corrupted. Recovery is possible from a single surviving server, which need not be the leader. It most likely involves data loss that did not reach the survivor, and it implicitly commits all outstanding Raft log entries, so data that was uncommitted before the failure may be committed.

`peers.json` lists the servers that should form the cluster. Consul reads it at startup, then deletes it. Place it in the `raft` folder of the data directory (for `data_dir = "/opt/consul"`: `/opt/consul/raft/peers.json`) on each surviving server, make it readable by the user Consul runs as, then start the server.

```json
[
  { "id": "<node-id>", "address": "10.0.4.155:8300", "non_voter": false }
]
```

- `id` (required): the node ID, from the logs at startup or the `node-id` file in the data directory.
- `address` (required): the server's IP and RPC port.
- `non_voter` (default false): used in some advanced Autopilot configurations.

Gotchas:
- If you have more than one survivor, include all of them.
- Do not list servers you lost and plan to redeploy with empty state: the server logs "recovery failed: refused to recover cluster with no initial state, this is probably an operator error" and exits with code 1.
- Success shows as "found peers.json file, recovering Raft configuration..." followed by "deleted peers.json file after successful recovery".
- Afterwards, `consul operator raft list-peers` (ACL `none`; `-stale=true` works without a leader) shows the Raft configuration.

## Checked

2026-11-03. Confirmed against the Consul tutorial "Recover from a Consul server outage" (data-loss note, single-survivor recovery, file location, fields and defaults, log lines, empty-state error) and commands/operator/raft (`list-peers`, `-stale`). Removed: the claim that every server must be stopped with identical file content, the advice to copy the raft directory first, the stale-server warning, the claim that `node-id` is the only ID source, and the Verify step; none are stated on the pages read.
Method: documentation only; no commands were run.
