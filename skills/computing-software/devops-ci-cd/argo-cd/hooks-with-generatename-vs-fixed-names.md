---
id: computing-software.devops-ci-cd.argo-cd.hooks-with-generatename-vs-fixed-names
name: hooks-with-generatename-vs-fixed-names
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, hook-generatename, resource-hooks, hook-delete-policy]
level: practitioner
status: docs-checked
description: "Choose between generateName and fixed names for Argo CD hook Jobs, combining them with hook-delete-policy so reruns do not fail on immutable Job specs or pile up."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/resource_hooks/", "https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/", "https://argo-cd.readthedocs.io/en/stable/user-guide/helm/#helm-hooks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hooks with generateName vs fixed names

## Fixed name
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migrate
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
```
Next sync: Argo CD deletes the existing hook resource before creating the new one. `BeforeHookCreation` is meant to be used with a fixed `/metadata/name`, and it is what Argo CD assumes when no delete policy is set.

## generateName
```yaml
metadata:
  generateName: db-migrate-
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
```
Each sync creates a new hook resource with a generated suffix. Successful ones are removed by `HookSucceeded`; failed ones stay for debugging until you delete them or the next sync with a `HookFailed` policy.

## Rules
- Pick one delete policy strategy:
  | Policy | Behaviour |
  |---|---|
  | `BeforeHookCreation` (assumed when no policy is set) | any existing hook resource is deleted before the new one is created; use with a fixed name |
  | `HookSucceeded` | the hook resource is deleted when the sync succeeds |
  | `HookFailed` | the hook resource is deleted after the hook failed |
- Do not use `ttlSecondsAfterFinished` on hook Jobs: Argo CD must read the Job to learn how the phase went, and if Kubernetes deletes it first the sync can wait for a hook that is gone. Use `hook-delete-policy` for cleanup.
- Helm hook annotations are mapped to Argo CD hooks, and `helm.sh/hook-delete-policy` is supported, with cleanup following Argo CD sync semantics.

## Verify
- [ ] Two consecutive syncs succeed; `kubectl get jobs` shows the expected retained hooks only.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: hook delete policies and their meanings, `BeforeHookCreation` assumed when no policy is set and intended for fixed names, `generateName` hook example in the docs, warning against `ttlSecondsAfterFinished` on hook Jobs (the old skill recommended it), Helm hook-delete-policy mapping. Removed unconfirmed claims (immutable Job error, generateName rejected for normal resources, hooks not pruned).

Method: documentation only; no commands were run.
