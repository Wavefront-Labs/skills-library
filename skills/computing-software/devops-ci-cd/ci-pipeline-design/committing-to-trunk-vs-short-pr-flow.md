---
id: computing-software.devops-ci-cd.ci-pipeline-design.committing-to-trunk-vs-short-pr-flow
name: committing-to-trunk-vs-short-pr-flow
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, commit-to-trunk, trunk-based-development, short-lived-branches]
level: practitioner
status: docs-checked
description: "Choose between committing straight to trunk and short-lived PR branches: team size, review and compliance needs, pre-push gates and the safety net each requires."
sources: ["https://trunkbaseddevelopment.com/committing-straight-to-the-trunk/", "https://dora.dev/capabilities/trunk-based-development/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Committing straight to trunk vs short PR flow

Both are trunk-based development. The choice is about review mechanics.

| | Direct to trunk | Short-lived PR (a day or two at most) |
|---|---|---|
| Fits | small co-located teams, pairing/mob, high trust | larger teams, open source, regulated |
| Review | pairing or post-commit review | pre-merge PR review |
| Gate | local pre-push build + fast CI on trunk | CI on PR + merge queue |
| Compliance | confirm with your auditor what counts as review evidence | PR approval is a typical record |
| Risk | broken trunk visible to all fast | queueing, review latency |

## Direct-to-trunk safety net
- Pre-push hook runs the same fast checks as CI (`make check` < 5 min).
- Rebase on the latest trunk before push (`git pull --rebase`); small commits.
- CI on every trunk commit with immediate revert policy.
- Feature flags for anything incomplete.

## Short PR flow rules
- One reviewer, required; review within hours.
- Merge queue so the tested state equals what lands.
- Delete branch on merge; no branch survives two days.

## Hybrid
Protected `main` with PRs required, but allow pairs to self-approve with a "paired-with:" trailer
and an audit check (where policy allows).

## Verify
- [ ] Chosen flow documented in CONTRIBUTING; metrics (PR lifetime or trunk red time) tracked.

## Checked

2026-10-28. Confirmed against trunkbaseddevelopment.com (committing straight to the trunk: verify your own commits, optionally with a pairing partner; short-lived branches should last a couple of days at most) and the git-pull manual (`--rebase`). Removed: the specific compliance frameworks (SOX, SOC 2) tied to pairing evidence, and the 1-day figure.

Method: documentation only; no commands were run.
