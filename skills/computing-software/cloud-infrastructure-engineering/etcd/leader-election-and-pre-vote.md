---
id: computing-software.cloud-infrastructure-engineering.etcd.leader-election-and-pre-vote
name: leader-election-and-pre-vote
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [raft, leader-election, pre-vote, term, move-leader, heartbeat, election, consensus]
level: advanced
status: docs-checked
description: "How etcd elects a leader with Raft: heartbeats, election timeout and what happens to writes during an election."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/failures/"
  - "https://etcd.io/docs/v3.5/tuning/"
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
  - "https://etcd.io/docs/v3.5/faq/"
  - "https://etcd.io/docs/v3.5/learning/api/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

etcd replicates a log with Raft. At any time one member is the leader and handles all writes; others are followers.

Mechanics:

- The leader sends heartbeats every `--heartbeat-interval` (default 100 ms).
- A follower that goes an election timeout (`--election-timeout`, default 1000 ms) without hearing a heartbeat attempts to become leader itself.
- During a leader election the cluster cannot process any writes; write requests sent during the election are queued until a new leader is elected.
- Writes already sent to the old leader but not yet committed may be lost: the new leader can rewrite uncommitted entries, so some writes may time out after an election. No committed writes are ever lost.
- Applications can use `Raft_Term` to detect when the cluster completes a new leader election.

Slow disks, CPU starvation or a slow network can cause the leader to miss heartbeats and trigger spurious elections; see the tuning skill for the FAQ's `failed to send out heartbeat on time` diagnosis.

## Checked

2026-11-03. Confirmed on the v3.5 failure modes page: no writes processed during leader election and queued requests, uncommitted writes may be lost while committed writes never are. Confirmed on the tuning page: heartbeat interval 100 ms and election timeout 1000 ms defaults, followers attempt to become leader after missing heartbeats. Confirmed on the API page: Raft_Term detects a completed election. Removed: randomised timeout range, --pre-vote and its default, MoveLeader and etcdctl move-leader, the endpoint status and metric hints, and the term-increment/majority-vote description, none of which appear on the fetched pages. The skill name keeps pre-vote for id stability.

Method: documentation only; no commands were run.
