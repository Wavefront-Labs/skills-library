---
id: computing-software.cloud-infrastructure-engineering.kubernetes.argocd-cli-sync-diff-rollback
name: argocd-cli-sync-diff-rollback
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, gitops, argocd-cli, argocd, rollback, sync]
level: practitioner
status: docs-checked
description: "Operate Argo CD applications from the argocd CLI: log in, diff, sync selected resources, wait for health, view history, roll back and terminate stuck operations."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd/", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_rollback/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# argocd CLI operations

## Log in
```bash
argocd login argocd.example.com --sso            # or --username admin --password ...
argocd login --core                              # talk to the cluster directly with kubeconfig
argocd context
```

## Inspect
```bash
argocd app list -p payments
argocd app get shop --refresh                    # status, health, sync, resources
argocd app diff shop                             # live vs desired; exit code 1 when different
argocd app manifests shop --source live | less
argocd app history shop
```

## Sync
```bash
argocd app sync shop --dry-run
argocd app sync shop --prune
argocd app sync shop --resource apps:Deployment:web     # one resource only
argocd app sync shop --revision 3f2c1ab                 # sync to a specific revision
argocd app wait shop --health --sync --timeout 600
argocd app terminate-op shop                            # stop a hung sync
```

## Roll back
```bash
argocd app history shop             # ID, date, revision
argocd app set shop --sync-policy none     # rollback requires auto-sync off
argocd app rollback shop 12
```
Then fix Git (revert the commit) and re-enable auto-sync; otherwise the next sync re-applies the
bad revision.

## CI usage
Use a token for a dedicated local account (`argocd account generate-token --account ci`, add
`--expires-in` to expire it) with RBAC limited to `sync` and `get` on its applications; `argocd app wait` makes the pipeline fail on degraded health.

## Verify
`argocd app get shop` shows `Synced` and `Healthy` at the expected revision.

## Checked

Documentation release: Argo CD stable docs (argo-cd repo docs/, latest release v3.5.6, repo commit 2026-10-25).
Confirmed against the generated CLI reference: `login --sso/--core`, `app get --refresh`, `app diff` exit code 1 when a diff is found, `app manifests --source live|git`, `app sync --dry-run/--prune/--resource GROUP:KIND:NAME/--revision`, `app wait --health --sync --timeout`, `app terminate-op`, `app set --sync-policy` (`none` is an alias of manual), `app rollback APPNAME [ID]` and that rollback cannot be performed against an app with automated sync enabled, `account generate-token --account/--expires-in`, existence of `argocd context` and `app history`.
Corrected: the CI token is for a local account, not a project-scoped role token; removed the unconfirmed "manual apps" qualifier.

Method: documentation only; no commands were run.
