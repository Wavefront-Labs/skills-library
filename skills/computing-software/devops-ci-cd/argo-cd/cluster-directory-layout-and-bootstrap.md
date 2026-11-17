---
id: computing-software.devops-ci-cd.argo-cd.cluster-directory-layout-and-bootstrap
name: cluster-directory-layout-and-bootstrap
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, cluster-directory-layout, gitops-repo-structure, app-of-apps]
level: practitioner
status: docs-checked
description: "Structure a GitOps repo with a directory per cluster plus shared infrastructure and apps layers, and bootstrap new clusters from it with Argo CD or Flux."
sources: ["https://fluxcd.io/flux/guides/repository-structure/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Directory per cluster and cluster bootstrap layout

```
clusters/
  prod-eu/
    bootstrap.yaml          # root Application / Flux Kustomizations for this cluster
    cluster-values.yaml     # region, domain, sizes
  staging-eu/
infrastructure/
  base/                     # cert-manager, ingress, ESO, monitoring
  overlays/{prod,staging}/
apps/
  base/<app>/
  overlays/{prod,staging}/<app>/
```

## Argo CD bootstrap
Root app per cluster pointing at an ApplicationSet that targets the cluster by label:
```yaml
# clusters/prod-eu/bootstrap.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata: { name: root-prod-eu, namespace: argocd }
spec:
  project: platform
  source: { repoURL: https://github.com/org/gitops, path: clusters/prod-eu, targetRevision: main }
  destination: { server: https://kubernetes.default.svc, namespace: argocd }
  syncPolicy: { automated: { prune: true, selfHeal: true } }
```
New cluster = register cluster secret with labels (`env=prod, region=eu`) + copy the directory.

## Flux bootstrap
The Flux repository structure guide keeps each cluster's state in a dedicated directory such as `clusters/production` that references the apps and infrastructure overlays; separating apps from infrastructure lets you define reconcile order (cluster add-ons first).

## Rules
- Infrastructure before apps: sync waves (Argo) or the ordering described in the Flux repository structure guide.
- Cluster-specific values live only under `clusters/<name>`; no `if cluster ==` logic in bases.
- Keep the per-cluster directory tiny: references, not copies.

## Verify
- [ ] A fresh cluster converges from bootstrap to all apps Healthy without manual steps.

## Checked
2026-10-28. Confirmed on the Argo CD cluster bootstrapping page: recommended use of ApplicationSets with labelled cluster secrets, and the app-of-apps alternative (admin-only). Confirmed on the Flux repository structure guide: per-cluster directory (for example `clusters/production`) referencing apps and infrastructure overlays, and apps/infrastructure separation to control reconcile order. Confirmed on the sync waves page: waves order resources.
Removed (not confirmed): the `flux bootstrap github` command and flags, and `dependsOn` as the Flux ordering mechanism.

Method: documentation only; no commands were run.
