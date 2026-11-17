---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-learner-members
name: etcd-learner-members
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd, etcd-learner, learner-member, member-add, member-promote, raft, quorum, runtime-reconfiguration, kubeadm]
level: advanced
status: docs-checked
description: "Add etcd members as non-voting learners first (member add --learner, then member promote) so a slow or misconfigured new member can never cost you quorum."
sources: ["https://etcd.io/docs/v3.6/op-guide/runtime-configuration/", "https://etcd.io/docs/v3.6/learning/design-learner/", "https://etcd.io/docs/v3.6/upgrades/upgrade_3_6/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/", "https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# etcd learner members

**Goal:** grow or replace etcd membership without the classic failure where the new member is
added as a voter, cannot catch up (wrong peer URL, firewall, slow disk), and the cluster now
needs 3-of-4 with only 2 healthy.

## Why learners exist
A learner receives the raft log but does not vote and does not count toward quorum. So a
3-member cluster + 1 learner still needs 2 votes. Once the learner's raft index has caught up
you promote it to a voter; etcd refuses to promote one that is not in sync.

Since 3.4, a cluster may have at most one learner (adding another fails with `etcdserver: too many learner
members in cluster`); the flag `--experimental-max-learners` was renamed `--max-learners` in 3.6. kubeadm joins
new stacked etcd members as learners through the `EtcdLearnerMode` feature gate (alpha 1.27, beta 1.29, GA 1.32,
removed in 1.33, so current kubeadm always does it).

## Procedure
```bash
E="etcdctl --endpoints=https://10.0.0.11:2379 --cacert=... --cert=... --key=..."
# 1. add as learner (note the generated member id and the ENV lines printed)
$E member add etcd3 --learner --peer-urls=https://10.0.0.14:2380
# 2. start etcd on the new host with initial-cluster-state=existing and the full initial-cluster
#    (static pod: set extraArgs or edit the manifest; systemd: ETCD_INITIAL_CLUSTER_STATE=existing)
# 3. watch it catch up
$E endpoint status --cluster -w table         # new member shows IS LEARNER=true; RAFT INDEX converging
# 4. promote when raft index matches (etcd errors with "learner is not ready" otherwise)
$E member promote <hex-id>                     # fails until the learner is in sync with the leader
$E member list -w table                       # IS LEARNER=false
```

## Replacing a member
The etcd runtime reconfiguration guide and the Kubernetes etcd page replace a failed or old member by removing
it first and then adding the new one (see `etcd-cluster-membership-and-recovery`); the etcd guide recommends
adding the new member as a learner until it has caught up, then promoting it. Do one change at a time and
check `endpoint health --cluster` between steps.

## Gotchas
- A learner's data dir must be **empty** on first start; reusing an old `/var/lib/etcd` from a
  previous member identity fails with cluster ID mismatch.
- A learner rejects all requests other than serializable reads and member status — do not point kube-apiserver `--etcd-servers` at a
  learner until it is promoted.
- `member promote` on a member added **without** `--learner` errors (`can only promote a learner member`).
- Promotion is immediate — make sure the host's disk latency is production-grade first
  (`etcd_disk_wal_fsync_duration_seconds` on the new member), because once it votes, its slowness
  slows every write.

## Verify
- [ ] During the add, `endpoint status --cluster` showed exactly one `IS LEARNER=true` member and the leader never changed.
- [ ] After promote, `member list` shows all voters and `endpoint health --cluster` all healthy.
- [ ] Write latency (`etcd_disk_backend_commit_duration_seconds` p99) did not degrade after promotion.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm and kube-apiserver source (kubernetes/kubernetes master); etcd mixin (etcd-io/etcd main); kube-prometheus-stack chart values (prometheus-community/helm-charts main).

Fixed: kubeadm joins new stacked etcd members as learners through the `EtcdLearnerMode` feature gate, which was alpha in 1.27, beta (on by default) in 1.29, GA in 1.32 and removed in 1.33 (kubeadm docs), not "1.30 and GA in 1.32"; the learner limit of one dates from etcd 3.4 and `--experimental-max-learners` was only renamed to `--max-learners` in 3.6 (not raised); the "add learner, promote, then remove the sick member" replacement recipe is not in the docs, which replace a failed member by removing it and then adding the new one. Confirmed: learners receive data but neither vote nor count toward quorum; `member add --learner` and `member promote`; promotion fails with `etcdserver: can only promote a learner member which is in sync with leader` (or `can only promote a learner member` for a voter); adding a second learner fails with `etcdserver: too many learner members in cluster`; a learner rejects all requests other than serializable reads and member status; `IS LEARNER` column in `endpoint status`. Removed as unconfirmed: the stuck-learner kubeadm join note and the exact `rpc not supported for learner` message.

Method: documentation only; no commands were run.
