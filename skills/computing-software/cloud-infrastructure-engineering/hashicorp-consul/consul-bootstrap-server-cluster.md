---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-bootstrap-server-cluster
name: consul-bootstrap-server-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, bootstrap-expect, server-agent]
level: practitioner
status: docs-checked
description: "Start a Consul server set with bootstrap_expect so leader election happens once all servers are present, and avoid split clusters."
sources: ["https://developer.hashicorp.com/consul/docs/architecture/consensus", "https://developer.hashicorp.com/consul/docs/agent/config/config-files"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`bootstrap_expect` is the number of expected servers in the datacenter. Either omit it or give every server the same value; when set, Consul waits until that many servers are available and then bootstraps the cluster, so an initial leader is elected automatically. It requires the agent to run in server mode.

```hcl
server           = true
bootstrap_expect = 3
datacenter       = "dc1"
data_dir         = "/opt/consul"
retry_join       = ["10.0.0.11", "10.0.0.12", "10.0.0.13"]
```

Gotchas: at most one server per datacenter may run in `bootstrap` mode, which lets a server self-elect; more than one means consistency cannot be guaranteed, and the docs advise against the flag once a cluster has bootstrapped. `data_dir` must be durable across reboots (servers persist cluster state there) and must support filesystem locking, so some mounted folders are unsuitable.

Verify: after all three start, `consul members` lists the three servers and `consul operator raft list-peers` shows one leader and two followers.

## Checked

2026-11-03. Confirmed against the agent bootstrap options page (bootstrap_expect, bootstrap), the general options page (data_dir durability and file locking, retry_join on the join page) and the consul members and operator raft command pages. Removed: the two-clusters claim, the tmpfs advice and the `consul info` check, which the pages do not state.

Method: documentation only; no commands were run.
