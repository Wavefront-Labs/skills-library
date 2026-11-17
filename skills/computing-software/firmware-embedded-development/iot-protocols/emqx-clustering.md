---
id: computing-software.firmware-embedded-development.iot-protocols.emqx-clustering
name: emqx-clustering
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [emqx-clustering, emqx-broker, emqx, cluster, core-replicant, iot-protocols]
level: practitioner
status: docs-checked
description: "EMQX clustering: Run EMQX as a cluster for capacity and availability."
sources:
  - https://docs.emqx.com/en/emqx/latest/deploy/cluster/introduction.html
  - https://docs.emqx.com/en/emqx/latest/admin/cli.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EMQX clustering

**Goal:** Run EMQX as a cluster for capacity and availability.

## Steps
1. Nodes use Erlang distribution and are named `<name>@<host>`; discovery strategies are manual, static, DNS (A and SRV records), etcd and k8s
2. EMQX 5.0 and later use Mria with a replication log (RLOG): core nodes handle writes and full replication, replicant nodes are read-only and handle client sessions
3. All nodes must share the same Erlang cookie (treat it as a secret)
4. Put a load balancer in front of the nodes; the EMQX docs have a separate cluster load balancing page
5. `emqx ctl cluster status` shows members (add `--json` for JSON output)
6. Keep inter-node latency under 10 ms; the docs say the cluster is not available above 100 ms; put core nodes in the same private network
7. The introduction page says clustering is available during a trial and then needs a commercial licence, and advises at most three nodes for the open-source edition: check the licence terms of your version

## Gotcha
Network partitions: cluster.autoheal (default true) isolates affected nodes and re-integrates them when the partition clears, and cluster.autoclean (default 24h) removes nodes that stay disconnected. Persistent sessions across nodes need clean_start false (MQTT 3.x) or clean_start false plus session_expiry_interval above 0 (MQTT 5.0).

## Verify
- [ ] cluster status lists all nodes
- [ ] Killing a node keeps clients reconnecting to others
- [ ] Session routing works across nodes

## Checked

2026-11-03. Confirmed in the EMQX Clustering introduction and the CLI page: discovery strategies, Mria core and replicant roles and RLOG, shared Erlang cookie, node naming, autoheal and autoclean settings and defaults, session persistence settings, latency requirements, licence and three-node note, and `emqx ctl cluster status [--json]`. Removed: LB ports and a /status health check, cluster linking across regions, and the instruction to open specific cluster ports (the page's port 4370 refers to pre-5.0 Mnesia clustering).
Method: documentation only; no commands were run.
