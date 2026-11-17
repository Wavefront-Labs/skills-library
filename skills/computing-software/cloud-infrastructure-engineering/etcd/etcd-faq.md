---
id: computing-software.cloud-infrastructure-engineering.etcd.etcd-faq
name: etcd-faq
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [faq, cluster-size, odd-members, latency, sizing, network, questions]
level: intro
status: docs-checked
description: "Short answers from the etcd FAQ: why odd cluster sizes, how many members, write latency, and the role of the leader."
sources:
  - "https://etcd.io/docs/v3.5/faq/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Answers from the FAQ page.

Cluster size: an etcd cluster needs a majority of nodes, a quorum, to agree on updates. For n members quorum is (n/2)+1. Odd sizes are recommended because an odd-size cluster tolerates the same number of failures as the even size above it with fewer nodes (a 4-member cluster tolerates 1 failure, like 3). The cluster should probably have no more than seven nodes; 5 members tolerate two failures, which is enough in most cases.

Why not more nodes: larger clusters give better fault tolerance, but write performance suffers because data must be replicated across more machines.

Failure handling: etcd operates as long as a member quorum can be established. After a transient partition it resumes automatically once quorum is restored. For power loss it replays the persisted Raft log. A permanently failed node can be removed through runtime reconfiguration.

Leader: Raft is leader-based and the leader handles all client requests that need consensus. A client need not know which node is the leader: such requests sent to a follower are forwarded to the leader, and requests that do not need consensus (for example serialized reads) can be served by any member.

Performance depends strongly on disk performance (SSD is highly recommended; fio can assess a disk) and on network latency between members. Across regions, the default heartbeat and election settings may cause frequent elections, so tune them for high latency.

When replacing a node, remove the unhealthy member first and then add its replacement.

## Checked

2026-11-08. Read in full: etcd v3.5 FAQ page. Confirmed quorum formula, odd-size rationale, seven-node guidance, forwarding to the leader, disk and cross-region latency notes and the remove-before-add rule. Removed: the claim that quorum loss stops linearizable reads, the rolling-upgrade statement and the zone-spreading recommendation (not on the page).
Method: documentation only; no commands were run.
