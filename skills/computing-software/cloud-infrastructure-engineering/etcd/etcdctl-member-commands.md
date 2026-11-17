---
id: computing-software.cloud-infrastructure-engineering.etcd.etcdctl-member-commands
name: etcdctl-member-commands
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [member, member-list, member-add, member-remove, member-update, member-promote, etcdctl, cluster-membership]
level: practitioner
status: docs-checked
description: "Inspect and change cluster membership with etcdctl member list, add, remove, update and promote."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/runtime-configuration/"
  - "https://etcd.io/docs/v3.5/op-guide/clustering/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Reconfiguration requests can only be processed when a majority of members is functioning. Changes must be made sequentially. Keep the cluster size above two in production: removing a member from a two-member cluster is unsafe because its majority is also two.

```bash
etcdctl member list
etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380
etcdctl member add infra4 --peer-urls=http://10.0.1.14:2380 --learner
etcdctl member promote 9bf1b35fc7761a23
etcdctl member update a8266ecf031671f3 --peer-urls=http://10.0.1.10:2380
etcdctl member remove a8266ecf031671f3
```

- `member list` prints each member as `ID: name=... peerURLs=... clientURLs=...`.
- `member add NAME --peer-urls=...` informs the cluster about the new member and prints `ETCD_NAME`, `ETCD_INITIAL_CLUSTER` and `ETCD_INITIAL_CLUSTER_STATE=existing`; export those and start the new etcd process with its own listen and advertise URLs and data directory. Adding is a two-step process: register the member, then start it.
- `--learner` adds a non-voting member (supported from v3.4). It is recommended so the member can catch up first. In v3.4 a cluster can have only one learner (`etcdserver: too many learner members in cluster`).
- `member promote ID` makes a learner a voting member, but only once its raft log has caught up with the leader's; otherwise it fails with `can only promote a learner member which is in sync with leader` and you should wait and retry. Promoting a non-learner or an unknown ID also fails.
- `member remove ID`: the target member stops itself and logs that it was permanently removed. Removing the leader is safe, but the cluster is inactive until a new leader is elected (about the election timeout plus voting).
- `member update ID --peer-urls=...` changes a member's advertised peer URLs; then restart the member. Advertised client URLs are updated by restarting the member with a new `--advertise-client-urls`.

Operations: replace a healthy member by removing the old one, then adding the new one; go from 3 to 5 members with two add operations and from 5 to 3 with two remove operations. Replace a failed machine promptly, since failed but unremoved members reduce tolerance for another failure. When adding several members, add one at a time and verify it starts before adding the next.

`--strict-reconfig-check` (default true) rejects reconfiguration requests that would cause quorum loss.

## Checked

2026-11-08. Read in full: etcd v3.5 Runtime reconfiguration page and Clustering Guide, plus the Configuration options page for the strict-reconfig-check default. Confirmed the commands, outputs, learner rules and operations above. Removed: the -w table form, the list of member list columns, the empty-data-directory instruction for replacements and the status field values (not on the pages read).
Method: documentation only; no commands were run.
