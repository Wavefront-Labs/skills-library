---
id: computing-software.software-engineering.git.fast-forward-no-ff-and-squash-merges
name: fast-forward-no-ff-and-squash-merges
category: computing-software
field: software-engineering
product: git
tags: [git, fast-forward, no-ff, squash-merge, ff-only, merge-commit, rebase-merge, pull-request-merge, linear-history]
level: practitioner
status: verified
description: "Choose between fast-forward, --no-ff merge commits, squash merges and rebase-merge, and set pull.ff / merge.ff so the history shape is deliberate."
sources: ["https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging", "https://git-scm.com/docs/git-merge#_fast_forward_merge", "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fast-forward, --no-ff and squash merges

**Goal:** pick a history shape on purpose and enforce it, instead of getting whatever
each developer's defaults produce.

## The options
| Method | Command | History result |
|---|---|---|
| Fast-forward | `git merge --ff-only feature` | Branch pointer moves; no merge commit; fails if diverged. |
| Merge commit | `git merge --no-ff feature` | Always a merge commit; feature's commits kept, grouped. |
| Squash | `git merge --squash feature && git commit` | One new commit; feature's commits not ancestors. |
| Rebase-merge | `git rebase main feature && git merge --ff-only feature` | Linear, each commit kept. |

## Trade-offs
- **--no-ff**: `git log --first-parent main` reads as one entry per feature; reverting a
  feature is one `git revert -m 1`. Cost: busier graph.
- **Squash**: clean main, one commit per PR, easy revert. Cost: the branch is not
  recognised as merged (`git branch --merged` lies, `git branch -d` refuses), and
  continuing work on the same branch after a squash causes repeat conflicts. Delete the
  branch after squash-merging.
- **Rebase-merge**: linear and bisectable at fine grain, but each commit must build;
  rewrites shas so signatures/CI results on the branch no longer match.
- **ff-only**: a safe default for `pull`; it refuses to create surprise merge commits.

## Configure defaults
```bash
git config --global pull.ff only        # git pull fails instead of making a merge when diverged
git config --global merge.ff false      # make every local merge --no-ff (maintainer style)
git config --global pull.rebase true    # alternative: rebase local commits on pull
```
On GitHub/GitLab enable only the merge methods you want in repository settings and
require linear history via branch protection if you choose squash/rebase.

## Gotchas
- `git pull` with no config on divergent branches errors (`fatal: Need to specify how to reconcile divergent branches`, tested on 2.46.2) and asks you to
  choose; set `pull.ff only` or `pull.rebase`. Git for Windows installs `pull.rebase=false` at system level, so it merges silently there.
- A squash commit message defaults to the concatenated commit list; edit it into a
  real description.

## Verify
- [ ] `git log --graph --oneline -20 main` matches the team's stated policy.
- [ ] Repo settings allow only the chosen merge methods.

## Checked
- Git 2.46.2: `--ff-only` fast-forwards and fails with `Not possible to fast-forward, aborting` when diverged; `--no-ff` gives a merge commit that `log --first-parent` shows as one entry; after `--squash` the branch is not in `branch --merged` and `branch -d` says `not fully merged`; `merge.ff=false` made a merge commit for a fast-forwardable branch; with no pull config on diverged branches `git pull` prints the three-option hint and `fatal: Need to specify how to reconcile divergent branches` (Git for Windows ships `pull.rebase=false` in its system config, so stock Windows installs merge silently), `pull.ff=only` fails and `pull.rebase=true` rebases. Hosting-site merge-method settings are not tested.
