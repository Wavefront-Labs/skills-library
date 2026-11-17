---
id: computing-software.software-engineering.git.branching-strategies-and-trunk-based-dev
name: branching-strategies-and-trunk-based-dev
category: computing-software
field: software-engineering
product: git
tags: [git, trunk-based-development, gitflow, feature-flags, branching-strategy, release-branch, ci-cd, merge-queue, short-lived-branches, continuous-integration, release-train]
level: advanced
status: draft
description: "Choose a branching strategy: trunk-based with short-lived branches and feature flags vs GitFlow release branches, and why most teams should default to trunk."
sources: ["trunkbaseddevelopment.com", "Google's engineering practices (monorepo, trunk-based at scale)", "Vincent Driessen - A successful Git branching model (GitFlow, for contrast)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Branching strategy — trunk-based by default, GitFlow only when releases demand it

**Goal:** pick a branching model that matches the release cadence, and know the
mechanics (feature flags, release branches) that make trunk-based work for
incomplete features.

## 1. Trunk-based development (default recommendation)
- Everyone merges to `main` at least daily; branches live hours to ~2 days, not weeks.
- Incomplete features ship behind a **feature flag**, dark-launched and merged
  continuously rather than kept on a long branch — this is the mechanism that makes
  "always mergeable main" compatible with "features that take weeks to build."
- CI gates every merge (tests + review) via a PR, but the PR itself is short-lived;
  this is not "commit straight to main with no review," it's "no long-lived branches."
- Requires: feature flags (LaunchDarkly, Unleash, or a simple config-driven boolean),
  fast CI (a 45-minute suite makes short-lived branches painful), and a culture of
  small PRs — a branching model doesn't fix a team that writes 2000-line PRs.

## 2. GitFlow (release branches, develop/main split)
- `develop` is the integration branch, `main` only receives tagged releases,
  `release/*` branches stabilize before a release, `hotfix/*` patches `main` directly.
- Fits teams that ship **discrete, versioned releases** on a schedule they control —
  desktop software, embedded firmware, libraries with semantic versioning and
  supported-version policies — where "cut a release branch, stabilize for a week,
  ship" is the actual process, not an artifact of the branching model.
- Cost: `develop` and `main` diverge, merge conflicts compound the longer a feature
  branch lives, and "which branch has this fix" becomes its own tracking problem.
  Most web/SaaS teams that adopt GitFlow by default (because it was once the famous
  blog post) are paying this cost for no release-cadence reason.

## 3. The actual decision
Ask: "can we deploy to production the moment a change merges?" If yes (most
continuously-deployed services), trunk-based is strictly less overhead. If no — you
genuinely maintain multiple supported versions concurrently (v1.x security patches
while building v2) — a release-branch model earns its complexity, but it can still be
layered ON TOP of trunk-based main-branch development (release branches cut from
main at release time, cherry-picked hotfixes back), rather than full GitFlow's
permanent `develop`.

## 4. Mechanics that make trunk-based safe
- **Merge queue** (GitHub merge queue, Mergify, Bazel's) — re-tests each PR against
  the latest main immediately before merging, catching "my branch passed CI but main
  moved" races that plain "tests pass on the PR" misses.
- **Feature flags with a kill switch** — a broken dark-launched feature gets disabled
  in seconds (flag flip) instead of requiring a revert-and-redeploy.
- **Stacked/short PRs** — break a multi-week feature into mergeable slices behind a
  flag rather than one branch that lives for the whole feature; review quality drops
  sharply on big diffs regardless of branching model.
- **Branch protection**: require status checks + at least one review before merge to
  `main`, even with trunk-based's short branch lifetimes — "short-lived" isn't
  "unreviewed."

## Gotchas
- Flags left in code after full rollout accumulate as dead conditionals — a flag
  needs a removal step in the same tracking system as the rollout, or the codebase
  fills with permanent `if (flagEnabled)` branches nobody dares delete.
- A long-lived branch under either model rots: resolve conflicts against main at
  least every day or two, never "right before merging three weeks later."
- Release branches without a clear cherry-pick policy become a second place bugs get
  fixed and silently never make it back to main.

## Verify
- [ ] The chosen model matches the actual deploy cadence (continuous vs versioned
      releases), not habit or what a past employer used.
- [ ] No branch (feature or release) has been open for longer than the team's stated
      target without an explicit reason.
- [ ] Incomplete trunk-based work is gated by a flag with a tracked removal date, not
      a branch kept open "until it's ready."
- [ ] Merge queue or equivalent re-test-before-merge is in place if merge volume is
      high enough for main to move between a PR's CI run and its merge.

Related: computing-software.software-engineering.git.rebase-and-history-repair,
computing-software.software-engineering.code-review.reviewing-a-diff
