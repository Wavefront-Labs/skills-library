---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-gossip-serf-pools
name: consul-gossip-serf-pools
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, serf-pools, serf, lifeguard, port-8301]
level: practitioner
status: docs-checked
description: "Know what Consul's LAN gossip pool (8301) and WAN pool (8302) do, how Lifeguard helps, and how gossip is secured."
sources: ["https://developer.hashicorp.com/consul/docs/concept/gossip", "https://developer.hashicorp.com/consul/docs/reference/architecture/ports", "https://developer.hashicorp.com/consul/commands/force-leave"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Consul uses Serf to manage membership and broadcast messages. There are two gossip pools:
- LAN pool: enabled by default and required. All nodes in a datacenter share membership information; Consul uses it to discover servers automatically and to distribute failure detection across the cluster. It also supports fast, reliable event broadcasts. Default port `8301`.
- WAN pool: extends gossip between a primary datacenter and secondary datacenters in a WAN-federated environment, so servers can make cross-datacenter requests. Default port `8302`.

Per the ports reference, 8301 and 8302 are both TCP and UDP.

```sh
consul members
consul members -wan
```

The Serf protocol assumes the local node is healthy. If the local node suffers CPU or network exhaustion, the `serfHealth` check can flip, causing false alarms and wasted diagnosis. Lifeguard addresses this (see the HashiCorp research paper "Lifeguard: SWIM-ing with Situational Awareness").

Gossip between agents in both pools is secured with a dedicated gossip encryption key; rotate it periodically with `consul keyring` (see `consul-gossip-encryption` and `consul-keyring-rotation`). In a WAN pool, a node is identified as `[node-name].[datacenter]` (used by `consul force-leave server1.us-east1`).

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: concept/gossip (pools, defaults, Lifeguard, key), reference/architecture/ports (8301/8302 TCP and UDP), commands/force-leave (WAN naming). Removed: the `consul info | grep` command, the claim that the WAN pool is servers only, firewall flapping remarks, and the Verify step.
Method: documentation only; no commands were run.
