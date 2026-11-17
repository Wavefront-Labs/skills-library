---
id: computing-software.cloud-infrastructure-engineering.etcd.failure-modes
name: failure-modes
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [failure-modes, leader-failure, majority-failure, network-partition, follower-failure, bootstrap-failure, fault-tolerance, recovery]
level: practitioner
status: docs-checked
description: "How etcd behaves in follower, leader, majority and partition failures and during bootstrap, and what leases do after failover."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/failures/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Failure modes from the operations guide:

- Minor followers failure: when fewer than half of the followers fail, the cluster keeps accepting requests. Two follower failures do not affect a five-member cluster. Clients lose connectivity to the failed members; client libraries should hide this for reads by reconnecting to other members, and the other members see more load from the reconnections.
- Leader failure: a new leader is elected automatically, taking about an election timeout because detection is timeout based. The cluster cannot process writes during the election; requests sent meanwhile are queued. Writes sent to the old leader but not yet committed may be lost and can show up as client timeouts, but no committed write is ever lost. The new leader extends the timeouts of all leases so a lease does not expire before its granted TTL.
- Majority failure: the cluster cannot accept more writes. It recovers once a majority of members is available again, elects a leader and extends lease timeouts so no lease expires because of server-side unavailability. If a majority cannot come back, the operator must start disaster recovery.
- Network partition: the majority side stays available and the minority side is unavailable. There is no split-brain because membership changes are approved by the current majority. A leader on the minority side steps down and the majority elects a new one. When the partition clears, the minority recognises the majority's leader and recovers its state.
- Failure during bootstrapping: bootstrap succeeds only if all required members start. Remove the data directories on all members and re-bootstrap with a new cluster token or discovery token. Recovering a failed bootstrapped cluster is possible but almost always costs more than re-bootstrapping, since there is no data to recover.

To prepare for rare or unrecoverable failures, always back up the cluster with snapshots.

## Checked

2026-11-08. Read the v3.5 failure modes page in full. Confirmed: all five failure kinds, election timeout, queued writes, lease extension, no split-brain reason and bootstrap advice. Removed: the pre-vote default claim, which the page does not mention.

Method: documentation only; no commands were run.
