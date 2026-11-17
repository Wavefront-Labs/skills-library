---
id: computing-software.messaging-and-integration.nats.jetstream-cluster-administration
name: jetstream-cluster-administration
category: computing-software
field: messaging-and-integration
product: nats
tags: [jetstream-cluster, raft, replicas, stream-report, step-down, meta-group]
level: practitioner
status: docs-checked
description: "Operate a JetStream cluster: replicated streams (1, 3 or 5), stream report, leader step-down, and the server report jetstream meta group view."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/clustering/jetstream_clustering/administration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: create replicated streams and inspect/steer RAFT leadership in a JetStream cluster.

Account level:
- Create with replicas: `nats stream add ORDERS --replicas 3`. The docs suggest 1, 3 or 5 replicas. Stream info then shows cluster name, leader and replicas with `current, seen N s ago`; `current` means the follower is caught up. The replica count can be edited later.
- Placement and health overview: `nats stream report` lists consumers, messages, bytes, storage, lost, deleted and the node list with the leader marked by an asterisk.
- Planned leader change: `nats stream cluster step-down ORDERS` (and `nats consumer cluster step-down ORDERS NEW` for a consumer). Elections cause short interruptions, so do them at a convenient time. Stepping down does not remove the node or stop it from becoming leader again.

System level (system account user): `nats server report jetstream --user admin --password <password>` gives a cluster-wide summary (streams, consumers, messages, memory, file, API requests and errors) plus the RAFT Meta Group table with Leader, Current, Offline, Active and Lag. Limit it with `--account`. A peer that is not current, offline with growing Active time and lag signals trouble.

Gotchas: system users can see the meta group but not individual streams or consumers; avoid passing real passwords on a shared shell history.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
