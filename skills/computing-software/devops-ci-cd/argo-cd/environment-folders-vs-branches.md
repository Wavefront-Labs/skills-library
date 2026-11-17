---
id: computing-software.devops-ci-cd.argo-cd.environment-folders-vs-branches
name: environment-folders-vs-branches
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, environment-folders, environments-as-branches, gitops-env-layout, overlay-per-environment]
level: practitioner
status: docs-checked
description: "Model GitOps environments as folders on one branch rather than branch-per-environment: layout, promotion by file copy or PR, and the failure modes of env branches."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/", "https://codefresh.io/blog/stop-using-branches-deploying-different-gitops-environments/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment folders vs branches

## 1. Folders on main (recommended)
```text
apps/api/
  base/                       # shared manifests / chart values
  envs/
    dev/      kustomization.yaml  (image tag, replicas, config)
    staging/  kustomization.yaml
    prod-eu/  kustomization.yaml
    prod-us/  kustomization.yaml
```
Each Argo CD Application (or ApplicationSet element) points at `envs/<env>` on `main`.
Promotion = change the env folder's files (copy the tag/values from staging to prod) via a PR.

## 2. Why not branch-per-environment
- Promotions become merges of **everything** on the branch, including unrelated changes you did not mean to promote; teams resort to cherry-picks and branches drift.
- Env-specific config (replicas, URLs) must not be merged — so each branch carries permanent conflicts.
- Hard to see the difference between environments (`diff -r envs/staging envs/prod` vs comparing branches).

## 3. Keep promotion small
- Put the frequently promoted value (image tag/chart version) in one small file per env (`envs/prod/version.yaml`) so promotion PRs are one-line diffs.
- Keep env-specific settings that are *not* promoted separate from promoted artifacts.
- CODEOWNERS on `envs/prod*/` for approvals.

## Verify
- [ ] `git diff envs/staging envs/prod` shows only intended differences plus pending promotions.

## Checked

2026-10-28. Confirmed from the Codefresh article "Stop using branches for deploying to different GitOps environments": environments modelled as folders (Kustomize base plus overlay per environment), merges between environment branches are problematic, unintended changes need manual git cherry-pick, and branch-per-environment invites configuration drift. Removed (not found): Argo CD polling more refs, duplicated branch protection, ApplicationSet PR generator for previews.

Method: documentation only; no commands were run.
