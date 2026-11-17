---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.argo-cd-sync-waves-hooks-pruning-and-image-updates
name: argo-cd-sync-waves-hooks-pruning-and-image-updates
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, gitops, sync-waves, prune, image-updater, argocd]
level: advanced
status: docs-checked
description: "Order GitOps deployments with Argo CD sync waves and hooks, prune safely, and automate image tag updates with Argo CD Image Updater or Flux."
sources:
  - https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/
  - https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/
  - https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/
  - https://argocd-image-updater.readthedocs.io/en/stable/
  - https://fluxcd.io/flux/guides/image-update/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sync waves, hooks, pruning and image updates

## Sync waves
```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "5"
```
- The value is an integer; Argo CD deploys from the lowest number to the highest. Resources and hooks default to wave 0; negative waves run before everything else.
- Order of precedence within a sync: phase, then wave (lower first), then kind (namespaces first, then other resources, then custom resources), then name.
- Argo CD syncs the first wave that has any out-of-sync or unhealthy resource, applies it, and repeats until all phases and waves are in sync and healthy. A resource stuck unhealthy in an early wave can stop the app ever becoming healthy.
- There is a delay between waves, 2 seconds by default, configurable with the `ARGOCD_SYNC_WAVE_DELAY` environment variable.
- When pruning, wave order is reversed: higher waves are pruned first, and a prune failure in a wave marks the operation failed and skips lower waves.

## Hooks
```yaml
metadata:
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
```
- Hook types: PreSync (before manifests apply), Sync (with the manifests, after PreSync hooks succeed), PostSync (after Sync hooks succeed and resources are Healthy), SyncFail (when the sync fails), Skip (do not apply the manifest), PreDelete (before the Application is deleted; only on Application deletion), PostDelete (after resources are deleted; v2.10+).
- A failing PreSync hook stops the whole sync. The docs suggest essential checks as PreSync hooks and smoke tests as PostSync hooks.
- Hooks do not run during a selective sync. They run on every sync, including self-heal and unrelated changes, so they must be safe to run twice.
- Delete policies: `HookSucceeded`, `HookFailed`, `BeforeHookCreation` (the default when none is set). Use the annotation rather than `ttlSecondsAfterFinished` on hook Jobs, because Argo CD must still read the Job.
- A PreSync hook runs before the Application's own Secrets and ConfigMaps are applied. Keep hook credentials outside the Application, or make the Secret a hook with a lower wave.

## Automated sync and pruning
```yaml
spec:
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - PruneLast=true
      - ApplyOutOfSyncOnly=true
```
- Automated sync does not delete resources removed from Git by default; set `prune: true` to enable it. Prune is also protected against an empty target unless `allowEmpty: true`.
- Self-heal is off by default; with it on, live-cluster drift triggers a sync (default self-heal timeout 5 seconds).
- Automated sync only runs when the app is OutOfSync, once per unique commit and parameters, and does not retry a failed attempt for the same commit. Rollback is not possible while automated sync is enabled.
- Protect an object from pruning with the annotation `argocd.argoproj.io/sync-options: Prune=false` (a resource-level setting overrides the application's prune policy). `PruneLast=true` prunes after other syncs finish; `ApplyOutOfSyncOnly=true` applies only out-of-sync resources while still running hooks.
- Retries use exponential backoff via `syncPolicy.retry` (`limit`, `backoff.duration`, `factor`, `maxDuration`).

## Image updates
- Argo CD Image Updater v1.x is configured with `ImageUpdater` custom resources placed in the same namespace as the Applications; the old annotation-based configuration belongs to v0.x. It sets image parameters on Argo CD applications for Helm, Kustomize or plugin-rendered apps, using strategies `semver`, `newest-build`, `alphabetical`, `digest` and `calver`, and can write changes back to Git. Whether Argo CD deploys the new image automatically depends on the app's automated sync policy.
- Flux: an `ImageRepository` scans a registry, an `ImagePolicy` selects tags (for example a semver range), and an `ImageUpdateAutomation` writes updates to Git. Manifest fields carry marker comments of the form `{"$imagepolicy": "namespace:name"}`, with optional `:tag`, `:name` or `:digest` suffixes.

## Verify
- [ ] Sync history shows resources applied in wave order; removed manifests prune only where intended.

## Checked
Method: docs-checked 2026-11-09 against Argo CD "Sync Phases and Waves", "Automated Sync Policy" and "Sync Options" pages (waves and auto-sync read in full, sync-options searched for Prune, PruneLast, ApplyOutOfSyncOnly), the Argo CD Image Updater landing page (full) and the Flux image-update guide (searched for resource kinds and markers).
Removed: sample wave tiers (-2 to 2), annotation-based Image Updater example (stale for v1.x), semver patch-only advice, app-of-apps wave claim.
