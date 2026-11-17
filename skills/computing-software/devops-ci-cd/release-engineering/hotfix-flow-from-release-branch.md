---
id: computing-software.devops-ci-cd.release-engineering.hotfix-flow-from-release-branch
name: hotfix-flow-from-release-branch
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, hotfix-flow, hotfix, release-branches]
level: practitioner
status: docs-checked
description: "Ship a hotfix for a released version: fix on trunk first and cherry-pick to the release branch (or the reverse under pressure), tagging, pipeline path and avoiding regressions."
sources: ["https://trunkbaseddevelopment.com/branch-for-release/", "https://git-scm.com/docs/git-cherry-pick"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hotfix flow from release branch to main

## Preferred: trunk first
1. Fix on `main` with a test reproducing the bug; merge normally.
2. Cherry-pick to the release branch:
   ```bash
   git checkout release/2.4
   git cherry-pick -x <sha-on-main>       # -x records "cherry picked from commit ..."
   git push origin release/2.4
   ```
3. Release pipeline builds `v2.4.1` from the release branch, runs the full test suite, deploys.
Guarantees the fix is never lost in the next release. Continuous-delivery teams that release from trunk can skip release branches and roll forward (Trunk Based Development: branch for release).

## Under severe pressure: release branch first
Fix on `release/2.4`, ship, then **immediately** open a PR porting it to `main` (tracked by a
"needs forward-port" label and a check that blocks the next release cut until resolved).

## Tooling
- Backport automation is optional; the manual path is the `git cherry-pick -x` above.
- Version: patch bump, tag on the release branch (`v2.4.1`), changelog entry under 2.4.1.

## Gotchas
- Cherry-pick conflicts because trunk diverged: resolve carefully and run tests on the release
  branch; do not "fix" by bringing extra trunk changes.
- Hotfixes that need migrations must remain compatible with the next version's migrations.
- Expedited approvals still leave an audit trail (change record, PR).

## Verify
- [ ] `git log main --grep "cherry picked from"` or the forward-port PR proves the fix is on main; v2.4.1 deployed with tests green.

## Checked

2026-10-28. Confirmed: fix production bugs on trunk first, then cherry-pick to the release branch (Trunk Based Development branch-for-release page); git cherry-pick -x records a cherry picked from line (git-cherry-pick docs). Removed: named backport bots and the GitLab cherry-pick button (not in the sources).

Method: documentation only; no commands were run.
