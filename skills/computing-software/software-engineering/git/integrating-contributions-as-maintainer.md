---
id: computing-software.software-engineering.git.integrating-contributions-as-maintainer
name: integrating-contributions-as-maintainer
category: computing-software
field: software-engineering
product: git
tags: [git, integrating-contributions, topic-branches, maintaining-a-project, merge-vs-rebase, integration-branch, pu-branch]
level: advanced
status: gated
description: "Integrate contributed work as a maintainer: topic branch per contribution, review against merge-base, merge vs rebase vs squash vs cherry-pick."
sources: ["https://git-scm.com/book/en/v2/Distributed-Git-Maintaining-a-Project", "https://git-scm.com/docs/gitworkflows", "https://git-scm.com/docs/git-merge-base"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integrating contributions as a maintainer

**Goal:** accept outside work so main stays releasable, history stays readable, and
contributors keep credit.

## 1. Isolate every contribution
```bash
git fetch https://github.com/jane/project.git fix-parser
git switch -c jd/fix-parser FETCH_HEAD          # namespace: <initials>/<topic>
# or add a remote for repeat contributors: git remote add jane <url>
```
Topic branches let you test, rework or drop one contribution without touching others.

## 2. Review what it really changes
```bash
git log --oneline --no-merges main..jd/fix-parser    # commits introduced
git diff main...jd/fix-parser                        # three dots: vs merge-base, not vs main tip
git range-diff main jd/fix-parser@{1} jd/fix-parser  # after contributor force-pushes a v2
```
Two-dot `git diff main jd/fix-parser` also shows main's newer changes reversed - a classic
false alarm.

## 3. Choose how it lands
| Method | Use when | Cost |
|---|---|---|
| merge `--no-ff` | multi-commit topic with meaningful history | merge commits in log |
| rebase then ff | linear history policy, contributor's commits are clean | rewrites their hashes |
| squash merge | messy WIP commits, one logical change | loses granular bisect, attribution needs `Co-authored-by` |
| cherry-pick | taking one fix from a larger branch, backports | duplicate patch identity; use `-x` |

Keep the contributor as author in all cases (`git am`, `cherry-pick` and rebase preserve it;
hosts preserve it on squash).

## 4. Integration branches for large projects
gitworkflows: `maint` (fixes for last release) <- `master`/`main` <- `next` (testing) <- `seen`
(throw-away integration branch for topics not yet ready; it may be rewound and rebuilt, per gitworkflows). Topics merge downward only when they
graduate; fixes are made on the oldest branch that needs them and merged upward, so
`maint` fixes never require cherry-picks (gitworkflows, "Merge upwards").

## 5. After merging
```bash
git branch -d jd/fix-parser
git tag -s v2.3.1 -m "v2.3.1"            # if releasing
git shortlog -sn v2.3.0..v2.3.1           # credit in release notes
```

## Verify
- [ ] Every contribution reviewed against merge-base, tested on its topic branch.
- [ ] Author fields show contributors, not the maintainer.
- [ ] Policy (merge/rebase/squash) written in CONTRIBUTING and enforced by branch protection.

> Review note: some commands in this skill (Git Credential Manager, exiftool/pandoc textconv, signed tags, the `e` hunk-edit recipe) were not run during review. (gated: unconfirmed, source is paywalled or blocked)
