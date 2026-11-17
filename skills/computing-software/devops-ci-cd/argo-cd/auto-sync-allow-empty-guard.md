---
id: computing-software.devops-ci-cd.argo-cd.auto-sync-allow-empty-guard
name: auto-sync-allow-empty-guard
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, allowempty, allow-empty, auto-sync-wipe-protection, prune-safety]
level: practitioner
status: docs-checked
description: "Understand Argo CD automated sync's allowEmpty guard that refuses to prune everything when the source renders no resources, and when to enable it."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/", "https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# allowEmpty guard

## 1. Behaviour
With `syncPolicy.automated.prune: true`, if the source suddenly renders **zero** resources (wrong
`path`, typo in an overlay, Helm `if` disabling everything, repo restructure), auto-sync would
delete the whole application. By default (a safety mechanism since v1.8) automated sync with prune is protected against automation or human errors when there are no target resources, so it does not leave the application empty.

## 2. Opt in only where empty is legitimate
```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
    allowEmpty: true
```
Enable it only where an empty application is intended. Everything else: keep the default `false`. CLI equivalent: `argocd app set <APPNAME> --allow-empty`.

## 3. Related safety nets
- `Prune=false` sync option per resource (`argocd.argoproj.io/sync-options: Prune=false`) for PVCs, namespaces with data.
- `PruneLast=true` so deletions happen after new resources are healthy.

## Verify
- [ ] Point a test app's path to an empty directory: the live resources remain.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: `allowEmpty` under `syncPolicy.automated` (default protection, v1.8, `argocd app set --allow-empty`), `Prune=false` and `PruneLast=true` sync options and annotation form. Removed the quoted log message and two remarks not stated in the documentation.

Method: documentation only; no commands were run.
