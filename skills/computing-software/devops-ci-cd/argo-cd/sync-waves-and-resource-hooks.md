---
id: computing-software.devops-ci-cd.argo-cd.sync-waves-and-resource-hooks
name: sync-waves-and-resource-hooks
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, gitops, sync-waves, sync-wave, resource-hooks, presync, sync-hook, postsync, syncfail, postdelete, hook-delete-policy, beforehookcreation, hooksucceeded, database-migration, migration-job, smoke-test, helm-hooks, sync-phases, sync-order, kubernetes, k8s, jobs]
level: advanced
status: gated
description: "Order an Argo CD sync precisely: phases vs waves, PreSync migration Jobs, PostSync smoke tests, SyncFail cleanup, hook delete policies, Helm hook mapping and the pitfalls."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/", "https://argo-cd.readthedocs.io/en/stable/user-guide/resource_hooks/", "https://argo-cd.readthedocs.io/en/stable/user-guide/helm/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo CD sync waves and resource hooks

**Goal:** within one Application's sync, things happen in a known order — migrate the DB,
roll the workloads, run a smoke test, alert on failure — and re-syncs never collide with
leftovers from the last run.

(For ordering *between* Applications, see
`computing-software.devops-ci-cd.argo-cd.app-of-apps-pattern`.)

## 1. The ordering model
Argo CD sorts every resource in a sync by, in order:
1. **Phase:** `PreSync` → `Sync` → `PostSync` (and `SyncFail` only if something failed).
2. **Wave** within the phase: `argocd.argoproj.io/sync-wave: "<int>"`, lowest first,
   default `0`, negatives allowed. Quote the number — it's an annotation string.
3. Kind (Namespaces, CRDs, ServiceAccounts... before Deployments), then name.

Between waves Argo CD waits until the previous wave's resources are **healthy** (for
Jobs: completed), plus a short delay between waves so other controllers can react (see the sync waves page for the current delay and how to change it).
A resource with no health check is considered healthy instantly — so waves on, e.g., a
ConfigMap don't really "wait" for anything.

## 2. Hooks
A hook is any manifest (usually a `Job`, sometimes a `Pod` or a `Workflow`) annotated:
```yaml
metadata:
  generateName: db-migrate-        # or a fixed name + BeforeHookCreation
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
    argocd.argoproj.io/sync-wave: "-1"
```
| Hook | Use for |
|---|---|
| `PreSync` | schema migrations, backups, "is the DB reachable" checks |
| `Sync` | rarely; runs alongside normal resources in their wave |
| `PostSync` | smoke tests, cache warm, notify — runs only after all Sync resources are healthy |
| `SyncFail` | cleanup or alerting when the sync failed |
| `PostDelete` | cleanup after all Application resources are deleted (available starting in v2.10) |
| `Skip` | tell Argo CD not to apply this manifest at all |

Delete policies (combinable, comma-separated):
- `BeforeHookCreation` — any existing hook resource is deleted before the new one is created (since v1.3); meant to be used with a fixed `metadata.name`. It is also assumed when no deletion policy is specified.
- `HookSucceeded` — the hook resource is deleted when the sync succeeds.
- `HookFailed` — the hook resource is deleted when the sync fails.
A Job's spec is immutable, so a hook that is not replaced between syncs will collide on a fixed name.

## 3. A migration done properly
- `PreSync`, wave `-1`, `backoffLimit: 0` or `1` (you want a failed migration to *stop*
  the sync, not retry five times), `activeDeadlineSeconds` set.
- The migration must be compatible with the still-running old pods (expand/contract,
  see `computing-software.devops-ci-cd.deployment-strategies.canary-blue-green-and-rollback`).
- Image tag of the migration Job must move with the app image — template both from the
  same value, or a sync runs new code against an old schema.
- Secrets the Job needs must exist *before* PreSync: they're in the Sync phase by default,
  so on the very first sync the hook can't mount them. Either make the Secret a PreSync
  hook too at an earlier wave, or manage it in another app.

## 4. Helm charts
Argo CD renders charts with `helm template`; it does **not** run Helm's lifecycle. It
maps common Helm hooks: `pre-install`/`pre-upgrade` → `PreSync`, `post-install`/
`post-upgrade` → `PostSync`, `post-delete` → `PostDelete`, `helm.sh/hook-weight` → wave. Argo CD can't tell install from upgrade (every operation is a sync), so pre-install and pre-upgrade hooks run together. Deletion policies are evaluated with Argo CD semantics, not Helm's per-event lifecycle.

## 5. Pitfalls
- Every sync re-runs its hooks (including self-heal and auto-sync syncs) (gated: unconfirmed, source is paywalled or blocked), so make hooks idempotent.
- A hung hook blocks the whole sync; set `activeDeadlineSeconds`, and use
  `argocd app terminate-op <app>` to abort.

## Verify
- [ ] `argocd app get <app>` during a sync shows PreSync job → Sync resources → PostSync job in order.
- [ ] Two consecutive syncs succeed (no "field is immutable"/"already exists" on hooks).
- [ ] A deliberately failing migration halts the sync and old pods keep serving.
- [ ] First-ever sync on an empty namespace works (hook secrets available in time).
- [ ] PostSync smoke test failing marks the sync Failed and fires SyncFail alerting.

## Checked

2026-11-02. Confirmed against the Argo CD resource hooks, sync waves and Helm pages: phases and Skip/PostDelete hook (PostDelete from v2.10), wave ordering (annotation integer, default 0, negatives allowed, lowest first, then kind), delay between waves, delete policies HookSucceeded and BeforeHookCreation (default when none given), Helm hook equivalents (pre/post-install, pre/post-upgrade, post-delete, hook-weight), pre-install and pre-upgrade running together, and argocd app terminate-op. Fixed: the claim that a fixed name with no delete policy fails (BeforeHookCreation is assumed). Removed: ARGOCD_SYNC_WAVE_DELAY, test-hook and prune-order claims. Gated: hooks re-run on every sync including self-heal.

Method: documentation only; no commands were run.
