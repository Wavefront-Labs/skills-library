---
id: computing-software.messaging-and-integration.rabbitmq.cluster-formation
name: cluster-formation
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, cluster-formation, rmq-clustering]
level: advanced
status: docs-checked
description: "Form a RabbitMQ cluster using the same Erlang cookie, peer discovery or rabbitmqctl join_cluster, with an odd number of nodes."
sources:
  - https://www.rabbitmq.com/docs/cluster-formation
  - https://www.rabbitmq.com/docs/clustering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster formation

**Goal:** Build a stable multi-node cluster.

## Steps
1. Nodes must share the Erlang cookie and resolve each other's hostnames.
2. Join: `rabbitmqctl stop_app; rabbitmqctl join_cluster rabbit@node1; rabbitmqctl start_app`.
3. Prefer peer discovery (classic config file, pre-configured DNS records, AWS, Kubernetes, Consul or etcd backends) to manual joins.
4. Use an odd number of nodes (1, 3, 5, 7); two-node clusters are strongly discouraged. Clustering is designed for a LAN with sub-millisecond round-trip time, which remains the recommended model; stretching a cluster across data centers works but needs deliberate planning.

## Failure modes
- Every node must have the same Erlang cookie, which should be readable only by its owner (UNIX permissions `600` or similar).
- Hostname changes break the node name.

## Verify
- `rabbitmqctl cluster_status` lists all nodes as running.

## Checked

Date: 2026-11-02. Confirmed in the Clustering Guide (docs/clustering) and Cluster Formation guide (docs/cluster-formation): shared cookie, odd node counts, LAN design, peer discovery backends. Removed or corrected: "never stretch across a WAN" (the guide says it works with planning), the log wording for cookie mismatch, and the federation/shovel remark.

Method: documentation only; no commands were run.
