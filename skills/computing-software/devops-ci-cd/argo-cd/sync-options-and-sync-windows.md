---
id: computing-software.devops-ci-cd.argo-cd.sync-options-and-sync-windows
name: sync-options-and-sync-windows
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, sync-options, server-side-apply, serversideapply, createnamespace, prunelast, applyoutofsynconly, prune-propagation-policy, replace, force, validate-false, respectignoredifferences, skipdryrunonmissingresource, prunepropagationpolicy, retry-backoff, selective-sync, managed-namespace-metadata, delete-options, sync-windows, sync-window, allow-deny-windows, manual-sync-window, maintenance-window, appproject, gitops, kubernetes]
level: practitioner
status: docs-checked
description: "Tune how Argo CD applies changes: per-app and per-resource sync options (ServerSideApply, Replace, PruneLast, ApplyOutOfSyncOnly), retry policy, and AppProject sync windows."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/", "https://argo-cd.readthedocs.io/en/stable/user-guide/sync_windows/", "https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sync options and sync windows

**Goal:** syncs that apply exactly what Git says without fighting admission webhooks,
large CRDs or orphaned namespaces — and that cannot run into production at 17:00 on Friday.

## 1. Where options live
```yaml
spec:
  syncPolicy:
    automated: { prune: true, selfHeal: true, allowEmpty: false }
    syncOptions:
      - ServerSideApply=true
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
      - ApplyOutOfSyncOnly=true
      - RespectIgnoreDifferences=true
    retry:
      limit: 5
      backoff: { duration: 10s, factor: 2, maxDuration: 3m }
    managedNamespaceMetadata:            # with CreateNamespace: labels/annotations Argo keeps on the namespace
      labels: { pod-security.kubernetes.io/enforce: restricted }
```
Per-resource (annotation on the manifest) overrides app-level:
`argocd.argoproj.io/sync-options: Replace=true,Validate=false,Prune=false,Delete=false,ServerSideApply=true`.
Comma-separated; `Prune=false` protects a resource from pruning; `Delete=false` keeps it
when the Application is deleted.

## 2. The options that matter
| option | effect | use when |
|---|---|---|
| `ServerSideApply=true` | `kubectl apply --server-side --force-conflicts`; Argo becomes a field manager | manifests > 262 KB (the `last-applied` annotation limit — big CRDs), fields managed by other controllers (HPA replicas), avoiding `kubectl.kubernetes.io/last-applied-configuration` bloat |
| `Replace=true` | `kubectl replace`/`create` instead of apply; takes precedence over `ServerSideApply=true` | immutable field changes (Job templates, StatefulSet volumeClaimTemplates); **destroys** the object — never on PVCs/Namespaces app-wide; annotate the single resource |
| `Force=true` with `Replace=true` | delete + recreate | last resort for stuck resources; downtime |
| `Validate=false` | skip schema validation | CRDs unknown to the cluster at apply time; unknown fields |
| `CreateNamespace=true` | create destination ns | plus `managedNamespaceMetadata` to label it (PSA, Istio injection) |
| `PruneLast=true` | prune after other resources are healthy | avoid deleting old resources mid-rollout |
| `PrunePropagationPolicy=foreground/background/orphan` | how dependents are deleted | `foreground` waits for children (Jobs/pods), safer sequencing |
| `ApplyOutOfSyncOnly=true` | apply only diffed resources | large apps (hundreds of objects); keeps syncs fast and reduces webhook load |
| `RespectIgnoreDifferences=true` | don't overwrite ignored fields on sync | with `ignoreDifferences` on replicas, webhooks' caBundle etc. — without it, ignore only hides the diff but sync still resets the field |
| `SkipDryRunOnMissingResource=true` | skip dry-run for CRs whose CRD arrives in the same sync | apps that ship CRD + CR together (also fixed by sync waves) |
| `FailOnSharedResource=true` | fail if a resource is already owned by another app | catch duplicate ownership early |
| `Prune=false`/`Delete=false` (resource) | never prune / keep on app deletion | namespaces, PVCs, cluster-scoped shared CRDs |

Selective sync: `argocd app sync myapp --resource apps:Deployment:web` or
`--label tier=frontend`; UI "Sync → Synchronize resources". Dry run: `argocd app sync --dry-run`.

## 3. Retry and self-heal interplay
Without `retry`, a failed sync (webhook timeout, transient API error) stays Failed until
the next Git change or manual sync — set `retry.limit` on automated apps. Self-heal
retries a sync after the self-heal timeout (5 seconds by default, `--self-heal-timeout-seconds` on the application controller); `timeout.reconciliation` in `argocd-cm`
controls automatic refresh, default 120 s plus up to 60 s of jitter (3 minutes at most). A retry `limit` of -1 means unlimited. `allowEmpty: false` refuses to prune everything when
the rendered manifest set is empty (a broken Kustomize render would otherwise delete the
app's resources).

## 4. Sync windows (AppProject)
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata: { name: prod }
spec:
  syncWindows:
    - kind: deny
      schedule: "0 17 * * 5"      # Fri 17:00 …
      duration: 63h               # … to Mon 08:00
      timeZone: Europe/London
      applications: ["*"]
      manualSync: false           # true = humans may still sync manually during the window
    - kind: allow
      schedule: "0 9 * * 1-5"
      duration: 8h
      namespaces: ["payments-*"]
      clusters: ["prod-eu"]
```
Rules: with no matching window all syncs are allowed; if any matching **allow** window exists, syncs happen *only* inside an active allow window; an active **deny**
window always wins over allow; windows affect both automated and manual syncs
(unless `manualSync: true`). Selectors (applications, namespaces, clusters) are OR-ed unless the window's "Use AND operator" option is set. `argocd app get` shows `SyncWindow` and `Assigned Windows`; `argocd proj windows list prod`. `syncOverrun: true` lets an in-progress sync finish when its window ends (see the page for the transition rules). Use deny windows
for change freezes and allow windows for strictly scheduled environments.

## 5. Gotchas
- `ServerSideApply` + an existing client-side-applied object: first sync may show
  conflicts for fields owned by `kubectl`; Argo forces ownership (`--force-conflicts`)
  by default — expected, one-off.
- `Replace=true` on a Deployment resets rollout history and can cause a double rollout.
- `CreateNamespace` namespaces are **not** pruned on app deletion (by design).
- Unlike selective sync, `ApplyOutOfSyncOnly` still runs sync hooks and records the sync in history.
- Set `timeZone` explicitly on each window; `argocd proj windows list` shows the zone (UTC in the docs example).

## Checked
2026-10-31. Confirmed against the Argo CD Sync Options, Sync Windows and Automated Sync pages: option names, per-resource annotation, 262144-byte annotation limit, `--force-conflicts`, retry fields, 5 s self-heal timeout, 120 s reconciliation plus jitter, window rules and CLI. Removed: version claims (since 2.5, 2.12+), hooks-in-window claim, refresh claim, the `andOperator` field name, controller-clock claim, `--prune` CLI note.
Method: documentation only; no commands were run.

## Verify
- [ ] Big CRD app syncs with `ServerSideApply` and no `metadata.annotations: Too long` error.
- [ ] Changing an immutable Job field syncs via resource-level `Replace=true` without affecting other resources.
- [ ] A sync attempted during the deny window is refused (`argocd app get` shows `SyncWindow: Sync Denied`).
- [ ] Transient failures auto-retry; empty renders are rejected (`allowEmpty: false`).
