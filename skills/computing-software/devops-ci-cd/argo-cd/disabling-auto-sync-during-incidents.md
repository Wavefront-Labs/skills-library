---
id: computing-software.devops-ci-cd.argo-cd.disabling-auto-sync-during-incidents
name: disabling-auto-sync-during-incidents
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, disable-auto-sync, automated-sync, self-heal]
level: practitioner
status: docs-checked
description: "Pause Argo CD reconciliation during an incident (manual hotfix, debugging): turning off automated sync safely, parent app-of-apps reversion, sync windows and restoring."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/", "https://argo-cd.readthedocs.io/en/stable/user-guide/sync_windows/", "https://argo-cd.readthedocs.io/en/stable/user-guide/skip_reconcile/", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_proj_windows_add/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disabling auto-sync during incidents

With `automated.selfHeal: true`, any manual `kubectl` change is reverted within seconds. During an
incident you may need to hold a hotfix or stop a bad rollout.

## Options (least to most invasive)
1. **Sync window deny** on the project (no edit to the app spec, auditable):
   ```bash
   argocd proj windows add team-a --kind deny --schedule "* * * * *" --duration 2h \
     --applications 'payments-*' --manual-sync
   ```
   `--manual-sync` still lets manual syncs through (windows otherwise affect both manual and automated syncs). Remove with `argocd proj windows delete team-a <id>`; find the ID with `argocd proj windows list team-a`.
2. **Disable automation on the app**:
   ```bash
   argocd app set payments --sync-policy none      # alias of manual
   ```
   or remove `spec.syncPolicy.automated` in Git.
3. **Skip reconcile entirely** (all processing stops and the Application `status` is no longer updated; alpha feature since v2.7.0):
   ```bash
   kubectl -n argocd annotate application payments argocd.argoproj.io/skip-reconcile=true
   ```

## App-of-apps trap
If a parent app manages the child Application manifest with self-heal, `argocd app set` on the
child can be reverted by the parent. Disable auto-sync on the **parent** first (or change Git), or use
the sync window. ApplicationSets regenerate children too; use `spec.syncPolicy.applicationsSync: create-only` or `ignoreApplicationDifferences`.

## Restore
- Reconcile the hotfix into Git first, then re-enable automation, otherwise Argo reverts the fix.
- Remove the skip annotation (or set it to `"false"`) and the deny window; check `argocd app diff` is empty before enabling self-heal.

## Verify
- [ ] Manual change persists for the incident window; after restore the app is Synced with the fix from Git.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: `argocd proj windows add` flags (`--kind`, `--schedule`, `--duration`, `--applications`, `--manual-sync`), `windows delete PROJECT ID`, `argocd app set --sync-policy none`, `skip-reconcile` annotation behaviour and alpha status (v2.7.0), sync window semantics, `applicationsSync: create-only`. Softened the unconfirmed parent-revert claim.

Method: documentation only; no commands were run.
