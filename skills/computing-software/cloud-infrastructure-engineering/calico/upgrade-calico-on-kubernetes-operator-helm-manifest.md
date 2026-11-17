---
id: computing-software.cloud-infrastructure-engineering.calico.upgrade-calico-on-kubernetes-operator-helm-manifest
name: upgrade-calico-on-kubernetes-operator-helm-manifest
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [upgrade, operator, helm, manifest, crds, server-side-apply, calicoctl, ownerreferences]
level: practitioner
status: docs-checked
description: "Upgrade Calico on Kubernetes: operator, Helm (CRDs first) or manifest paths with server-side apply, CRD mode preserved, then a matching calicoctl."
sources:
  - https://docs.tigera.io/calico/latest/operations/upgrading/kubernetes-upgrade
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The page covers upgrading to the current release (3.33 at the time of reading) from the two previous releases; read the upgrade notes for each release first. Upgrading preserves your CRD mode: an aggregation API server (v1 CRDs) cluster stays that way, and a native v3 CRD cluster stays on v3. Do not use an older calicoctl after upgrading.

**Operator install:**

```bash
curl <manifests-base-url>/manifests/v1_crd_projectcalico_org.yaml -O
curl <manifests-base-url>/manifests/tigera-operator.yaml -O
kubectl apply --server-side --force-conflicts -f v1_crd_projectcalico_org.yaml
kubectl apply --server-side --force-conflicts -f tigera-operator.yaml
```

The page uses the raw GitHub manifests URL for the target release tag in place of the placeholder. Native v3 CRD clusters use `v3_projectcalico_org.yaml` instead. To get Whisker and flow logs (introduced in 3.30), also create `Goldmane` and `Whisker` resources named `default` (`operator.tigera.io/v1`).

**Helm.** The `tigera-operator` chart does not contain the CRDs and `helm upgrade` does not upgrade them. Recommended: apply the CRDs yourself first (same `kubectl apply --server-side --force-conflicts`), then `helm upgrade <release> projectcalico/tigera-operator`. Alternative: `manageCRDs: true` (default) lets the operator apply them when the new pod starts.

**Manifest + Kubernetes datastore.** Download `calico.yaml` (or `canal.yaml`, `calico-policy-only.yaml`), re-apply any manual edits, apply server-side, and `watch kubectl get pods -n kube-system`. Reinstall calicoctl, then confirm `calicoctl version` shows the new Cluster Version.

Etcd datastore users are advised to move to the Kubernetes API datastore, and manifest users to the operator.

## Checked

2026-11-08. The Upgrade Calico on Kubernetes page was read in full. Commands, CRD-mode behaviour, Helm CRD options and the Goldmane and Whisker note were confirmed. Removed the v3.15 starting version and the claim about OwnerReference UIDs changing since v3.28, which the page does not state. The etcd and application layer policy sections were read but are not covered by this skill.

Method: documentation only; no commands were run.
