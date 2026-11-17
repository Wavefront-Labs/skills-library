---
id: computing-software.devops-ci-cd.argo-cd.automated-promotion-pull-requests
name: automated-promotion-pull-requests
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, promotion-pr-automation, gitops-promotion-pr, image-tag-bump-pr, auto-merge-lower-envs]
level: practitioner
status: docs-checked
description: "Promote releases through GitOps environments with CI-generated pull requests: separate config repo, tag-bump PRs with gh, Image Updater write-back branches."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/", "https://cli.github.com/manual/gh_pr_create", "https://argocd-image-updater.readthedocs.io/en/stable/basics/update-methods/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automated promotion pull requests

Pattern: CI publishes an image, then changes the image tag in a deployment-config repo through a pull request. Argo CD deploys whatever the config repo says.

## 1. Keep config in its own repository
The Argo CD best-practices guide recommends a separate Git repo for manifests, because:
- you can change only the manifests (for example the replica count) without a full CI build;
- the config history is a cleaner audit log;
- a service set built from several repos but deployed as one unit has no natural home in a single source repo;
- commit access to production config can be separated from access to source code;
- CI that pushes manifest changes to the same repo it builds from can loop (build, commit, build).

## 2. The promotion PR
A CI job after image publish checks out the config repo, edits the tag for one environment (a Kustomize image entry, a Helm values file, or similar), pushes a branch and opens a PR with `gh pr create`. Its documented flags include `--title`, `--body`, `--label`, `--base` (target branch) and `--head`; `--fill` autofills title and body from commits, and explicit `--title` / `--body` win over it. Without a fully pushed branch, `gh` prompts to push or fork, so push the branch first. Use a credential that can write to the config repo.

## 3. Higher environments
Promote the exact tag already running in the lower environment rather than a floating "latest". Keep production PRs behind human review and make the PR body link to the source commit.

## 4. Image Updater alternative
Argo CD Image Updater has two write-back methods: `argocd` (modifies the Application resource in the cluster) and `git` (stores parameter overrides in Git, needs Argo CD v2.0 or later). Configure Git write-back in the ImageUpdater custom resource under `writeBackConfig`. By default it commits to the Application's `.spec.source.targetRevision` branch, and `writeBackConfig.gitConfig.branch` overrides it. A `base:target` value creates a separate write branch from the base, which suits protected default branches (you can then open a PR from that branch). Alternate Git credentials use `method: "git:secret:<namespace/name>"`.

## 5. Gotchas
- Leave `replicas` out of manifests if an HPA owns the count.
- Pin remote bases to a tag or commit SHA so a revision's manifests cannot change meaning.

## Verify
- [ ] A publish produces a PR against the config repo whose diff touches only the intended environment.
- [ ] After merge, Argo CD shows the new image tag for that environment.

## Checked
2026-11-09. Confirmed against the Argo CD best-practices page (separate config repo reasons, HPA replicas, immutable revisions), the gh pr create manual (--title, --body, --label, --fill precedence, --base, --head, push/fork prompt) and the Image Updater update-methods page (argocd vs git write-back, v2.0 requirement, writeBackConfig, branch override, base:target write branch, git:secret credentials). Removed: the full GitHub Actions workflow and its action versions, kustomize edit and yq commands, gh pr merge --auto, the claim that GITHUB_TOKEN PRs do not trigger workflows, CODEOWNERS advice, Kargo and Renovate mentions (pages not read).
Method: documentation only; no commands were run.
