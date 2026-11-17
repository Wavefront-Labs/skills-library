---
id: computing-software.devops-ci-cd.atlantis.atlantis-checkout-strategy
name: atlantis-checkout-strategy
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [checkout-strategy, merge-strategy, checkout-depth, shallow-clone, branch-strategy]
level: practitioner
status: docs-checked
description: "Pick the branch or merge checkout strategy and tune shallow clones with checkout-depth."
sources: ["https://www.runatlantis.io/docs/checkout-strategy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis checkout strategy

Set with `--checkout-strategy` or `ATLANTIS_CHECKOUT_STRATEGY`. Two values exist.

`branch` (default): Atlantis checks out the PR source branch. Risk: if the branch is behind `main`, `terraform plan` may propose deleting resources added to `main` since the branch point. Fix by merging `main` into the branch or using `merge`.

`merge`: Atlantis checks out the destination branch (for example `main`), runs `git merge` with the source branch locally, and runs Terraform on the result. The merge is never committed anywhere. If a transient error occurs while updating the merged branch, Atlantis fails rather than use a stale one. The merge happens only in the plan phase, so commits pushed to `main` after planning are not picked up; pair it with the `undiverged` requirement to block applying stale plans.

GitHub App behaviour: Atlantis fetches the PR head from `pull/<PR number>/head` on `origin` and does not create a separate `source` remote, avoiding forks the App cannot access.

Shallow clones with `--checkout-depth`:
1. Shallow-clone the default branch to that depth (zero means full clone).
2. Fetch the PR branch to the same depth.
3. Check the merge base exists in the shallow clone.
4. If not, fetch the full history.

If branches often diverge by more than the depth, raise `--checkout-depth` to avoid frequent full fetches.

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Checkout Strategy. Removed or fixed: nothing needed removing.

Method: documentation only; no commands were run.
