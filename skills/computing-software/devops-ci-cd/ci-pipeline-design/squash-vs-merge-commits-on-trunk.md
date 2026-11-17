---
id: computing-software.devops-ci-cd.ci-pipeline-design.squash-vs-merge-commits-on-trunk
name: squash-vs-merge-commits-on-trunk
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, squash-vs-merge-commit, trunk-merge-policy, trunk-based-development]
level: practitioner
status: docs-checked
description: "Pick a trunk merge policy (squash, rebase, merge commit) for bisectability, conventional-commit changelogs and revertability; enforce it in repo settings."
sources: ["https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github", "https://docs.gitlab.com/user/project/merge_requests/methods/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Squash vs merge commits and rebase policy

| Method | History | Revert | Gotchas |
|---|---|---|---|
| Squash merge | one commit per PR on trunk | `git revert <sha>` reverts the PR | PR title becomes the commit subject (make it conventional) |
| Rebase merge | PR commits replayed linearly | revert several commits | every commit must build (bisect) |
| Merge commit | non-linear, PR commits + merge commit | `git revert -m 1 <merge>` | noisy log, harder bisect |

## Recommendation for trunk-based teams
Squash merge by default:
- Linear, one-change-per-commit trunk, so `git bisect` lands on a PR.
- Commit-message tooling that reads conventional subjects sees one subject per PR.
- WIP commits ("fix typo") vanish.
Use rebase merge where commits are deliberately curated (kernel-style projects).

## Enforce
GitHub: in the repository settings allow only the merge method you want (squash and merge, rebase and merge or merge commit).
GitLab: project merge request settings: Merge method "Fast-forward merge"; Squash commits when merging "Require" (squashing is always performed). With GitLab's default merge method a separate merge commit is still created, even when squashing.
Lint PR titles in CI since titles become commit subjects.

## Gotchas
- GitHub's rebase and merge re-writes the commit history on the base branch with new commits, so the commit SHAs change.
- Stacked PRs with squash require rebasing children after the parent lands.

## Verify
- [ ] Trunk `git log --oneline` shows one conventional commit per PR; bisect works.

## Checked

2026-10-28. Confirmed: GitHub merge methods page (rebase and merge adds commits individually without a merge commit and re-writes history on the base branch with new commits); GitLab merge methods page (merge commit, semi-linear, fast-forward options; squash Do not allow / Allow / Encourage / Require; default merge commit even when squashing). Removed: release-please, semantic-release and the PR-title action names, the GitHub ruleset and message settings, and the co-author and commit-signing claims (not in the sources). Corrected: GitLab squash still creates a merge commit under the default merge method.

Method: documentation only; no commands were run.
