---
id: computing-software.cloud-infrastructure-engineering.etcd.runtime-reconfiguration
name: runtime-reconfiguration
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [runtime-reconfiguration, add-member, remove-member, update-member, strict-reconfig-check, quorum, member-replace, cluster-membership]
level: advanced
status: docs-checked
description: "Change membership of a running cluster safely: add, remove and update members, the one-change-at-a-time rule and strict reconfig check."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/runtime-configuration/"
  - "https://etcd.io/docs/v3.5/op-guide/runtime-reconf-design/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Runtime reconfiguration changes membership without restarting the cluster. Requests can only be processed while a majority of members are functioning, so a quorum must be available before any change.

Rules:

- Changes are made sequentially: update one member's peer URLs with `member update`; replace a healthy member by removing the old one then adding a new one; going from 3 to 5 members takes two add operations; 5 to 3 takes two removes.
- Keep clusters larger than two members in production. Removing a member from a two-member cluster is unsafe: the majority is also two, so a failure during removal can leave the cluster unable to progress.
- Every change uses two phases: first inform the cluster (the API call returns when the cluster agrees), then start the new member with the correct `--initial-cluster` and `--initial-cluster-state existing`. A duplicate member ID fails in phase one, and a new member that tries to join before the cluster accepted the change is refused.
- `--strict-reconfig-check` (enabled by default) rejects a reconfiguration if the number of started members would be less than a quorum of the reconfigured cluster. It protects against a misconfigured new member (for example wrong peer URLs) counting toward quorum while unreachable.

Add a member (one at a time; verify it starts before adding another):

```bash
etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380
# prints ETCD_NAME, ETCD_INITIAL_CLUSTER (existing members + new) and ETCD_INITIAL_CLUSTER_STATE=existing
```

Export those variables and start etcd on the new machine with its listen and advertise URLs and `--data-dir`. Adding to a 1-node cluster stalls it until the new member connects, because two members are needed for consensus.

Safer since v3.4: add as a non-voting learner, start it, then promote it.

```bash
etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380 --learner
etcdctl member promote 9bf1b35fc7761a23
```

Promotion fails until the learner's raft log has caught up to the leader (`can only promote a learner member which is in sync with leader`); wait and retry. In v3.4 a cluster may hold one learner (`too many learner members in cluster`).

Remove a member: `etcdctl member remove ID`. The member stops itself and logs `this member has been permanently removed from the cluster. Exiting.` Removing the leader is safe but the cluster is inactive while a new leader is elected (election timeout plus voting).

Update peer URLs: `etcdctl member update ID --peer-urls=URL`, then restart the member. Advertise client URLs need no member command; restart the member with the new `--advertise-client-urls` and it publishes them itself.

Replace a failed machine: remove the member, then add a new one. Failed members left in place hurt quorum and reduce tolerance for further failures.

Start errors: a joining node missing from `--initial-cluster` gives `the member count is unequal`; a peer URL different from the one registered gives `unmatched member while checking PeerURLs`. A removed member started on its old data directory exits when it contacts an active member.

Permanent majority loss cannot be fixed by force-removing members; start a new cluster from an old data directory (the design page rejects force removal as unsafe). Do not use the public discovery service for reconfiguration; it is for bootstrap only.

## Checked

2026-11-08. Read in full: etcd v3.5 Runtime reconfiguration page and the runtime reconfiguration design page. Confirmed everything above. Removed: the quorum arithmetic example for a 3-node cluster, the claim that a removed member must be shut down before hardware is decommissioned, the "restart after peer URL update" ordering beyond what the page states, and the wrong-data-directory ID mismatch remark (not on the pages read).
Method: documentation only; no commands were run.
