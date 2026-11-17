---
id: computing-software.cloud-infrastructure-engineering.kubernetes.helm-crd-lifecycle-and-deletion-risk
name: helm-crd-lifecycle-and-deletion-risk
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, helm-crds, crd-upgrade, crd-deletion, helm, crd, operators]
level: advanced
status: verified
description: "Install and upgrade CRDs shipped in Helm charts without data loss: crds/ directory limits, separate CRD charts, server-side apply upgrades, and guarding against CRD deletion."
sources: ["https://helm.sh/docs/chart_best_practices/custom_resource_definitions/", "https://helm.sh/docs/topics/charts/#custom-resource-definitions-crds", "https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#delete-a-customresourcedefinition"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CRD lifecycle with Helm

## What Helm 3 does with `crds/`
- Installs CRDs from `crds/` on `helm install` **only if absent**.
- **Never upgrades** them on `helm upgrade` and **never deletes** them on `helm uninstall`.
- No templating in `crds/`; `--skip-crds` skips them.
Result: chart upgrades silently run new controllers against old CRD schemas (new fields
pruned, validation mismatches).

## The danger: deleting a CRD deletes every CR
`kubectl delete crd certificates.cert-manager.io` cascades to all Certificate objects in all
namespaces, and the operator then deletes what they managed. Helm never doing it is
deliberate. Anything else that might (Argo CD prune, `kubectl delete -f` of a whole
manifest, a templated CRD removed from a chart) needs a guard.

## Upgrade patterns (pick one per chart)
1. **Apply CRDs out of band before upgrading** (most common for cert-manager, Prometheus operator):
```bash
helm pull prometheus-community/kube-prometheus-stack --version 77.0.0 --untar
kubectl apply --server-side --force-conflicts -f kube-prometheus-stack/charts/crds/crds/
helm upgrade kps prometheus-community/kube-prometheus-stack --version 77.0.0 --reset-then-reuse-values
```
   `--server-side` avoids the 262144-byte annotation limit large CRDs hit with client-side apply.
2. **Separate CRD chart** (e.g. `prometheus-operator-crds`) with CRDs under `templates/`,
   upgraded first. Add the annotation so uninstalling never deletes them:
```yaml
metadata:
  annotations:
    helm.sh/resource-policy: keep
```
3. **Chart flag** (`crds.enabled=true` in cert-manager; `installCRDs` is deprecated there): CRDs templated in
   the main chart; check the chart sets `keep` (cert-manager's `crds.keep` defaults to `true`, and its values
   file warns that removing the CRDs removes every Certificate and Issuer), or uninstall deletes them.

## GitOps notes
- Argo CD: put CRDs in an earlier sync wave, use `ServerSideApply=true` for large CRDs, and
  annotate CRDs with `argocd.argoproj.io/sync-options: Prune=false,Delete=false`.
- Flux HelmRelease: `spec.install.crds: Create`, `spec.upgrade.crds: CreateReplace` to have
  Flux upgrade CRDs from `crds/`.

## Before a CRD upgrade
- Read the operator's upgrade notes for storage version changes and conversion webhooks.
- Back up CRs: `kubectl get <kind> -A -o yaml > backup.yaml` (or Velero).
- `kubectl diff --server-side -f crds/` to see schema changes.

## Verify
```bash
kubectl get crd <name> -o jsonpath='{.spec.versions[*].name} {.status.storedVersions}'
kubectl get crd <name> -o jsonpath='{.metadata.annotations.helm\.sh/resource-policy}'
```
- [ ] CRD schema matches the chart version; CR count unchanged after upgrade.
