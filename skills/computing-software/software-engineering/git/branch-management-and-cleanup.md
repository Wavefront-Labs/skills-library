---
id: computing-software.software-engineering.git.branch-management-and-cleanup
name: branch-management-and-cleanup
category: computing-software
field: software-engineering
product: git
tags: [git, branch-management, delete-branches, git-branch, merged-branches, stale-branches, git-branching]
level: practitioner
status: verified
description: "List, rename and delete local branches safely: --merged/--no-merged, -d vs -D, cleaning branches whose upstream is gone, squash-merged branches, and recovering a deleted one."
sources: ["https://git-scm.com/book/en/v2/Git-Branching-Branch-Management", "https://git-scm.com/docs/git-branch", "https://git-scm.com/docs/git-for-each-ref"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Branch management and cleanup

**Goal:** keep a short, meaningful branch list without deleting unmerged work.

## Listing
```bash
git branch -vv                       # last commit + upstream + ahead/behind
git branch --merged main             # fully contained in main: safe to delete
git branch --no-merged main          # still has unique commits
git branch -a --sort=-committerdate  # newest first, include remotes
git for-each-ref --sort=committerdate refs/heads \
  --format='%(committerdate:short) %(refname:short) %(upstream:track)'
```

## Renaming
```bash
git branch -m old new                # rename local
git branch -m master main            # then update the remote:
git push -u origin main && git push origin --delete master
```
On the host, change the default branch before deleting the old one; collaborators run
`git fetch --prune && git branch -u origin/main main`.

## Deleting
```bash
git branch -d feature/x              # refuses if not merged into HEAD or its upstream
git branch -D feature/x              # force; only when you know the commits are elsewhere
```
`-d` checks merge into the current branch (or upstream), so run it from `main`.

### Branches whose remote is gone
```bash
git fetch --prune
git branch -vv | awk '/: gone]/{print $1}' | xargs -r git branch -d
```
Use `-d` first: squash- or rebase-merged branches are not "merged" by ancestry, so `-d`
refuses them. Verify each with `git log main..branch` or `git cherry main branch`
(lines starting `-` mean an equivalent patch is already upstream), then `-D`.

## Recovering a deleted branch
Deletion prints the tip (`Deleted branch x (was 1a2b3c4)`). Otherwise:
```bash
git reflog | grep -A1 "checkout: moving from x to"   # the entry BELOW the checkout line is x's last commit
git branch x <sha-of-that-entry>   # the sha on the checkout line itself is where HEAD went next (e.g. main)
```
Reflog entries expire (default 90 days reachable, 30 days unreachable).

## Verify
- [ ] `git branch --no-merged main` reviewed before any `-D`.
- [ ] No local branch tracks a `gone` upstream.

## Checked
- Git 2.46.2 with a bare origin: `--merged`/`--no-merged`, `-vv`, `for-each-ref` and `--sort=-committerdate` output; `-d` refuses an unmerged branch and a squash-merged one while `git cherry main sq` prints `-`; the `: gone]` awk pipeline lists branches whose remote was pruned (and `-d` still refused an unmerged one); `push origin --delete` after a rename; recovery from `git reflog` works only with the entry below the `checkout: moving from x to main` line (see the corrected recipe); `gc.reflogExpire` is documented as 90 days.
