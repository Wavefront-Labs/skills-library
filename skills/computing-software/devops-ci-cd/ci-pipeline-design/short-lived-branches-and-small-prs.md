---
id: computing-software.devops-ci-cd.ci-pipeline-design.short-lived-branches-and-small-prs
name: short-lived-branches-and-small-prs
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, trunk-based-development, short-lived-branches, small-prs, stacked-prs, feature-flags, branch-by-abstraction, pr-size, review-latency, merge-frequency, dora]
level: practitioner
status: docs-checked
description: "Run trunk-based development day to day: branches merged within a day or two, small PRs, stacked PRs, flags and branch-by-abstraction for big work, and metrics to enforce it."
sources: ["https://trunkbaseddevelopment.com/short-lived-feature-branches/", "https://dora.dev/capabilities/trunk-based-development/", "https://google.github.io/eng-practices/review/developer/small-cls.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Short-lived branches and small PRs

DORA's trunk-based capability: three or fewer active branches, branches merged to trunk
at least daily, no code freezes. In practice that means **branches live hours to two
days** and **PRs are small**.

## Size targets
- A PR does one thing: one refactor, *or* one behaviour change, *or* one dependency bump.
- Keep PRs small enough to review in one sitting; agree a team target for lines changed (excluding generated files and lockfiles).
- Separate pure moves/renames/formatting into their own PR so the logic diff is readable.

## How to keep work small when the feature is big
1. **Feature flags**: merge incomplete code dark (`if flags.enabled("new-checkout")`);
   release is a flag flip, not a merge.
2. **Branch by abstraction**: introduce an interface, move callers to it, build the new
   implementation behind it, switch, delete the old one; every step is a mergeable PR.
3. **Expand / contract** for schemas and APIs (add new, migrate, remove old).
4. **Stacked PRs**: PR2 based on PR1's branch; keep the stack rebased and merge bottom-up.
5. Ship the tests/scaffolding first, behaviour second.

## Workflow habits
- Branch from fresh main; rebase on main (`git pull --rebase`) at least daily.
- Open a **draft PR early** to get CI and visibility; mark ready when small and green.
- Review SLA: first review within a few working hours. Small PRs only stay small if
  they're reviewed fast; otherwise people batch.
- Delete branches on merge (repo setting) and clean up stale ones.

## Measure it
- Branch age at merge (p50/p90), PR size (lines changed), time to first review, PRs merged
  per dev per week. Pull from the GitHub/GitLab API; alert on branches older than N days.
- Lead time for changes (DORA) improves when these do; don't game with trivial PRs.

## Anti-patterns
- Long-lived `develop`/feature branches with "integration day" merges.
- "Just one more thing" PRs that grow over a week.
- Flag debt: every flag gets an owner and a removal ticket.

## Verify
Over a month, p90 branch age < 2 days and p90 PR size within your team target; merge conflicts and
"main is red" incidents trend down.

## Checked

2026-10-28. Confirmed: DORA trunk-based development page (three or fewer active branches, merge to trunk at least once a day, no code freezes), trunkbaseddevelopment.com (short-lived branches last a couple of days, beyond two days they risk becoming long-lived), Fowler's Parallel Change page (branch by abstraction, expand and contract), git-pull manual (`--rebase`). Removed: the 200-400 line figure and review-quality claim, the stacked-PR tool names, `git fetch --prune` and `git switch`.

Method: documentation only; no commands were run.
