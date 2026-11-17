---
id: computing-software.devops-ci-cd.argo-cd.application-spec-source-and-destination
name: application-spec-source-and-destination
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, application-spec, source-targetrevision, application-finalizer, destination-name-vs-server, revision-history-limit]
level: practitioner
status: docs-checked
description: "Write Argo CD Application manifests correctly: project, source repoURL/path/chart and targetRevision forms, destination server vs name, finalizers and revisionHistoryLimit."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/", "https://argo-cd.readthedocs.io/en/stable/user-guide/tracking_strategies/", "https://argo-cd.readthedocs.io/en/stable/user-guide/app_deletion/", "https://github.com/argoproj/argo-cd/blob/master/docs/operator-manual/application.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application spec: source, targetRevision, destination

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payments-prod
  namespace: argocd                       # where Argo CD watches Applications
  finalizers:
    - resources-finalizer.argocd.argoproj.io   # delete app => delete its resources (cascade)
spec:
  project: payments                       # never leave prod apps in "default"
  source:
    repoURL: https://github.com/acme/deploy.git
    targetRevision: v1.8.2                # branch | tag | commit SHA | HEAD
    path: apps/payments/overlays/prod
  destination:
    name: prod-eu                         # cluster name from the cluster secret, OR
    # server: https://kubernetes.default.svc
    namespace: payments
  revisionHistoryLimit: 10
  syncPolicy:
    automated: { prune: true, selfHeal: true }
    syncOptions: [CreateNamespace=true]
```

## targetRevision forms
- Git: branch (`main`, tracks HEAD of it), tag (`v1.8.2`), full SHA (pinned), `HEAD` (symbolic reference to the repo default branch).
  Semver constraints (`1.*`, `>=1.0.0 <2.0.0`) are matched against Git tags only, never branches.
- Helm repo source (`chart: payments`, `repoURL: https://charts.acme.io`): exact version `1.8.2`
  or semver range `1.8.*` / `>=1.8.0 <2.0.0` (tracks the newest matching version). Add a `-0` suffix (`*-0`) to include pre-releases.
- Pinning to tags/SHAs moves promotion into Git commits on the Application itself (auditable); branches give continuous delivery.

## destination
- Use `server` (cluster API URL) **or** `name` (cluster name), not both.
- `namespace` is only set on namespace-scoped resources that have no `metadata.namespace` of their own.

## Deletion behaviour
- With the finalizer: deleting the Application cascades to its managed resources;
  `resources-finalizer.argocd.argoproj.io/background` makes it a background cascading deletion.
- Without it: resources stay (orphaned) — safer for stateful apps, surprising for review apps.
- `argocd app delete payments-prod --cascade=false` (`--cascade` defaults to true) to keep resources once.

## Gotchas
- Applications must live in the Argo CD namespace unless "apps in any namespace" is enabled.
- `revisionHistoryLimit` limits the revision history kept for the Application, which rollback uses.

## Verify
- [ ] `argocd app get payments-prod` shows the resolved revision, sync and health.
- [ ] `kubectl -n argocd get app payments-prod -o jsonpath='{.metadata.finalizers}'` matches intent.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: `finalizers` names (foreground and background), destination `server`/`name` and namespace semantics, `revisionHistoryLimit`, Helm semver ranges and the Git-tags-only rule for constraints, `argocd app delete --cascade` default. Removed unconfirmed claims (validation error on both server and name, name surviving endpoint changes).

Method: documentation only; no commands were run.
