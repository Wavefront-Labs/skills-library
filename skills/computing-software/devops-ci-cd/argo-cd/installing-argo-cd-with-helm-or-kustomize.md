---
id: computing-software.devops-ci-cd.argo-cd.installing-argo-cd-with-helm-or-kustomize
name: installing-argo-cd-with-helm-or-kustomize
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd-helm-chart, argocd-kustomize-install, argocd-install-manifests, argocd-self-management]
level: practitioner
status: docs-checked
description: "Install Argo CD reproducibly: pinned upstream manifests (HA, namespace, core), Kustomize overlays or the argo-cd Helm chart, server-side apply, self-management."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/installation/", "https://github.com/argoproj/argo-helm/blob/main/charts/argo-cd/values.yaml", "https://argo-cd.readthedocs.io/en/stable/operator-manual/argocd-cm-yaml/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing Argo CD with Helm or Kustomize

## 1. Choose a flavour
| Manifest | Use |
|---|---|
| `install.yaml` | standard install with cluster-admin access (to deploy to the same cluster) |
| `ha/install.yaml` | recommended for production: same as `install.yaml` with multiple replicas for supported components |
| `namespace-install.yaml` | only namespace-level privileges, no cluster roles; CRDs are **not** included and must be installed separately |
| `core-install.yaml` | Argo CD Core: no API server or UI, lightweight non-HA components |

## 2. Kustomize (pinned, patchable)
```yaml
# bootstrap/argocd/kustomization.yaml
namespace: argocd
resources:
  - https://raw.githubusercontent.com/argoproj/argo-cd/<release-tag>/manifests/ha/install.yaml
patches:
  - path: argocd-cm.yaml
  - path: argocd-cmd-params-cm.yaml
  - path: argocd-rbac-cm.yaml
```
```bash
kubectl create namespace argocd
kubectl apply -k bootstrap/argocd --server-side --force-conflicts
```
The Argo CD installation docs install the CRDs with `kubectl apply --server-side --force-conflicts`,
so use server-side apply here too.

## 3. Helm (argo/argo-cd chart)
```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd -n argocd --create-namespace --version <chart-version> -f values.yaml
```
```yaml
# values.yaml
global: { domain: argocd.example.com }
configs:
  params: { server.insecure: true }
  cm: { admin.enabled: false, timeout.reconciliation: 180s }   # chart default for timeout.reconciliation is 120s
  rbac: { policy.default: role:readonly }
redis-ha: { enabled: true }
controller: { replicas: 1 }
server: { replicas: 2 }
repoServer: { replicas: 2 }
crds: { keep: true }          # keep CRDs on chart uninstall (chart default is true)
```
Chart version ≠ Argo CD version; check the chart's `appVersion`.

## 4. Self-management
After bootstrap, create an Application pointing at `bootstrap/argocd` so Argo CD upgrades itself
from Git. Disable prune for the CRDs and its own namespace, and never auto-sync a change that breaks the controller without a tested rollback path (keep the `kubectl apply -k` bootstrap documented).

## Verify
- [ ] `argocd version` shows the pinned server version; all pods Ready; re-running the install is a no-op.

## Checked

2026-10-25, against the Argo CD operator-manual installation page, argocd-cm reference, and argo-helm `charts/argo-cd` (`Chart.yaml`, `values.yaml`, chart 10.x / appVersion 3.5 at check time). Confirmed: the four manifest flavours and what each includes (namespace-install omits CRDs, core-install has no API server or UI), server-side apply for CRDs, `global.domain`, `configs.cm`/`configs.params`/`configs.rbac`, `redis-ha.enabled`, `crds.keep` default true, `timeout.reconciliation` and `admin.enabled`. Removed the pinned Argo CD and chart versions and the 262 KB annotation-limit explanation, which the docs do not state.

Method: documentation only; no commands were run.
