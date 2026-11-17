---
id: computing-software.devops-ci-cd.argocd-image-updater.git-repository-branch-and-templates
name: git-repository-branch-and-templates
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, git-branch, git-repository, branch-template, write-branch, base-target, text-template]
level: advanced
status: docs-checked
description: "Control which repository and branch git write-back uses: gitConfig.repository for Helm-repo apps, branch overrides, base:target write branches, and the text/template variables."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-methods.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Repository, branch and branch templates

Repository. Default: `.spec.source.repoURL`. If that is a Helm repository, Git fails, so set `writeBackConfig.gitConfig.repository`, for example `git@github.com:example/example.git`.

Branch. Default: `.spec.source.targetRevision`. Override (or supply, when it is not a branch) with `gitConfig.branch: "main"`.

Separate write branch, for protected default branches: `branch: "base:target"` creates `target` from `base` and pushes there. `":target"` keeps the Application's target revision as base. Templates use Go `text/template`:

```yaml
gitConfig:
  branch: "main:image-updater{{range .Images}}-{{.Name}}-{{.NewTag}}{{end}}"
# or: "main:image-updater-{{.SHA256}}"
```

Variables:

- `.Images`: list with `.Name`, `.Alias`, `.OldTag`, `.NewTag`
- `.SHA256`: unique hash of the changes
- `.TargetKey`: 8-hex-character hash of the write-back target (repo, branch, path)
- `.AppNamespace`, `.AppName`

Output over 255 characters (git branch limit) is truncated.

Pitfall: the `base:target` colon form is not allowed together with `pullRequest`; that mode takes only the base branch.

## Checked

2026-11-04. Confirmed against update-methods.md (repository and branch defaults, base:target and :target forms, text/template examples, variable list, 255-character truncation, PR-mode colon restriction). Removed a generic self-check line the page does not state.

Method: documentation only; no commands were run.
