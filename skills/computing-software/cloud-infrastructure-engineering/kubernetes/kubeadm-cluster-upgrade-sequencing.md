---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-cluster-upgrade-sequencing
name: kubeadm-cluster-upgrade-sequencing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeadm, upgrade, kubeadm-upgrade-plan, kubeadm-upgrade-apply, kubeadm-upgrade-node, rolling-upgrade, control-plane-upgrade, worker-upgrade, minor-version-upgrade, rollback, upgrade-rollback]
level: advanced
status: docs-checked
description: "Upgrade a kubeadm cluster one minor version at a time: kubeadm upgrade plan/apply/node sequence, control-plane-then-worker ordering, and what to check between each node."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-upgrade/", "https://kubernetes.io/releases/version-skew-policy/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# kubeadm cluster upgrade sequencing

**Goal:** move a kubeadm cluster forward one minor version, control plane first then
workers, without violating
`computing-software.cloud-infrastructure-engineering.kubernetes.version-skew-policy`
at any point mid-rollout, and with a backout plan if something breaks partway. Covers
only the kubeadm/bare-metal path; managed-service upgrade mechanics differ — see
`computing-software.cloud-infrastructure-engineering.kubernetes.bare-metal-vs-managed-cluster-lifecycle-differences`.

## 1. Before touching anything
- Take an etcd snapshot
  (`computing-software.cloud-infrastructure-engineering.kubernetes.etcd-backup-and-restore`)
  immediately before starting — this is the single most valuable thing to have if the
  upgrade goes wrong, cheaper than any rollback procedure.
- Upgrade **one minor version at a time** (for example 1.36 to 1.37, then 1.37 to 1.38);
  skipping minor versions is unsupported, and `kubeadm upgrade apply` enforces the version
  skew policies.
- Read the target version's release notes for API deprecations and removals that affect
  workloads already running.
- Pre-pull target-version images cluster-wide where feasible, same rationale as initial
  bootstrap — catches registry issues before they're on the upgrade's critical path.

## 2. First control-plane node
```bash
apt-mark unhold kubeadm && apt-get install -y kubeadm='<target>.x-*' && apt-mark hold kubeadm
kubeadm upgrade plan                       # shows the exact target and what will change
kubeadm upgrade apply v<target>.x           # on exactly one control-plane node: the first
```
- `upgrade apply` checks the cluster is upgradeable (API server reachable, all nodes `Ready`,
  control plane healthy), enforces the version skew policies, upgrades the control-plane
  components on **that one node** (rolling back if one fails to come up), applies the new
  CoreDNS and kube-proxy manifests and renews the certificates kubeadm manages on the node
  (opt out with `--certificate-renewal=false`). Run it only on the first control-plane node;
  every other control-plane node uses `upgrade node` (next step).
- Drain the node (`kubectl drain <node> --ignore-daemonsets`; a minor kubelet upgrade requires
  it), then upgrade kubelet and kubectl on that same node, and uncordon afterwards:
  ```bash
  apt-mark unhold kubelet kubectl && apt-get install -y kubelet='<target>.x-*' kubectl='<target>.x-*' && apt-mark hold kubelet kubectl
  systemctl daemon-reload && systemctl restart kubelet
  ```
- Confirm `kubectl get nodes` shows this node's kubelet at the new version and
  `Ready` before moving on.

## 3. Remaining control-plane nodes
```bash
kubeadm upgrade node       # NOT "upgrade apply" — that's first-node-only
```
Then the same kubelet/kubectl package bump and restart as above, one node at a time,
confirming `Ready` between each. Doing all control-plane nodes simultaneously risks a
moment where no API server is reachable if something goes wrong mid-restart on more
than one at once.

## 4. Worker nodes
For each worker, drain first (see
`computing-software.cloud-infrastructure-engineering.kubernetes.node-maintenance-cordon-drain-taint`):
```bash
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data
# on the node itself:
apt-mark unhold kubeadm && apt-get install -y kubeadm='<target>.x-*' && apt-mark hold kubeadm
kubeadm upgrade node
apt-mark unhold kubelet kubectl && apt-get install -y kubelet='<target>.x-*' kubectl='<target>.x-*' && apt-mark hold kubelet kubectl
systemctl daemon-reload && systemctl restart kubelet
kubectl uncordon <node>
```
- Workers can be upgraded in waves over days, relying on the version-skew allowance —
  this is the whole point of the skew policy existing; don't feel pressured into an
  all-at-once worker rollout for a large fleet.
- Upgrade workers in batches sized to your actual spare capacity — draining more nodes
  at once than the remaining fleet can absorb causes `Pending` pods, not a clean rollout.

## 5. Rollback reality check
- The kubeadm upgrade documentation describes no downgrade command. `kubeadm upgrade apply`
  rolls the control plane back automatically if a component fails to come up, and
  `kubeadm upgrade apply --force` can recover a bad state without changing the version. During
  an upgrade kubeadm writes `kubeadm-backup-etcd-<date>-<time>` and
  `kubeadm-backup-manifests-<date>-<time>` under `/etc/kubernetes/tmp`; if automatic rollback
  fails they can be restored by hand (the etcd one is empty with external etcd) and they must
  be cleaned up manually afterwards.
- Beyond that, "rollback" means restoring the etcd snapshot taken in step 1 onto a control
  plane still at the old version, or rolling forward to a fixed patch.
- The later into the rollout a problem surfaces, the less a full rollback is actually
  viable — a snapshot restore undoes every object change since the snapshot, not just
  the upgrade. Past a certain point, fixing forward is usually the real plan; say this
  explicitly in the runbook so nobody discovers it mid-incident.

## Gotchas
- `apt-mark hold` (or the DNF/YUM equivalent) on `kubeadm`/`kubelet`/`kubectl` is what
  stops an unattended package upgrade from silently violating version skew between
  upgrade windows — if packages aren't held, an OS patch cycle can bump kubelet past
  the API server without anyone running this procedure.
- CNI and CSI driver compatibility with the new minor is not covered by `kubeadm
  upgrade` at all — check their own release notes before upgrading, not after.

## Verify
- [ ] `kubeadm upgrade plan` was run on the first control-plane node and its target is the
      next minor (or a newer patch of the current one).
- [ ] Every control-plane node shows the new version in `kubectl get nodes -o wide`
      before worker upgrades begin.
- [ ] Each worker is drained, `Ready` at the new version, and uncordoned before moving
      to the next.
- [ ] An etcd snapshot from immediately before the upgrade exists and its restore path
      has been reasoned through (not necessarily executed) for this specific upgrade.
- [ ] CNI/CSI/add-on compatibility with the target minor was checked independently of
      `kubeadm upgrade`'s output.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website and kubernetes/kubernetes master, commit dates 2026-10-24/25) (`kubeadm-upgrade.md` task page and reference). Confirmed: skipping minor versions is unsupported; the first-node, additional-node, worker order; `upgrade apply` checks, skew enforcement, rollback on failure, CoreDNS/kube-proxy manifests and certificate renewal with `--certificate-renewal=false`; a minor kubelet upgrade requires draining; `apt-mark unhold` package steps; the `/etc/kubernetes/tmp` backup folders and `--force` recovery. Removed as unconfirmed: the pinned package revision strings, the claim that a stuck control-plane node blocks `upgrade node` on others, and the unqualified "no supported downgrade" wording (replaced by what the docs state).

Method: documentation only; no commands were run.
