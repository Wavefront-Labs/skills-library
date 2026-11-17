---
id: computing-software.devops-ci-cd.argocd-image-updater.git-write-back-workflow
name: git-write-back-workflow
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, git-write-back, argocd-source-file, target-revision, branch-tracking, persistent-overrides, write-back-config]
level: practitioner
status: docs-checked
description: "Understand what the git write-back method does: it commits .argocd-source-appName.yaml to the tracked branch, why the app must track a branch, and the fetch-commit-push workflow."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-methods.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Git write-back workflow

Enable it with:

```yaml
spec:
  writeBackConfig:
    method: "git"
```

Requires Argo CD v2.0 or later. By default the parameters are stored in `.argocd-source-<appName>.yaml` in the path the Application sources its manifests from; Argo CD picks the file up when rendering the Application named `<appName>`. Helm parameters in it are sorted alphabetically for deterministic output, and a file per app minimises merge conflicts unless another CI party edits it.

Workflow:

1. Fetch the repository from `.spec.source.repoURL`, or from `gitConfig.repository` if set, using the credentials from `writeBackConfig.method`.
2. Check out the target branch: `gitConfig.branch`, else `.spec.source.targetRevision`.
3. Create or update `.argocd-source-<appName>.yaml`.
4. Commit locally.
5. Push using the configured credentials.

Important: Argo CD credentials are reused unless you override them, and the write-back is a commit to the Application's tracking branch. The Application should track a branch. If `targetRevision` is `HEAD`, a tag or a revision, you must set `writeBackConfig.gitConfig.branch`, and for Argo CD to pick up the change the app really should track that branch.

For plugin apps the file may be `.argocd-source-<namespace>_<appName>.yaml` when the Application namespace differs from the controller's.

## Checked

2026-11-04. Confirmed against update-methods.md (git write-back method: Argo CD v2.0 requirement, .argocd-source file, alphabetical Helm parameters, five-step workflow, branch-tracking note, plugin file name).

Method: documentation only; no commands were run.
