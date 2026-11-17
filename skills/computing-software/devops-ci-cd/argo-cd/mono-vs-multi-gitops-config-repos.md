---
id: computing-software.devops-ci-cd.argo-cd.mono-vs-multi-gitops-config-repos
name: mono-vs-multi-gitops-config-repos
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, config-monorepo, config-polyrepo, config-repo-separation, manifest-generate-paths]
level: advanced
status: docs-checked
description: "Choose one GitOps config monorepo or several config repos: access control, blast radius, Argo CD scaling with manifest-generate-paths, code vs config split."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/high_availability/#monorepo-scaling-considerations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mono vs multi config repos

## 1. Separate config from application code (both options agree)
Argo CD best practice: keep manifests in a repo separate from source code — config changes do
not trigger app CI, audit history is clean, and access to production config can be narrower than access to code.

## 2. Options
| | Config monorepo | Repo per team / per env |
|---|---|---|
| Visibility | everything in one place, easy cross-cutting changes | fragmented |
| Access control | CODEOWNERS + rulesets per folder | repo permissions per team/env |
| Blast radius | a bad merge can touch every app | contained |
| Argo CD load | every commit refreshes every app from that repo (unless tuned) | natural isolation |
| Platform-wide refactors | one PR | N PRs |
Common hybrid: one **platform** repo (cluster add-ons, AppProjects, ApplicationSets) + one config repo per team; prod sometimes in its own repo with stricter controls.

## 3. Making a monorepo scale in Argo CD
The `argocd.argoproj.io/manifest-generate-paths` annotation limits manifest regeneration to changes under the listed paths (separate several globs with semicolons); see "Monorepo Scaling Considerations" in the High Availability docs for its requirements. Argo CD polls on a configurable interval (`timeout.reconciliation` in `argocd-cm`); webhooks remove the polling delay.

## 4. Decision hints
- One platform team and a modest number of apps: a monorepo is simpler.
- Many teams with different change cadence or compliance boundaries: repo per team plus a platform repo.
- Regulated prod: a separate prod repo with restricted write access and required reviews.

## Verify
- [ ] A commit touching one app's folder regenerates manifests only for that app (check repo-server logs).

## Checked
2026-10-28. Confirmed on the best-practices page: the five reasons to keep config in a repo separate from source code (clean separation, audit log, multi-repo deployments, access separation, CI loop avoidance). Confirmed in the High Availability, ApplicationSet and operator pages: the `manifest-generate-paths` annotation with semicolon-separated globs, `timeout.reconciliation` in `argocd-cm`, webhooks avoiding polling delay.
Fixed: removed "shallow clones are not available"; the docs describe repositories configured with shallow cloning (depth greater than 0).
Removed (not confirmed): the "<~50 apps" threshold, `reposerver.parallelism.limit`, and the claim that the annotation requires webhooks.

Method: documentation only; no commands were run.
