---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.release-branching-and-cherry-picks
name: release-branching-and-cherry-picks
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [release-branching-strategy, cherry-pick-policy, release-engineering, trunk-based-development, git, hotfix]
level: practitioner
status: docs-checked
description: "Run trunk-based development with release branches cut from mainline and fixes cherry-picked from mainline only, with a written cherry-pick approval policy."
sources: ["https://sre.google/sre-book/release-engineering/", "https://trunkbaseddevelopment.com/branch-for-release/", "https://git-scm.com/docs/git-cherry-pick"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Release branching and cherry-pick policy

## What the sources say
- SRE Book (Release Engineering): Google's release tooling (Rapid) creates a release branch from a requested
  integration revision number (often taken from the continuous test system), manages release branches and
  cherry picks, and lets each cherry-pick request be approved or rejected for inclusion. Unit tests are re-run
  on the release branch with an audit trail, because with cherry picks the branch may hold a version of the
  code that exists nowhere on mainline.
- Trunk-Based Development (branch for release): teams that release monthly still need bug-fix releases, so
  they commonly cut a release branch just in time, a few days before the release. The release branch should
  not receive continued development work. The branch cut is a lightweight commit. Some teams instead
  release from a tag on the trunk and create a branch retroactively only if a fix is needed.
- Best practice there: reproduce the bug on trunk, fix it there with a test, let CI verify, then cherry-pick
  to the release branch and let CI for the release branch verify it again. The trunk pipeline is duplicated
  to guard active release branches.
- Cherry-picks go from trunk to branch only. Fixing on the release branch and planning to port it back is
  risky: forgetting means a regression in production later.
- A cherry-pick is not a regular merge: it takes specific commits and skips earlier commits made after the
  branch was cut. The page says the cherry-pick role suits one developer or pair, who polices rules (for
  example which business representative signed off), and that an audit trail of approvals can be a wiki or
  ticket system.

## Git
`git cherry-pick -x <commit>` appends "(cherry picked from commit ...)" to the message. Git's docs say this
is useful between publicly visible branches (for example backporting to a maintenance branch) and is done
only for cherry picks without conflicts; do not use it from a private branch.

## Policy to write down
Decide, in writing, what may be cherry-picked after the cut, who approves each pick, and what testing a
pick triggers (new build, re-run tests on the release branch, canary). The categories and approver roles
are your choice; the sources only establish that picks are approved individually and re-tested.

## Verify
- [ ] Every commit on the release branch traces to a mainline commit.
- [ ] Tests ran on the release branch itself, not only on mainline.

## Checked
2026-11-01. Confirmed against the SRE Book Release Engineering chapter, the trunkbaseddevelopment.com
"Branch for release" page and the git-cherry-pick manual page. Removed: invented branch names and shas,
tag and branch-cut commands, the P0/P1 allowed-fix policy text, two-approver rule, branch protection and CI
grep check, and the "more than a handful of picks" guideline, none stated on those pages.
Method: documentation only; no commands were run.
