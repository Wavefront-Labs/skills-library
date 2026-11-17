---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-wan-federation
name: consul-wan-federation
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, wan-federation, federation, retry-join-wan]
level: practitioner
status: docs-checked
description: "Join Consul datacenters with consul join -wan or retry_join_wan, understand the primary datacenter, and open required ports."
sources: ["https://developer.hashicorp.com/consul/docs/architecture/gossip", "https://developer.hashicorp.com/consul/docs/agent/config/config-files"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
WAN federation joins datacenters so their servers can communicate. `primary_datacenter` designates the datacenter that is authoritative for ACL information, intentions and the service mesh root CA; all servers and datacenters must agree on it.

```hcl
retry_join_wan = ["10.1.0.11", "10.1.0.12"]
primary_datacenter = "dc1"
```

```sh
consul join -wan 10.1.0.11
consul members -wan
consul catalog datacenters
```

With traditional WAN federation the servers must be reachable over the WAN: WAN Serf on 8302 (TCP and UDP) and server RPC on 8300 (TCP). Secondary datacenters replicate ACL policies and roles by default; `acl.enable_token_replication` also replicates tokens (global tokens already in the secondary are lost), and `acl.tokens.replication` is the replication token.

Gotchas: `consul join -wan` and `consul members -wan` apply to agents in server mode. Gossip encryption uses a single key shared across the members of a datacenter. Mesh gateways are the alternative when exposing servers on the WAN is hard: WAN federation via mesh gateways (Consul 1.8.0 and later) only needs the gateways to be routable, and secondary servers must reach the primary's mesh gateways when they first start.

Verify: `consul catalog datacenters` lists both, and a cross-datacenter query `dig web.service.dc2.consul` works.

## Checked

2026-11-03. Confirmed against the WAN Federation Overview (traditional versus mesh gateway federation, requirements), the ports reference (8300 TCP, 8302 TCP and UDP), the general options page (primary_datacenter), the join options page (retry_join_wan), the ACL options page (token replication behaviour), the consul join and members pages (-wan) and the encryption overview (single gossip key per datacenter). Removed: the unique datacenter name rule, cross-datacenter gossip key and CA requirements, the token_ttl behaviour and the primary-change advice.

Method: documentation only; no commands were run.
