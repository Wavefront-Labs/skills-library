---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-autopilot
name: consul-autopilot
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, consul-autopilot, autopilot-state, cleanup-dead-servers]
level: practitioner
status: docs-checked
description: "Tune Autopilot cleanup, stabilization time and health thresholds with consul operator autopilot, and read state for failure tolerance."
sources: ["https://developer.hashicorp.com/consul/commands/operator/autopilot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`consul operator autopilot` has three subcommands: `get-config`, `set-config` and `state`.

```sh
consul operator autopilot get-config
consul operator autopilot set-config -cleanup-dead-servers=true \
  -last-contact-threshold=200ms -max-trailing-logs=250 \
  -server-stabilization-time=10s -min-quorum=3
consul operator autopilot state -format=json
```

Options of `set-config`:
- `-cleanup-dead-servers`: automatically remove dead servers when new servers join successfully.
- `-last-contact-threshold`: longest a server may go without contact from the leader before it is unhealthy (a duration such as `200ms`).
- `-max-trailing-logs`: most log entries a server may trail the leader by before it is unhealthy.
- `-min-quorum`: minimum number of servers required before Autopilot may prune dead servers.
- `-server-stabilization-time`: how long a server must be healthy before it is added to the cluster (such as `10s`). It only takes effect if all servers run Raft protocol version 3 or higher.
- Enterprise only: `-disable-upgrade-migration`, `-redundancy-zone-tag`, `-upgrade-version-tag`.

`state` (`-format` is `pretty` or `json`) prints overall health, Failure Tolerance, Optimistic Failure Tolerance, the leader, voters, and per-server name, address, version, status, node type, last contact, term and index. ACL needed: `operator:read` for `get-config` and `state`, `operator:write` for `set-config`.

Gotchas:
- Strict thresholds can mark a healthy but briefly slow server unhealthy.
- With `-cleanup-dead-servers=true`, set `-min-quorum` so Autopilot cannot prune the cluster below the size you can tolerate.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source (commands/operator/autopilot): subcommands, flags, ACLs, Raft protocol note, state output fields and `-format`. Removed: the invented Verify step, the closing runbook paragraph, and the claim that thresholds plus cleanup remove a server (the page only says unhealthy).
Method: documentation only; no commands were run.
