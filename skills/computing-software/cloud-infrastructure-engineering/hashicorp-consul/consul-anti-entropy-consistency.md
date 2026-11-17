---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-anti-entropy-consistency
name: consul-anti-entropy-consistency
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, anti-entropy, consistency-modes, stale-reads]
level: practitioner
status: docs-checked
description: "Know how Consul agents reconcile local and catalog state, and pick default, consistent or stale read modes for each use case."
sources: ["https://developer.hashicorp.com/consul/docs/concept/consistency", "https://developer.hashicorp.com/consul/api-docs/features/consistency"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The agent's local state is authoritative: agents forward service and check changes to the leader, which updates the catalog and replicates it to the other servers. Anti-entropy periodically syncs local agent state with the catalog, which also lets Consul re-populate the catalog after complete data loss. If agent and catalog differ, the agent's view wins.

Approximate periodic sync interval by cluster size (each agent picks a random staggered start within the window):

| Nodes | Interval |
|---|---|
| 1 - 128 | 1 minute |
| 129 - 256 | 2 minutes |
| 257 - 512 | 3 minutes |
| 513 - 1024 | 4 minutes |

Sync failures (agent misconfiguration, environment misconfiguration, I/O problems such as a full disk or permissions, networking problems) are logged and the agent keeps running; later syncs recover from transient failures.

Read modes (HTTP API query parameter):
- `default` (`leader`): requests go to the leader using leader leasing. If an election happens before the lease window ends, the old leader may serve stale reads in rare cases.
- `consistent` (`?consistent`): the leader verifies with a quorum of peers that it is still leader. Results are always consistent, at the cost of extra traffic and latency. Most clients should not use it unless they cannot tolerate a stale read.
- `stale` (`?stale`): any server answers, including without a leader during an outage. Reads are faster and more scalable but more likely to be stale. Consul DNS queries use `stale` by default.

```sh
curl -s 'localhost:8500/v1/catalog/service/web?stale'
curl -s 'localhost:8500/v1/catalog/service/web?consistent'
```

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: concept/consistency (authoritative agent state, sync table, failure causes, three modes) and api-docs/features/consistency (query parameters, DNS default). Fixed: the old text gave the sync interval as "about a minute up to several minutes"; the table is now exact. Removed: the claim that direct catalog API edits to agent-owned services get reverted, the advice on ACL or network causes of persistent errors, and the Verify step.
Method: documentation only; no commands were run.
