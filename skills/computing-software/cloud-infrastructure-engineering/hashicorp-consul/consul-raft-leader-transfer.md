---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-raft-leader-transfer
name: consul-raft-leader-transfer
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, leader-transfer, transfer-leader, rolling-restart]
level: practitioner
status: docs-checked
description: "Move the Raft leader to another server with consul operator raft transfer-leader instead of restarting the leader node."
sources: ["https://developer.hashicorp.com/consul/commands/operator/raft"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`consul operator raft transfer-leader` transfers Raft leadership to another server agent. The page says to use it to change leadership without restarting the leader node, which maintains quorum and workload capacity.

```sh
consul operator raft list-peers
consul operator raft transfer-leader -id=<server-node-id>
consul operator raft list-peers
```

- `-id`: node ID of the Raft peer to receive leadership. If empty, leadership goes to a random server agent.
- ACL: `operator:write`. The return code indicates success or failure.
- `list-peers` (ACL `none`) shows Node, ID, Address, State, Voter, RaftProtocol, Commit Index and "Trails Leader By" per server; use that column to pick a follower that is not lagging and to check the result.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source (commands/operator/raft): `transfer-leader` purpose, `-id` and random default, `operator:write`, `list-peers` output columns. Removed: unsupported claims about lagging followers delaying commits, failure domains, three-server quorum arithmetic, and the `kv put` Verify step.
Method: documentation only; no commands were run.
