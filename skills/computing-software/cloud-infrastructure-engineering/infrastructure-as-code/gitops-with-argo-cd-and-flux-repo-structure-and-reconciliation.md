---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.gitops-with-argo-cd-and-flux-repo-structure-and-reconciliation
name: gitops-with-argo-cd-and-flux-repo-structure-and-reconciliation
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, gitops, argocd, flux, reconciliation-loop, reconcile, gitops-repo-structure, app-of-apps, self-heal]
level: practitioner
status: docs-checked
description: "Set up pull-based GitOps with Argo CD or Flux: repo layout (app-of-apps, kustomize overlays), reconciliation intervals, self-heal and prune, and drift handling."
sources: ["https://opengitops.dev/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/", "https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/webhook/", "https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/", "https://github.com/fluxcd/kustomize-controller/blob/main/docs/spec/v1/kustomizations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitOps with Argo CD and Flux

OpenGitOps principles: desired state is **declarative**, **versioned and immutable** (Git),
**pulled automatically** by an agent, and **continuously reconciled**.

## Repository structure
```
platform-gitops/
  bootstrap/                 # root app (Argo) or flux-system (Flux)
  apps/
    base/orders/             # kustomize base: deployment, service, hpa
    overlays/
      staging/orders/        # patches: replicas, image tag, config
      prod/orders/
  clusters/
    staging/apps.yaml        # which overlays this cluster runs
    prod/apps.yaml
  infrastructure/            # ingress, cert-manager, monitoring (HelmRelease / Application)
```
Separate application source repos (code + CI building images) from the GitOps config repo; CI
updates the image tag in the config repo (PR or Argo CD Image Updater / Flux image automation).

## Argo CD: app of apps
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata: {name: root-prod, namespace: argocd}
spec:
  project: default
  source:
    repoURL: https://git.example.com/platform-gitops.git
    targetRevision: main
    path: clusters/prod
  destination: {server: https://kubernetes.default.svc, namespace: argocd}
  syncPolicy:
    automated: {prune: true, selfHeal: true}
    syncOptions: [CreateNamespace=true]
```
`clusters/prod` contains child `Application` manifests; the Argo CD cluster-bootstrapping docs list the
app-of-apps pattern as the alternative and recommend `ApplicationSet`s (for example the cluster generator). `selfHeal` reverts manual `kubectl edit` changes; `prune` deletes resources
removed from Git.

## Flux
```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata: {name: apps, namespace: flux-system}
spec:
  interval: 10m          # reconcile period
  retryInterval: 2m
  sourceRef: {kind: GitRepository, name: platform-gitops}
  path: ./clusters/prod
  prune: true
  wait: true
  dependsOn: [{name: infrastructure}]
```
Force now: `flux reconcile kustomization apps --with-source`; status: `flux get kustomizations`.

## Reconciliation and drift
- Argo CD polls Git/OCI/Helm repositories every three minutes (`timeout.reconciliation` in `argocd-cm`; webhooks remove the delay); OutOfSync = drift between Git and cluster.
- Self-heal means console/kubectl hotfixes are reverted — the incident process must go through Git (or temporarily disable auto-sync on that app, documented).
- `ignoreDifferences` (Argo) for fields mutated by controllers (HPA replicas, injected sidecars, caBundle).

## Where Ansible fits
Ansible provisions what sits below the cluster or outside Kubernetes (VMs, network, cluster
bootstrap, installing Argo/Flux itself). For VM fleets the pull analogue is `ansible-pull` on a
timer.

## Gotchas
- Secrets cannot be committed in plain text — use Sealed Secrets, SOPS (Flux native) or External Secrets.
- `prune: true` + moving a manifest between apps can delete and recreate resources; Argo CD's `argocd.argoproj.io/sync-options: Prune=false` annotation protects a resource from pruning.
- Many small apps polling a large monorepo hit Git hosting rate limits — use webhooks and repo caching.

## Verify
- [ ] Changing a replica count with kubectl is reverted within the reconcile interval.
- [ ] Removing a manifest in Git removes the resource after sync.

## Checked

2026-10-25, against the Argo CD docs (cluster bootstrapping, webhook, sync options, diffing, auto-sync) and the Flux Kustomization v1 spec. Confirmed: three-minute polling and webhook behaviour, `Prune=false` sync option annotation, `ignoreDifferences`, app-of-apps being the documented alternative to ApplicationSet, Flux `retryInterval`, `prune`, `wait`, `dependsOn` and `flux reconcile kustomization --with-source`. The four OpenGitOps principles (declarative, versioned and immutable, pulled automatically, continuously reconciled) match open-gitops/documents PRINCIPLES.md. Removed the prose-titled sources.

Method: documentation only; no commands were run.
