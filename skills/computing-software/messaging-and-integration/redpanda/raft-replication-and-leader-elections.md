---
id: computing-software.messaging-and-integration.redpanda.raft-replication-and-leader-elections
name: raft-replication-and-leader-elections
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [raft, replication, leader-election, quorum, heartbeat, partitions]
level: advanced
status: docs-checked
description: "How Redpanda partitions form Raft groups, how quorum commits relate to acks=all, and how heartbeats and election_timeout_ms drive elections."
sources:
  - https://docs.redpanda.com/streaming/current/get-started/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every Redpanda topic partition is its own Raft group: one elected leader plus zero or more followers, the number set by the topic's replication factor. A group tolerates f failures with 2f+1 nodes, so a five-node cluster with replication factor five stays fully operational if two nodes fail.

**Commit rule.** Raft is a majority vote. The leader makes an event available to consumers, and acknowledges it when `acks=all (-1)`, only after a majority of replicas have written it to their log. Because the leader needs only a quorum, a minority of slow replicas (gray failures) does not add latency for clients.

**Elections.**
- The leader sends a heartbeat to all followers every 150 ms.
- A follower that sees no heartbeat within the election timeout starts an election. The timeout is the `election_timeout_ms` cluster property, default 1500 ms.
- The candidate increments its term, votes for itself and asks the others for votes. It becomes leader on a majority, yields to a node that claims leadership with an equal or greater term, or retries with a new term after a split vote.
- Split votes are kept rare by a random timeout of 150-300 ms between rounds.

**Failure behavior.** If the old leader comes back after a follower has already raised the term, its requests from the older term are rejected, which forces the leadership change. If network latency stays above the heartbeat timeout, back-to-back election rounds can leave unstable groups without a quorum. Those partitions reject writes, but data already written to disk is not lost. Redpanda uses a Raft-priority implementation so the system settles quickly after network outages.

## Checked

2026-11-08. Read the whole How Redpanda Works page. Confirmed: Raft group per partition, 2f+1 tolerance example, majority commit and acks=all, gray-failure note, 150 ms heartbeat, election_timeout_ms default 1500 ms, election outcomes, 150-300 ms random timeout, term rejection, back-to-back elections above the heartbeat timeout, writes rejected without losing written data, Raft-priority implementation. Removed: the closing diagnostic hint (an inference, not on the page).

Method: documentation only; no commands were run.
