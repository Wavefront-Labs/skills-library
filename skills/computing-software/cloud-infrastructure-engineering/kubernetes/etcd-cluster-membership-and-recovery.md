---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-cluster-membership-and-recovery
name: etcd-cluster-membership-and-recovery
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd, membership, quorum-loss, member-add, member-remove, raft, disaster-recovery, split-brain, etcdctl, runtime-reconfiguration, force-new-cluster]
level: sme
status: docs-checked
description: "Add, remove, and replace etcd members without losing quorum, and recover a cluster that already has: single-member vs full quorum-loss procedures."
sources: ["https://etcd.io/docs/v3.6/op-guide/runtime-configuration/", "https://etcd.io/docs/v3.6/op-guide/recovery/", "https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://etcd.io/docs/v3.6/learning/design-learner/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# etcd cluster membership and recovery

**Goal:** change who is in the etcd cluster (replace a dead node, scale from 3 to 5)
without a wrong-order step costing quorum, and know the difference between "one member
is down" (routine) and "quorum is gone" (the procedure in
`computing-software.cloud-infrastructure-engineering.kubernetes.etcd-backup-and-restore`).
Pairs with
`computing-software.cloud-infrastructure-engineering.kubernetes.control-plane-ha-stacked-vs-external-etcd`
for the topology this is operating within.

## 1. Rules that govern every membership change
All membership changes are sequential and need a working quorum (etcd runtime reconfiguration guide).
Failed members that have not been removed still count toward the quorum and reduce fault tolerance, so
replace a failed member promptly. It is unsafe to remove a member from a two-member cluster: the majority of
two is two. Use a unique name for each member to avoid human errors (Kubernetes docs).

Replace a failed member (Kubernetes docs and etcd runtime reconfiguration guide; remove, then add):
1. Check the cluster still has quorum and get the failed member's ID: `etcdctl member list`.
2. Point the API servers away from the failed member (remove it from `--etcd-servers`, or stop the API
   server that talks only to it) and stop the etcd process on the broken node.
3. `etcdctl member remove <member-id>`; the removed member stops itself.
4. `etcdctl member add <new-name> --peer-urls=https://<new-ip>:2380`; the output lists the
   `ETCD_NAME`, `ETCD_INITIAL_CLUSTER` and `ETCD_INITIAL_CLUSTER_STATE=existing` values to start with.
5. Start the new member with an **empty** data directory and those values.
6. Wait until it is healthy in `etcdctl member list`, then restore the API server configuration.

## 2. Scaling member count (3 to 5)
Issue one `member add` per new member, and configure and start one member at a time, verifying it starts
correctly before adding the next. To make an addition safer, add it as a learner
(`etcdctl member add <name> --learner --peer-urls=...`), start it, then promote it with
`etcdctl member promote <member-id>` once it has caught up; promotion fails until the learner's log is
in sync. Kubernetes docs recommend a static five-member cluster for production and say not to
autoscale etcd.

## 3. Minority of members down (not a quorum emergency)
A cluster of N members tolerates up to (N-1)/2 permanent failures and keeps serving. Fix the node, or
replace the member with the procedure above on your own schedule.

## 4. Quorum already lost (the actual emergency)
If more than (N-1)/2 members are permanently lost (2 of 3, 3 of 5), the survivors cannot elect a leader and
etcd stops accepting updates; the API server cannot change state and no new pods can be scheduled. Two paths:
- **Members return**: etcd recovers automatically from temporary failures such as reboots; check this first.
- **Majority permanently gone**: restore all members from one snapshot (`etcd-backup-and-restore`),
  optionally supplying new membership at restore time with `--initial-cluster` and a new
  `--initial-cluster-token` so the new cluster only connects to the restored members. Alternatively start the
  surviving member with `--force-new-cluster` to overwrite cluster membership while keeping its data, then
  add new members one at a time. etcd docs call `--force-new-cluster` strongly discouraged because it
  panics if other members from the previous cluster are still alive, so isolate or stop them first. Only
  data present on the surviving member is kept.

## Gotchas
- Start a replacement with an empty data directory and a unique name; never reuse a removed member's data.
- Stop other members of the old cluster before using `--force-new-cluster`.
- Rehearse these procedures in a disposable cluster; membership recovery is high-stakes and rare.

## Verify
- [ ] `etcdctl member list -w table` matches the intended member set, one member per
      failure domain, odd count.
- [ ] A practiced "replace a member" drill exists and has been run in a non-prod
      cluster, not just read.
- [ ] Alerting distinguishes "1 member down, cluster fine" from "quorum lost" — the
      response is different and conflating them causes either panic or complacency.
- [ ] The incident runbook for quorum loss names both recovery paths (wait for
      majority to return vs force-new-cluster vs restore-from-snapshot) and the decision
      criteria between them, not just one procedure.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm and kube-apiserver source (kubernetes/kubernetes master).

Fixed: the skill said to add a replacement member before removing the failed one; the etcd runtime reconfiguration guide and the Kubernetes etcd page both replace a failed member by removing it first and then adding the new one (sequential changes, quorum required). Fixed: the failure tolerance is up to (N-1)/2 permanent failures, not floor(N/2) members; a majority loss means more than (N-1)/2. Fixed: `member remove` makes the removed member stop itself. Confirmed: `member add` prints the `ETCD_NAME`, `ETCD_INITIAL_CLUSTER` and `ETCD_INITIAL_CLUSTER_STATE=existing` values; `member add --learner` and `member promote`; `--force-new-cluster` is strongly discouraged and panics if other members of the previous cluster are alive; restoring with updated membership via `etcdutl snapshot restore`. Removed as unconfirmed: the claims about adding two members at once stalling, and about removed members campaigning.

Method: documentation only; no commands were run.
