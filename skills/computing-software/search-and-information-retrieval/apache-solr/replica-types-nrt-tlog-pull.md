---
id: computing-software.search-and-information-retrieval.apache-solr.replica-types-nrt-tlog-pull
name: replica-types-nrt-tlog-pull
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [replica-types, nrt-replica, tlog-replica, pull-replica, solrcloud-replicas]
level: advanced
status: docs-checked
description: "Choose SolrCloud replica types: NRT default, TLOG and PULL, which copy the leader, soft-commit limits, recommended combinations, and PULL recovery and skipLeaderRecovery."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/solrcloud-shards-indexing.html
  - https://solr.apache.org/guide/solr/latest/deployment-guide/replica-management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# replica-types-nrt-tlog-pull

Types, set at collection or replica creation (default NRT):
- NRT: keeps a transaction log and indexes locally. Only type supporting soft commits.
- TLOG: keeps a transaction log, copies the index from the leader. If it becomes leader, it acts like NRT.
- PULL: no transaction log, no local indexing, only replicates. Cannot be a leader.

Combinations in the guide: all NRT (use when near-real-time is needed); all TLOG; TLOG with PULL.

If more than one replica in a shard writes its own index instead of replicating from an NRT replica, a leader election can leave all replicas out of sync and force full replication.

PULL behavior:
- It keeps serving queries if the leader is down; replication resumes later.
- It stops replicating when it cannot reach ZooKeeper.
- A joining or restarted PULL replica is not queryable until it has recovered from the current leader. The expert replica property `skipLeaderRecovery=true` skips that initial RECOVERING phase.

Add replicas with ADDREPLICA, giving the type (see replica management).

## Checked

2026-11-04. Confirmed against the Solr Reference Guide SolrCloud Shards and Indexing and Replica Management pages: the three types and the NRT default, soft commits only on NRT, TLOG acting like NRT as leader, PULL never leader, the three recommended combinations, the out-of-sync warning, PULL behaviour when the leader or ZooKeeper is unreachable, initial recovery and `skipLeaderRecovery`. Removed the `commitPollInterval` sentence, which the pages do not state.

Method: documentation only; no commands were run.
