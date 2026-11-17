---
id: computing-software.software-engineering.code-review.splitting-large-changes
name: splitting-large-changes
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, splitting-changes, small-cls, stacked-prs, refactor-first, incremental-delivery]
level: practitioner
status: draft
description: "Split a large change into small reviewable ones: refactor-first, by layer, by feature slice, stacked PRs, and feature flags to merge incomplete work safely."
sources: ["https://google.github.io/eng-practices/review/developer/small-cls.html", "https://www.stacking.dev/", "https://graphite.dev/docs/command-reference", "https://martinfowler.com/articles/feature-toggles.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Splitting a large change

Google "Small CLs": small changes are reviewed faster and more thoroughly, are less likely to
introduce bugs, easier to roll back and to merge. ~100 lines is usually reasonable; 1000 is usually
too large (deletions and generated code count less).

## Splitting strategies
1. **Refactor first**: separate pure refactorings (rename, move, extract) that make the feature
   easy into their own PRs, merged before the behaviour change. Reviewers check "no behaviour
   change" quickly.
2. **By layer / stack**: schema migration -> data access -> service logic -> API -> UI. Each PR
   compiles and passes tests; lower layers may be unused at first.
3. **Horizontal by feature slice**: thinnest end-to-end path first (one endpoint, one field), then
   widen.
4. **By file ownership**: split along OWNERS/CODEOWNERS so each PR needs one team.
5. **Tests and infrastructure first**: test helpers, fixtures, CI changes in their own PR.
6. **Parallel implementation behind a flag**: merge incomplete feature code disabled by a feature
   toggle; flip when complete.

## Stacked PRs
Each PR targets the previous PR's branch. Tools manage rebasing: Graphite (`gt create`, `gt submit`),
`git-branchless`, ghstack, `git rebase --update-refs` (git 2.38+) to move a whole stack at once;
GitLab supports stacked diffs via `glab stack`. Review and merge bottom-up.

## Keep each PR self-contained
- Builds and passes tests on its own; no broken intermediate states on main.
- Description explains where it fits ("Part 2/4 of #123: adds repository; not wired up yet").
- Includes its own tests.

## When it can't be split
Say so in the description and why (atomic rename across the codebase, generated code). Offer a
walkthrough and an ordered file list.
