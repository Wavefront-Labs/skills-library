---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-raft-quorum-sizing
name: consul-raft-quorum-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, raft-quorum, consul-servers, fault-tolerance]
level: practitioner
status: docs-checked
description: "Choose 3 or 5 Consul servers by quorum maths, see why even counts add no tolerance, and spread servers across availability zones."
sources: ["https://developer.hashicorp.com/consul/docs/concept/consensus", "https://developer.hashicorp.com/consul/docs/concept/reliability", "https://developer.hashicorp.com/consul/commands/operator/autopilot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Only Consul server nodes are in the Raft peer set; client agents are not, so a group of servers can support thousands of clients without scale affecting Raft performance. Quorum for `N` servers is at least `(N/2)+1`, and without a quorum no new logs can be committed.

| Servers | Quorum | Fault tolerance |
|---|---|---|
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 2 | 1 |
| 4 | 3 | 1 |
| 5 | 3 | 2 |
| 6 | 4 | 2 |
| 7 | 4 | 3 |

HashiCorp recommends 3 or 5 voting servers for production, and a single-server datacenter only for development. Four servers tolerate the same single failure as three.

```sh
consul operator raft list-peers
consul operator autopilot state
```

- Spread voting servers across 3 availability zones where you can; with 5 servers, limit each zone to 2 so that losing a zone still leaves a quorum of 3.
- Consul Enterprise redundancy zones improve fault tolerance without increasing the number of voting servers.
- When quorum is lost, it is impossible to process log entries or reason about peer membership, and re-establishing a leader typically needs manual intervention (see `consul-raft-peer-recovery`).
- `autopilot state` reports "Failure Tolerance" and the voters; `list-peers` shows each server's State and Voter columns.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: concept/consensus (peer set, quorum formula, quorum loss), concept/reliability and its quorum table (3 or 5 recommendation, zones), commands/operator/autopilot and operator/raft (output fields). Removed: the claim that each extra voter raises write latency beyond 5 servers, the rule about never taking two of three servers offline together as stated, and the Verify step with exact `FailureTolerance` values.
Method: documentation only; no commands were run.
