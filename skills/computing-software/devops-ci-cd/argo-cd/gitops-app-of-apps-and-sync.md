---
id: computing-software.devops-ci-cd.argo-cd.gitops-app-of-apps-and-sync
name: gitops-app-of-apps-and-sync
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, gitops, flux, fluxcd, kubernetes, k8s, continuous-delivery, cd, app-of-apps, applicationset, application, appproject, sync-policy, automated-sync, self-heal, prune, sync-waves, sync-hooks, presync, rollback, helm, kustomize, argo-rollouts, progressive-delivery, drift, ignoredifferences]
level: practitioner
status: docs-checked
description: "Deliver to Kubernetes with Argo CD: separate config repo, automated sync with prune/self-heal, sync waves and hooks, ignoreDifferences, deletion and rollback."
sources: ["https://argo-cd.readthedocs.io/en/stable/", "https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/", "https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/", "https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/", "https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/", "https://argo-cd.readthedocs.io/en/stable/user-guide/app_deletion/", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo CD: app-of-apps, sync policies and safe rollouts

**Goal:** Git is the only way changes reach the cluster; Argo CD keeps the cluster matching Git, and you know how to order, pause and roll back a change.

## 1. Repo layout
Keep application source and deployment config (manifests, Helm values, Kustomize overlays) in separate repos. The best-practices guide gives the reasons: change config without a CI build, a clean audit log, separate access, multi-repo applications deployed as one unit, and no build-commit loop when CI pushes manifest changes.

## 2. Sync policy
Automated sync lives under `spec.syncPolicy.automated`:
- `prune: true`: by default automated sync does not delete resources that left Git. A manual sync with pruning checked, or `argocd app set <APPNAME> --auto-prune`, also works. Pruning has a protection against an empty target set, relaxed with `allowEmpty`.
- `selfHeal: true`: revert manual changes to the cluster. Without it, automated sync attempts one sync per unique combination of commit SHA and parameters.
- `enabled: false` keeps `prune`, `selfHeal` and `allowEmpty` set but inactive.
- `retry` with `limit` (`-1` = unlimited) and `backoff` retries failed syncs with exponential backoff.
- `syncOptions` list such as `CreateNamespace=true` (create `spec.destination.namespace` if missing; otherwise the sync fails) and `ServerSideApply=true` (uses `kubectl apply --server-side --force-conflicts`; `Replace=true` takes precedence over it).

## 3. Deleting applications
A cascade delete removes the app and its resources; a non-cascade delete removes only the app: `argocd app delete APPNAME --cascade=false` (or `--cascade`). In Kubernetes terms the cascade depends on the finalizer `resources-finalizer.argocd.argoproj.io`: unset it for a non-cascade delete, set it (for example with `kubectl patch app APPNAME -p '{"metadata": {"finalizers": ["resources-finalizer.argocd.argoproj.io"]}}' --type merge`) for a cascade delete. For ApplicationSets, `syncPolicy.preserveResourcesOnDeletion: true` keeps child resources when the generated Application is deleted.

## 4. Projects
An AppProject restricts what its apps may use. Spec fields include `sourceRepos` and `clusterResourceWhitelist`; set them per team instead of leaving everything open.

## 5. Ordering: sync waves and hooks
- Sync waves use the `argocd.argoproj.io/sync-wave` annotation (an integer, lowest first, default 0, negative allowed). There is a delay between waves, 2 seconds by default, configurable with `ARGOCD_SYNC_WAVE_DELAY`. Pruning runs in reverse wave order.
- Hooks use the `argocd.argoproj.io/hook` annotation (`PreSync`, `Sync`, `PostSync`, `SyncFail`, `Skip`; also `PreDelete` and `PostDelete`). A failed PreSync hook stops the sync and marks it failed, so use PreSync for essential checks and PostSync for smoke tests. Hooks do not run during a selective sync.
- `argocd.argoproj.io/hook-delete-policy`: `HookSucceeded`, `HookFailed` or `BeforeHookCreation`; if none is specified, `BeforeHookCreation` is assumed.
- To apply a CR in the same sync as a missing CRD, `SkipDryRunOnMissingResource=true` (per resource annotation `argocd.argoproj.io/sync-options` or application-wide sync option) skips the dry run.

## 6. Drift and noise
- For fields changed by other controllers, use `spec.ignoreDifferences` with `jsonPointers` or `jqPathExpressions`; add the `RespectIgnoreDifferences=true` sync option if sync should not overwrite them.
- If an HPA manages replicas, leave `replicas` out of the manifest.
- `argocd app get <app> --hard-refresh` and `argocd app diff <app> --hard-refresh` refresh application data and the manifests cache.
- `argocd app history` shows deployment history and `argocd app rollback` rolls back to a previous deployed version by history ID (the previous one if omitted). With automated sync on, a rollback is undone by the next sync from Git, so prefer reverting the config commit.

## Verify
- [ ] A manual edit of a managed object is reverted when `selfHeal` is on.
- [ ] Deleting a manifest from Git removes the object when `prune` is on.
- [ ] The app belongs to a restricted AppProject.
- [ ] A PreSync migration Job completes before the workloads update.

## Checked
2026-11-09. Confirmed against the Argo CD pages for best practices, automated sync, sync waves and hooks, sync options, application deletion, projects, the ApplicationSet resource-modification page and the `argocd app` command reference. Removed: the Flux comparison (pages not read), the Argo Rollouts remarks, the app-of-apps repo tree and generator list, the full YAML example, `argocd app sync --dry-run`, the claim that rollback works only with auto-sync disabled, wave-by-type examples, and the default-project claim.
Method: documentation only; no commands were run.
