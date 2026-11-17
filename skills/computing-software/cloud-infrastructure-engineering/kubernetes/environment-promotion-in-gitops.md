---
id: computing-software.cloud-infrastructure-engineering.kubernetes.environment-promotion-in-gitops
name: environment-promotion-in-gitops
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, gitops, promotion, environment-promotion, dev-staging-prod, pr-based-promotion, bake-time, image-tag-bump, digest-pinning, argo-cd, fluxcd, release-pipeline, approval-gate, rollback]
level: practitioner
status: docs-checked
description: "Promote a change dev to staging to prod through GitOps: PR-based tag/digest bumps, bake time, bot-authored vs human-gated promotion, and rollback by revert."
sources: ["https://github.com/argoproj/argo-cd/blob/master/docs/user-guide/best_practices.md", "https://github.com/fluxcd/website/blob/main/content/en/flux/guides/image-update.md", "https://github.com/kubernetes-sigs/kustomize/blob/master/api/types/image.go", "https://github.com/argoproj/argo-rollouts/blob/master/docs/features/analysis.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment promotion in GitOps — moving one validated artifact forward, deliberately

**Goal:** the exact artifact (image digest, chart version) validated in dev is the
one that reaches prod — never a rebuild, and never a promotion that skips the gates
you intended. This assumes a repo layout from
`computing-software.cloud-infrastructure-engineering.kubernetes.gitops-repo-structure-patterns`
(directories-per-env is assumed below).

## 1. The mechanism: a PR that bumps a reference, not a rebuild
```
clusters/dev/apps/api/kustomization.yaml      images: [{name: api, newTag: "sha-abc123"}]
clusters/staging/apps/api/kustomization.yaml  images: [{name: api, newTag: "sha-abc123"}]  # promoted here
clusters/prod/apps/api/kustomization.yaml     images: [{name: api, newTag: "sha-def456"}]  # one version behind
```
Promotion = a PR that copies the *same* tag/digest from the staging file into the
prod file (or sets the kustomize image `digest` field, which takes precedence over `newTag`
when both are present). It is never a new build — rebuilding at promotion time breaks the "what's live is what was tested"
guarantee GitOps exists to provide.

## 2. Who/what opens the promotion PR
- **Bot-authored, human-merged**: a scheduled job or a post-deploy webhook (CI
  "staging deploy succeeded" → opens a PR bumping prod's reference) does the diffing
  and PR creation; a required reviewer merges. This is the common default — it
  removes manual copy-paste error while keeping a human gate before prod.
  A small script comparing the `images:` blocks across the environment directories can
  generate this PR. Flux's image automation (`ImagePolicy` plus `ImageUpdateAutomation`) is the
  documented way to have a controller commit and push image updates to Git on a branch you
  choose, which fits the dev-to-staging step.
- **Fully automated (no human gate)**: acceptable for dev→staging, where blast
  radius is low and fast feedback matters more than a review step. Rarely
  appropriate for staging→prod — reserve for teams with strong automated
  verification (SLO-gated canary analysis via Argo Rollouts `AnalysisTemplate` or
  Flagger) standing in for the human judgment call.
- **Fully manual**: a human edits the prod file and opens the PR by hand — fine at
  small scale, but nothing stops someone from promoting a digest that was never
  actually deployed to staging; pair with a CI check that verifies the promoted
  digest previously existed in the staging file's git history.

## 3. Bake time
"Bake time" = a deliberate minimum dwell period in staging (or a canary slice of
prod) before promotion is allowed, to surface issues that only appear under real
traffic/time (memory leaks, periodic job failures, cache warm-up regressions).
Enforce it as a CI gate on the promotion PR (checking the staging deploy's
timestamp/age), not as a verbal policy — verbal bake-time policies get skipped under
deadline pressure, which is exactly when the skipped bake time was most needed.

## 4. Rollback = revert, not rebuild
Because promotion is a git commit, rollback is `git revert` of the promotion commit
(or the prior digest pasted back in) — Argo CD/Flux reconcile the prior state
automatically once the revert lands. This is faster and safer than redeploying an
old build artifact by hand, and it's why digest/tag pinning in step 1 matters: a
floating tag can't be reverted to reliably because it may have moved since.

## Gotchas
- Promoting a chart/app whose `values.yaml` differs meaningfully between envs
  (not just replicas/limits but actual feature flags) means "promotion" isn't a
  pure tag bump — audit what's actually allowed to differ per env before assuming a
  single-field bump is sufficient; large values drift between envs usually means the
  envs aren't really testing the same configuration.
- A promotion PR that touches the tag **and** an unrelated config change in the same
  commit defeats traceability — keep promotion PRs mechanical/single-purpose; bundle
  config changes through the normal dev→staging→prod path on their own.
- Canary/progressive delivery (Argo Rollouts, Flagger) changes what "promoted" means
  mid-rollout — a promotion PR during an in-flight canary can race with the
  rollout's own promote/abort decision; coordinate rather than assuming they're
  independent.
- Multi-service promotions (promoting 3 services that must move together) need an
  explicit convention (one PR touching all three, or a release-train tag) — ad hoc
  per-service promotion PRs can land out of order and create a prod state nothing
  in staging ever actually ran.

## Verify
- [ ] The digest/tag in a promotion PR matches, byte for byte, what's currently
      deployed in the environment being promoted *from* — not a different, newer
      build that happened to land in between.
- [ ] Reverting a promotion commit actually restores the prior working state
      end-to-end (test this once, deliberately, before relying on it under pressure).
- [ ] Bake-time and any canary-analysis gates are enforced by CI/the rollout
      controller, not by a policy doc nobody checks.
- [ ] A promotion PR's diff is scoped to the reference bump alone — no incidental
      unrelated changes riding along.

## Checked

Checked 2026-10-27. Documentation checked: Argo CD best-practices page (master), Flux image update automation guide (website main), kustomize `images` example and `api/types/image.go` (master), Argo Rollouts analysis docs (master). Confirmed: kustomize `images` entries support `name`, `newName`, `newTag` and `digest` (digest wins over `newTag`); Flux `ImagePolicy` and `ImageUpdateAutomation` commit image updates to Git; a separate config repository is recommended by Argo CD; a failed Rollouts analysis aborts the rollout. Fixed: the `ociRef digest` field mention (not a documented field) and the unsupported suggestion that Argo CD Application diffs generate promotion PRs. Process guidance (bake time, bot-authored PRs, revert as rollback) is design advice and not a factual claim about a tool.

Method: documentation only; no commands were run.
