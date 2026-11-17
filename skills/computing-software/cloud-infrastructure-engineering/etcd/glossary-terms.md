---
id: computing-software.cloud-infrastructure-engineering.etcd.glossary-terms
name: glossary-terms
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [glossary, raft, quorum, member, cluster, peer, revision, lease, snapshot, terminology]
level: intro
status: docs-checked
description: "Core etcd vocabulary from the glossary: member, cluster, peer, client, quorum, revision, lease, compaction, snapshot, watcher and more."
sources:
  - "https://etcd.io/docs/v3.5/learning/glossary/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Terms as the etcd glossary defines them:

- Alarm: raised by the server whenever the cluster needs operator intervention to remain reliable.
- Authentication: manages user access permissions for etcd resources.
- Client: connects to the cluster to fetch pairs, write data or watch for updates.
- Cluster: several members. The node in each member follows Raft to replicate logs; the cluster receives proposals from members, commits them and applies them to the local store.
- Compaction: discards all event history and superseded keys before a given revision, to reclaim space in the backend database.
- Election: the cluster holds elections among members to choose a leader as part of Raft.
- Endpoint: a URL pointing to an etcd service or resource.
- Key: a user-defined identifier for storing and retrieving values.
- Key range: a set of keys that is an individual key, a lexical interval, or all keys greater than a given key. The glossary writes the interval as a < x <= b, while the API overview describes ranges as half-open `[a, b)`; the API page governs request behaviour.
- Keyspace: the set of all keys in a cluster.
- Lease: a short-lived renewable contract that deletes the keys associated with it on expiry.
- Member: a logical etcd server that participates in serving a cluster.
- Modification Revision: the first revision to hold the last write to a key.
- Peer: another member of the same cluster.
- Proposal: a request, such as a write or configuration change, that must go through Raft.
- Quorum: the number of active members needed for consensus to modify cluster state; etcd requires a member majority.
- Revision: a 64-bit cluster-wide counter that starts at 1 and is incremented each time the keyspace is modified.
- Role: a unit of permissions over a set of key ranges that can be granted to users.
- Snapshot: a point-in-time backup of the cluster state.
- Store: the physical storage backing the keyspace.
- Transaction: an atomically executed set of operations; all modified keys share the same modification revision.
- Key Version: the number of writes to a key since it was created, starting at 1; zero for a nonexistent or deleted key.
- Watcher: opened by a client to observe updates on a key range.

## Checked

2026-11-08. Read the v3.5 glossary in full. Rewrote the skill to the glossary entries only. Removed: leader, follower, learner, term, Raft index, WAL, proxy entries and the default port numbers, which the glossary does not define. Noted the glossary interval wording versus the API overview.

Method: documentation only; no commands were run.
