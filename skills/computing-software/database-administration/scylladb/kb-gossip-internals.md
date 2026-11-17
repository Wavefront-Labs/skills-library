---
id: computing-software.database-administration.scylladb.kb-gossip-internals
name: kb-gossip-internals
category: computing-software
field: database-administration
product: scylladb
tags: [gossip, gossip-digest-syn, heart-beat-state, failure-detection, messaging-service]
level: advanced
status: docs-checked
description: "How ScyllaDB gossip works: once per second each node contacts 1 to 3 random peers, three-message rounds (syn, ack, ack2), heart_beat_state, application_state, shard 0."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/gossip.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gossip internals

ScyllaDB nodes exchange metadata about node identity and up/down state through a gossip protocol, so no single point of failure holds the cluster state. Each node runs gossip once per second, picking 1 to 3 random peers; runs are not synchronised across nodes. Traffic is small and infrequent.

One round is three messages (node A initiates, node B is the random peer):
1. A sends `gossip_digest_syn` (a digest summarising what A knows).
2. B sends `gossip_digest_ack`.
3. A sends `gossip_digest_ack2`.
These borrow names from TCP, but no new TCP connection is needed per round.

Contents exchanged: `heart_beat_state` (a generation number that increases each time the node starts, plus an ever-increasing version) and `application_state` (data on the status of components within the node, such as load, plus a version number). The digest design minimises data sent while resolving conflicts between the two nodes.

Implementation: gossip messages ride on the ScyllaDB `messaging_service` (Seastar RPC), along with mutations and streaming. Because each node is made of shared-nothing shards, gossip runs on CPU 0 only and its state is replicated to other shards.


## Checked

2026-11-04: gossip frequency, the three-message round, heart_beat_state, application_state, messaging_service and the CPU 0 note confirmed against the ScyllaDB gossip knowledge-base page. Removed the unsupported gossipinfo troubleshooting paragraph and the invented application_state key list.

Method: documentation only; no commands were run.
