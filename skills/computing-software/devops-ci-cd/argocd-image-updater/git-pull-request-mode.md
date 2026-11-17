---
id: computing-software.devops-ci-cd.argocd-image-updater.git-pull-request-mode
name: git-pull-request-mode
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, pull-request, merge-request, protected-branch, head-branch, git-credentials, pr-title]
level: advanced
status: docs-checked
description: "Open a pull request per image update instead of pushing: head branch naming, credential limits (PAT or GitHub App only), PR title and body from the commit template, and TLS rules."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-methods.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Git pull request mode

Adds `gitConfig.pullRequest` to the git method. Instead of pushing to the tracking branch, the controller:

1. pushes the update commit to a generated head branch `image-updater-<targetKey>-<sha256>`
2. opens a PR/MR from it into the base branch

An existing PR for the same head and base is a no-op, and the controller checks the SCM for an open PR before cloning, skipping the whole cycle if one exists. Use it for protected branches or review workflows.

Rules:

- `branch` must be the base branch only; `base:target` with a colon is a validation error that blocks reconciliation
- credentials must carry a bearer token (PAT or GitHub App) via `method: "git:secret:<secret>"`; SSH keys do not work
- `<targetKey>` is an 8-character hash of repo, branch and target path, so apps sharing a target share the PR branch. The old name was `image-updater-<appNamespace>-<appName>-<sha256>`; after upgrading, old PRs are not closed automatically, so close them and delete their branches
- title is the first line of the rendered commit message template, body is the rest. Defaults: `chore: update images for <namespace>/<appName>` and a created-by-argocd-image-updater sentence. Titles over 255 and bodies over 65,536 characters are truncated (Azure DevOps bodies: 4,000)
- SCM API calls always verify TLS (they carry the token) and trust certificates in `ARGOCD_TLS_DATA_PATH`

## Checked

2026-11-04. Confirmed against update-methods.md (Git Pull Request: head branch template and targetKey, no-op for existing PR, colon branch validation error, credentials needing a bearer token, branch rename warning, title and body defaults and truncation limits, TLS rules).

Method: documentation only; no commands were run.
