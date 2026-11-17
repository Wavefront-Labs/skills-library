---
id: computing-software.messaging-and-integration.apache-zookeeper.zxid-and-zab-protocol
name: zxid-and-zab-protocol
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, zab, atomic-broadcast, zxid, epoch, quorum, leader-activation]
level: sme
status: docs-checked
description: "ZooKeeper atomic broadcast internals: zxid epoch/counter split, majority quorums, leader activation and active messaging phases, and how it differs from Paxos."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperInternals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zab internals

- Guarantees: reliable delivery, total order, causal order; assumes FIFO channels (TCP). Timeouts affect liveness only.
- zxid is 64 bits: high 32 bits epoch (changes per leader), low 32 bits counter incremented per proposal.
- Quorums are majorities (n/2+1); weighted and hierarchical quorums are supported.
- Phase 1, leader activation: FastLeaderElection picks a leader with the highest zxid among followers; leader syncs followers with missing proposals or a snapshot, discards uncommitted old-epoch proposals, proposes NEW_LEADER and serves only once it commits.
- Phase 2, active messaging: like two-phase commit without abort; leader sends proposals in order, followers persist and ack, leader sends COMMIT after a quorum.
- Not Multi-Paxos: no single-coordinator assumption, but requires strict cross-proposal FIFO.

Verify: after a leader change, new proposals carry a higher epoch (high 32 bits of the zxid) than before.

## Checked

Method: docs-checked 2026-11-09 against zookeeperInternals.html (full page read)
