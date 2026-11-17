---
id: computing-software.cloud-infrastructure-engineering.kubernetes.argocd-sync-waves-and-hooks
name: argocd-sync-waves-and-hooks
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, gitops, argocd, sync-waves, sync-hooks, argocd-hooks, presync, sync-options]
level: practitioner
status: docs-checked
description: "Order Argo CD syncs with sync waves and PreSync/Sync/PostSync/SyncFail hooks (migrations, smoke tests), hook deletion policies, and how waves interact with health checks."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/", "https://argo-cd.readthedocs.io/en/stable/user-guide/resource_hooks/", "https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo CD sync waves and hooks

## Order of a sync
Phases: **PreSync → Sync → PostSync** (SyncFail only on failure). Within a phase, resources are
applied by **wave** (annotation, integer, default 0, negatives allowed), then by kind
(Namespaces first, then other Kubernetes resources, then custom resources), then name. Argo CD
waits for the resources in a wave to be in sync and **healthy** before the next wave, with a
2 second delay between waves (configurable with `ARGOCD_SYNC_WAVE_DELAY`).
```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "-1"     # e.g. ConfigMaps/Secrets/CRDs before apps
```
An illustrative layout: `-2` CRDs/operators, `-1` config and secrets, `0` databases, `1` apps,
`2` ingress/routes.

## Hooks
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migrate
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation,HookSucceeded
    argocd.argoproj.io/sync-wave: "0"
spec:
  backoffLimit: 1
  template:
    spec:
      restartPolicy: Never
      containers: [{name: migrate, image: myapp:1.9.0, command: ["./migrate","up"]}]
```
- `PreSync` (migrations), `Sync` (with resources), `PostSync` (smoke tests, notifications after
  everything is healthy), `SyncFail` (cleanup/alert), `Skip`.
- Delete policies: `HookSucceeded`, `HookFailed`, `BeforeHookCreation` (delete the existing
  hook before creating the new one; meant to be used with a fixed `metadata.name`, which suits
  immutable Job specs). If none is specified, Argo CD assumes `BeforeHookCreation`.
- Hooks do not run during a selective sync.
- A failing PreSync hook stops the sync — new app version never applied (good for migrations).
- Helm charts' `helm.sh/hook` annotations are mapped to Argo CD hooks (pre-install and
  pre-upgrade become PreSync, post-install and post-upgrade become PostSync, pre-delete and
  post-delete map to PreDelete and PostDelete); `helm.sh/hook-weight` maps to the wave.
  `test-success`, `test-failure`, rollback hooks and `hook-delete-timeout` are not supported,
  and if any Argo CD hook is defined all Helm hooks are ignored.

## Gotchas
- Waves wait on **health**: a stuck Progressing Deployment blocks all later waves. A resource
  annotated `argocd.argoproj.io/sync-options: SkipHealthCheck=true` is treated as synced as soon
  as it is applied, so later waves do not wait for it.
- During pruning the wave order is reversed (higher waves are pruned first); use `PruneLast=true`
  in sync options for resources that must be pruned last.
- Waves order resources within one Application; to order across Applications, put waves on the
  Application objects in an app-of-apps (this relies on Application health assessment, see the
  health docs).

## Verify
- [ ] Sync history shows hooks in order; migration Job runs once per sync and is cleaned up; failed PreSync leaves the old version running.

## Checked

Documentation release: Argo CD stable docs (argo-cd repo docs/, latest release v3.5.6, repo commit 2026-10-25).
Confirmed: PreSync/Sync/PostSync/SyncFail/Skip hooks; default wave 0 with negative waves allowed; ordering by phase, wave, kind, name; 2 second inter-wave delay and its env variable; delete policies and the `BeforeHookCreation` default; hooks not run on selective sync; reverse-order pruning and `PruneLast`; `SkipHealthCheck`; the Helm hook mapping table and the "any Argo CD hook disables Helm hooks" warning.
Corrected: "a second sync fails without a delete policy" (BeforeHookCreation is the default), the Helm test hook behaviour and the kind ordering. Removed the claim that a resource without a health check counts as healthy immediately and the unsourced `argocd-cm` Application health requirement.

Method: documentation only; no commands were run.
