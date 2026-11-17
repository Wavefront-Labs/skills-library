---
id: computing-software.cloud-infrastructure-engineering.kubernetes.emptydir-disk-usage-accounting
name: emptydir-disk-usage-accounting
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, ephemeral-volumes, emptydir-usage, emptydir, ephemeral-storage, eviction]
level: practitioner
status: docs-checked
description: "Understand how emptyDir usage counts toward pod ephemeral-storage and memory limits, set sizeLimit, and find which pod is filling node disk."
sources: ["https://kubernetes.io/docs/concepts/storage/volumes/#emptydir", "https://kubernetes.io/docs/concepts/storage/ephemeral-storage/", "https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#memory-backed-emptydir"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# emptyDir disk usage accounting

## Disk-backed emptyDir
It lives on the medium that backs the kubelet root directory. Local ephemeral storage combines `emptyDir` volumes, container writable layers, images and logs into one filesystem; the kubelet tracks it against `ephemeral-storage` requests and limits.
```yaml
volumes:
- name: scratch
  emptyDir: {sizeLimit: 5Gi}
```
If a Pod's `emptyDir` usage exceeds its `sizeLimit`, or the total of its `emptyDir` volumes exceeds the overall Pod ephemeral-storage limit, the kubelet marks the Pod for eviction; a container whose writable layer plus logs exceeds its limit also leads to eviction. The kubelet message is `Usage of EmptyDir volume "scratch" exceeds the limit "5Gi".`

Usage is measured either by periodic scanning (the kubelet scans each `emptyDir`; scans overlook space used by deleted files) or by filesystem project quotas (`LocalStorageCapacityIsolationFSQuotaMonitoring`, beta in 1.31 and off by default). Project quotas monitor usage faster and more accurately but do not enforce limits; the filesystem must support them (XFS always, ext4 with project quota enabled).

## Memory-backed emptyDir
```yaml
emptyDir: {medium: Memory, sizeLimit: 512Mi}
```
The kubelet counts tmpfs `emptyDir` as container memory use, not ephemeral storage. Without `sizeLimit` a memory-backed volume may consume up to the Pod's memory limit; with no memory limit it can consume all node memory. Files in a memory-backed volume are not reclaimed under memory pressure. Admins can enforce size limits with ResourceQuota, LimitRange or ValidatingAdmissionPolicy. Windows nodes do not support `medium: Memory`.

## Find the culprit
The kubelet summary API reports ephemeral storage and volume usage per Pod:
```bash
kubectl get --raw "/api/v1/nodes/<node>/proxy/stats/summary"
```
Reading it needs `nodes/proxy` access, which is powerful (see the node log query warning in the Kubernetes docs); process the JSON with your own tooling.

## Verify
Pods that use `emptyDir` have ephemeral-storage requests and limits, and `kubectl describe node` no longer shows `DiskPressure` after the change.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: ephemeral storage accounting and eviction, kubelet eviction message in source, periodic scan versus project quota (beta in 1.31, off by default), memory-backed behaviour.

Method: documentation only; no commands were run.
