---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-version-upgrade-in-static-pod-clusters
name: etcd-version-upgrade-in-static-pod-clusters
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd, etcd-upgrade, etcd-version-upgrade, kubeadm, static-pods, rolling-upgrade, etcd-3-5, etcd-3-6, downgrade, kubeadm-upgrade]
level: advanced
status: docs-checked
description: "Roll etcd to a new minor version one member at a time in a kubeadm/static-pod cluster, with the version-compat rules, pre-checks and the no-downgrade trap."
sources: ["https://etcd.io/docs/v3.6/upgrades/upgrade_3_6/", "https://etcd.io/docs/v3.6/upgrades/upgrading-etcd/", "https://etcd.io/docs/v3.6/downgrades/downgrade_3_6/", "https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-upgrade/", "https://github.com/kubernetes/kubernetes/blob/master/cmd/kubeadm/app/constants/constants.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# etcd version upgrade in static-pod clusters

**Goal:** move etcd from e.g. 3.5.x to 3.6.x without losing quorum, on a cluster where etcd
runs as a kubelet static pod (kubeadm stacked) or on dedicated hosts.

## When kubeadm does it for you
`kubeadm upgrade apply vX.Y.Z` upgrades stacked etcd to the version pinned for that Kubernetes
release (see `kubeadm config images list --kubernetes-version vX.Y.Z`). You only do this by hand
when: etcd is external, you need a patch release ahead of kubeadm, or you set `etcd.local.imageTag`
and froze it. `kubeadm upgrade` skips etcd if `--etcd-upgrade=false`.

## Rules
- One minor at a time (3.4 to 3.5 to 3.6); updating to the latest patch release first is recommended, and
  skipping a minor version is unsupported (etcd upgrade guide).
- A 3.5 to 3.6 upgrade needs every member on 3.5.32 or later first, and a clean v2 store: run
  `etcdutl check v2store` on each member and remove `--enable-v2` (see the 3.6 upgrade guide).
- Kubernetes compatibility: Kubernetes docs list `3.4.29+` and `3.5.11+` as the minimum recommended etcd versions
  for production, and kubeadm records the etcd version it supports per Kubernetes release (its current source pins
  3.7.1-0 for 1.35 to 1.37); stay on the version kubeadm ships unless you have a reason.
- Mixed versions run at the lowest common version; once all members are on the new minor, binaries cannot be rolled
  back. Take a snapshot immediately before; recovery is a restore, or the documented downgrade procedure
  (3.6 to 3.5 downgrade guide).

## Procedure (one member at a time)
```bash
# 0. precheck on any member
etcdctl endpoint status --cluster -w table      # same version everywhere, no errors, small raft-index spread
etcdctl snapshot save /root/pre-upgrade-$(date +%F).db
# 1. on the first member's node, edit the static pod image tag in the manifest
sed -i 's#registry.k8s.io/etcd:<old-tag>#registry.k8s.io/etcd:<new-tag>#' /etc/kubernetes/manifests/etcd.yaml
# kubelet restarts the static pod when the manifest changes
crictl ps | grep etcd ; etcdctl endpoint health --cluster -w table
# 2. wait for the member to be healthy and caught up (RAFT INDEX close to the others), then do the next member
```
On a 3-member cluster never have more than one member down. kubeadm docs warn that in-flight API server requests
stall while the etcd static pod restarts.

For dedicated hosts running systemd etcd: replace the binary (`etcd`, `etcdctl`, `etcdutl`),
`systemctl restart etcd`, same ordering.

## 3.5 to 3.6 specifics
- Every 3.5 member must be on 3.5.32 or later first; mixed 3.5/3.6 is supported only during the roll.
- `etcdctl` only takes snapshots from 3.6; use `etcdutl` for `snapshot status` and `snapshot restore`; fix backup
  scripts first.
- The v2 store is gone: `--enable-v2` was removed. Run `etcdutl check v2store` first and resolve any custom v2
  content as the upgrade guide describes.
- Flags removed, deprecated and added are listed in the 3.6 upgrade guide (for example the `--experimental-*`
  forms of `--corrupt-check-time` and `--max-learners` are deprecated); grep your manifest for them before starting.

## Gotchas
- The cluster-wide version only advances when **all** members are upgraded; until then the
  cluster still behaves as the old minor (no new features, but also safe to pause).
- Watch `etcd_server_version` in Prometheus to see the roll progress.

## Verify
- [ ] `etcdctl endpoint status --cluster -w table` shows the new VERSION on every member and a single leader.
- [ ] `etcdctl member list -w table` shows all members `started`, none `unstarted`/learner.
- [ ] `kubectl get --raw /readyz?verbose` is all `ok`; API latency unchanged.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm source (kubernetes/kubernetes master).

Fixed: the 3.5 to 3.6 prerequisite is that all members run 3.5.32 or later (not 3.5.20), and the v2 store must be checked with `etcdutl check v2store` and `--enable-v2` removed before upgrading; after all members reach 3.6, binaries cannot be rolled back but etcd documents a v3.6 to v3.5 downgrade procedure (the skill said there is no downgrade except by snapshot restore); the leader-last ordering and the `~20s` restart claim are not in the docs. Confirmed: one minor version at a time and update to the latest patch first; mixed versions run on the lowest common version and the cluster counts as upgraded only when all members are; take a snapshot first; `kubeadm upgrade apply --etcd-upgrade` flag (default true); kubeadm supports etcd versions defined in its constants (current master pins 3.7.1-0 for Kubernetes 1.35 to 1.37); Kubernetes docs list 3.4.29+ and 3.5.11+ as the minimum recommended production versions; kubeadm docs warn that in-flight API requests stall while the etcd static pod restarts; the 3.6 flag renames and removals. Removed as unconfirmed: image-tag suffix remarks, the managed-cluster remark, the kubeadm-config imageTag advice and `etcd_cluster_version`.

Method: documentation only; no commands were run.
