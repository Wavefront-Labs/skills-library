---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-backup-and-restore
name: etcd-backup-and-restore
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd, etcdctl, snapshot, backup, restore, disaster-recovery, velero, static-pod, cluster-state, point-in-time-recovery, kubeadm, snapshot-save, snapshot-restore, etcdutl]
level: advanced
status: docs-checked
description: "Take, verify, and restore etcd snapshots for a kubeadm cluster: the exact etcdctl commands, restore procedure, and the gotchas that make backups untestable."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://etcd.io/docs/v3.6/op-guide/recovery/", "https://etcd.io/docs/v3.6/tasks/operator/how-to-save-database/", "https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# etcd backup and restore

**Goal:** a snapshot that is actually restorable, and a restore procedure that has been
run at least once before you need it for real. etcd is the single source of truth for
the entire cluster — every object, every Secret, every CRD instance — so this is the one
backup in the stack where "we have a cron job" without a tested restore is a false sense
of safety. Membership loss / adding-back-a-member is
`computing-software.cloud-infrastructure-engineering.kubernetes.etcd-cluster-membership-and-recovery`;
routine health/defrag is
`computing-software.cloud-infrastructure-engineering.kubernetes.etcd-defragmentation-and-compaction`.

## 1. Taking a snapshot
Run on a control-plane node, against one etcd member (snapshots are full-state, any
healthy member works):
```bash
ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-$(date +%Y%m%d%H%M).db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```
- `etcdctl` and `etcdutl` are separate binaries (etcd 3.6 and later: `etcdctl` takes snapshots, `etcdutl`
  works on snapshot and data files). Install the versions that match the running etcd, or run the tool
  from a container image directly in the container runtime (for example `crictl run`), as the kubeadm
  external etcd guide does. Copy the snapshot off that host immediately; it is not where backups should live.
- Always verify immediately: `etcdutl snapshot status /backup/etcd-....db -w table` prints the hash,
  revision, total keys and size (`etcdctl snapshot status` is deprecated). Snapshots made with
  `snapshot save` carry an integrity hash that `etcdutl snapshot restore` checks.
- Request the snapshot from one member only: the `--endpoints` flag must contain a single endpoint.
- Ship the snapshot off-node before the node it came from can be the thing that fails —
  S3/GCS/Azure Blob with lifecycle-expiry, or a separate backup host. A snapshot sitting
  only on the control-plane node's disk is not a backup.

## 2. What a snapshot does and does not capture
- Captures the entire etcd keyspace: every Kubernetes object, CRDs, Secrets. Secrets are stored as plain
  text unless encryption at rest is configured on the API server; with it, the snapshot holds ciphertext
  and the API server's encryption keys are needed to read the data, so back those keys up separately.
  Kubernetes docs advise encrypting the snapshot file itself.
- Does **not** capture: PV/PVC data itself (only the K8s objects describing it — storage
  class snapshotting/Velero with volume backup is separate), container images, or
  anything outside the API server's view (node-local config, CNI state).
- A snapshot is a point-in-time full copy, not incremental — size and `save` time grow
  with keyspace size; for large clusters schedule snapshots during low-write windows and
  monitor `save` duration as a capacity signal.

## 3. Scheduling and retention
- Cron or a CronJob-adjacent mechanism on a control-plane node (not a workload Pod — it
  needs host access to the etcd certs and, ideally, local disk before upload). Hourly to
  every-6-hours is typical; align retention with how much config drift you can tolerate
  re-applying via GitOps after a restore (if config is in Git, snapshot frequency matters
  less — restore to the last snapshot, then `kubectl apply` the GitOps state forward).
- Keep snapshots from before and after any cluster upgrade explicitly, tagged — these are
  the ones you reach for first if an upgrade goes wrong.

## 4. Restore
Restore is **offline and replaces the whole cluster state**; it is not a merge. Kubernetes docs: stop *all*
API server instances, restore state in all etcd members, then restart the API servers; they also
recommend restarting `kube-scheduler`, `kube-controller-manager` and the kubelets so nothing relies on
stale data.

From etcd 3.6, `etcdctl` only takes snapshots and `etcdutl` restores them. Every member restores from the
SAME snapshot file into a new data directory, with its own name and peer URL:
```bash
etcdutl snapshot restore /backup/etcd-20261001.db \
  --name <etcd-member-name> \
  --data-dir /var/lib/etcd-restore \
  --initial-cluster <name1>=https://<ip1>:2380,<name2>=https://<ip2>:2380,... \
  --initial-advertise-peer-urls https://<this-ip>:2380 \
  --initial-cluster-token <restored-cluster-token>
```
- Restore overwrites the member ID and cluster ID, so the restored members form a new logical cluster and
  cannot rejoin the old one; the new `--initial-cluster-token` makes them connect only to each other.
- Revisions go backwards after a restore, which can leave controller informers with stale caches. etcd
  docs recommend `--bump-revision <n> --mark-compacted` for Kubernetes restores (the bump should exceed the
  revisions written since the snapshot, for example 1000000000 for a week-old snapshot at under
  1500 writes per second).
- A file copied from `member/snap/db` has no integrity hash and restores only with `--skip-hash-check`.
- Then change the `etcd-data` hostPath volume in `/etc/kubernetes/manifests/etcd.yaml` to the new directory
  and delete the etcd pod or restart kubelet.
- Any object created after the snapshot is gone, including anything a controller reconciled in response (a
  Deployment scaled up after the snapshot reverts to its old replica count).

## Gotchas
- `--name` and `--initial-cluster` must match what each member will present when it starts.
- `etcdutl snapshot restore` creates the `--data-dir` itself: restore into a new path, not over the live
  data directory.
- Kubernetes docs say a snapshot "will not affect the performance of the member", but schedule it off peak
  for very large keyspaces and watch the duration.

## Verify
- [ ] A scheduled snapshot exists, is copied off the source node, and `etcdctl snapshot
      status` reports a valid revision and key count, not just a non-zero file size.
- [ ] A full restore has been rehearsed end-to-end in a non-prod cluster in the last
      quarter — not just read about.
- [ ] Restore runbook names the exact `--initial-cluster` string for the current member
      set, not a placeholder to fill in during the incident.
- [ ] Post-restore, `kubectl get events -A` and application state are reconciled against
      the GitOps/Git source of truth for anything created after the snapshot.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm and kube-apiserver source (kubernetes/kubernetes master).

Confirmed: `etcdctl snapshot save` against a single endpoint and `etcdutl snapshot status` (the etcdctl form is deprecated); since etcd 3.6 restore is done with `etcdutl snapshot restore`, all members restore from the same snapshot with `--name`, `--data-dir`, `--initial-cluster`, `--initial-cluster-token` and `--initial-advertise-peer-urls`; `--bump-revision` and `--mark-compacted` are recommended for Kubernetes restores; `--skip-hash-check` is needed for a file copied from `member/snap/db`; stop all API servers before restoring and restart control-plane components and kubelets afterwards; edit the `etcd-data` hostPath in the etcd static pod manifest and delete the pod or restart kubelet; snapshotting does not affect member performance (Kubernetes docs). Removed as unconfirmed: running etcdctl through `kubectl exec`, the single-member-first restore procedure (the docs restore every member from the same snapshot), and the claim that save holds a read transaction.

Method: documentation only; no commands were run.
