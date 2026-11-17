---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pre-upgrade-checklist-and-deprecated-api-scanning
name: pre-upgrade-checklist-and-deprecated-api-scanning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pre-upgrade-checklist, kubent, pluto, deprecated-apis, api-deprecation, apiserver-requested-deprecated-apis, cluster-upgrade, compatibility-matrix, upgrade-readiness]
level: practitioner
status: docs-checked
description: "The checklist before any minor upgrade: find removed APIs with kubent/pluto and the apiserver_requested_deprecated_apis metric, check addon matrices, PDBs, backups and skew."
sources: ["https://kubernetes.io/docs/reference/using-api/deprecation-guide/", "https://github.com/doitintl/kube-no-trouble", "https://github.com/FairwindsOps/pluto/blob/master/docs/quickstart.md", "https://kubernetes.io/docs/reference/instrumentation/metrics/", "https://kubernetes.io/releases/version-skew-policy/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre-upgrade checklist and deprecated API scanning

**Goal:** make the upgrade boring. Every item here is a real outage someone had because they
skipped it.

## 1. Removed APIs — three complementary scans
**Live cluster objects** (what is stored now):
```bash
kubent --target-version <X.Y.Z>               # kube-no-trouble: collectors for the cluster, kubectl last-applied annotations and Helm v3 (needs permission to read Secrets for Helm)
pluto detect-all-in-cluster --target-versions k8s=v<X.Y.Z>   # live cluster objects and Helm releases
```
**Manifests in git** (what will be applied later):
```bash
pluto detect-files -d ./manifests --target-versions k8s=v<X.Y.Z>
pluto detect-helm -owide --target-versions k8s=v<X.Y.Z>     # Helm releases in the cluster
helm template <chart-dir> | pluto detect -                   # rendered chart from stdin
```
**Who is still calling old APIs** (clients, not objects — the one most people miss):
```promql
apiserver_requested_deprecated_apis{removed_release="<X.Y>"}
```
The metric is a stable gauge labelled by group, version, resource, subresource and
`removed_release`. Per the deprecation policy the API server also records the deprecated request in
the audit event, so audit logs (`requestURI`, `userAgent`, `user.username`) show *which* client
is still calling an old API. Objects scanned clean but a controller still writing an old
version will fail once the version is removed. The deprecation guide lists removals per release
(for example 1.25 PodSecurityPolicy and `batch/v1beta1` CronJob, 1.26 `autoscaling/v2beta2`,
`flowcontrol.apiserver.k8s.io/v1beta2` in 1.29, `v1beta3` in 1.32).

## 2. Compatibility matrices (write the target versions down)
| Component | Where the matrix is |
|---|---|
| CNI, CSI drivers, ingress controllers, cert-manager, service mesh, operators | each project's own compatibility or supported-versions page and release notes |
| kubectl | supported within one minor version (older or newer) of kube-apiserver (version skew policy) |
| in-house controllers | the client library version they were built with, against the target minor |
Write the supported target versions down for every row before starting.

## 3. Cluster health gates
```bash
kubectl get nodes                                       # every node Ready
kubectl get pods -A                                     # explain every pod that is not Running or Completed
kubectl get pdb -A                                      # ALLOWED DISRUPTIONS 0 will block node drains
kubectl get csr                                         # pending CSRs
kubectl get apiservices                                 # AVAILABLE must be True for every aggregated API
kubectl get validatingwebhookconfigurations,mutatingwebhookconfigurations   # webhooks with failurePolicy Fail must be healthy
```
A webhook with `failurePolicy: Fail` (the default) whose backing pod is evicted during the node
roll rejects every matching request while it is down; scope it with `namespaceSelector` and run
more than one replica.

## 4. Backups and rollback plan
- Back up important components, such as app-level state in databases (the kubeadm upgrade guide
  says `kubeadm upgrade` does not touch workloads but backups are best practice); take an etcd
  backup for self-managed clusters. During an upgrade kubeadm also writes etcd and manifest backups
  under `/etc/kubernetes/tmp`.
- Node image or version noted so nodes can be rolled back.
- Written rollback decision point ("if X is not healthy by T+60 min, we…").

## 5. Feature gates and flags
Review `--feature-gates` on kube-apiserver and the kubelet config against the new release's
feature gate list; under the deprecation policy a gate that goes GA is deprecated and becomes
non-operational. `kubeadm upgrade plan` shows the available upgrade, and `kubeadm upgrade diff` shows
the changes that would be applied to static pod manifests.

## 6. Communication
Maintenance window announced; on-call knows what "control plane unavailable" looks like;
GitOps auto-sync paused for operators whose CRDs change in the new version.

## Gotchas
- kubent/pluto cannot see what is only in CI pipelines (`kubectl apply -f` from a repo they
  don't read) — scan the repos too.
- Scanning the Helm store finds releases; manifests rendered elsewhere and applied with
  `kubectl apply` show up through the last-applied annotation scan or only via the apiserver metric.
- A clean scan today can go dirty tomorrow: run the scan in CI on every PR to the manifests repo.

## Verify
- [ ] `apiserver_requested_deprecated_apis{removed_release="<target>"}` is 0 over the last 7 days.
- [ ] kubent and pluto report nothing for the target version against cluster, Helm store and git.
- [ ] Every row of the matrix table has a version that supports the target minor, and the upgrade order is written down.

## Checked
Checked 2026-10-24 against the kubernetes/website Deprecation Policy and Deprecated API Migration
Guide (removal releases, warning header and metric), the metrics reference (`apiserver_requested_deprecated_apis`,
stable, labels), the version skew policy (kubectl within one minor), the kubeadm upgrade guide and
reference (`upgrade plan`, `upgrade diff`, backups under `/etc/kubernetes/tmp`), the kube-no-trouble README
(`-t/--target-version`, collectors) and the Pluto docs (`detect-files -d`, `detect-helm -owide`,
`detect-all-in-cluster`, `detect -`, `--target-versions k8s=vX.Y.Z`). Removed: per-vendor compatibility page names,
the `jq` PDB filter and the claim that unknown feature gates stop a component starting.
Method: documentation only; no commands were run.
