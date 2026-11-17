---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-raft-remove-peer
name: consul-raft-remove-peer
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, raft-remove-peer, force-leave, remove-peer]
level: practitioner
status: docs-checked
description: "Remove failed Consul servers via consul force-leave and consul operator raft remove-peer, choosing the right one for the situation."
sources: ["https://developer.hashicorp.com/consul/commands/operator/raft", "https://developer.hashicorp.com/consul/commands/force-leave"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A dead server left in the Raft configuration still affects quorum. Prefer `force-leave` when the node still shows in `consul members`; use `remove-peer` for the rare case of a peer left behind in Raft although the server is no longer known to the cluster.

```sh
consul members
consul force-leave ec2-001-staging                 # failed node -> left
consul force-leave -prune ec2-001-staging          # remove from the member list entirely (1.6.2+)
consul force-leave server1.us-east1                # from a WAN pool: [node-name].[datacenter]
consul operator raft list-peers
consul operator raft remove-peer -address="10.0.0.15:8300"   # or -id=<server id>
```

- `force-leave` forces a failed or non-gracefully stopped member into the `left` state. Consul reaps `failed` nodes after 72 hours by default. For a server, the leader eventually removes it from the Raft configuration. Options: `-prune`, `-wan` (WAN pool only). ACL: `operator:write`.
- `remove-peer` takes `-address` ("IP:port", port usually 8300) or `-id`. ACL: `operator:write`. The return code shows success or failure.

Gotchas:
- `force-leave` takes full effect only if the target agent has shut down permanently. A live, reachable agent stays in the member list and Raft configuration, and an agent that returns after becoming `left` but before reaping rejoins the cluster.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: commands/force-leave (states, 72 hours, flags, WAN naming, ACL) and commands/operator/raft (`remove-peer`, `list-peers`). Removed: the `grep` pipe, the quorum-risk and Autopilot remarks, and the Verify step.
Method: documentation only; no commands were run.
