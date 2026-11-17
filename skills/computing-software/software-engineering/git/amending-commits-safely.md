---
id: computing-software.software-engineering.git.amending-commits-safely
name: amending-commits-safely
category: computing-software
field: software-engineering
product: git
tags: [git, git-commit-amend, amend-commit, fixup, reset-author, force-with-lease, commit-message]
level: practitioner
status: verified
description: "Fix the last commit's content, message or author with git commit --amend, and when amending is unsafe because the commit is already shared."
sources: ["https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things", "https://git-scm.com/docs/git-commit", "https://git-scm.com/docs/git-push#Documentation/git-push.txt---force-with-leaseltrefnamegt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Amending commits safely

**Goal:** tidy the commit you just made (forgotten file, typo in message, wrong author
email) without creating a "fix typo" commit, and without breaking anyone else's clone.

## Recipes
```bash
git add forgotten_file.py && git commit --amend --no-edit   # add content, keep message
git commit --amend -m "Fix race in cache eviction"           # replace message
git commit --amend --reset-author --no-edit                  # after fixing user.email
git commit --amend --date=now --no-edit                      # refresh author date
```
To fix an OLDER commit, do not amend; create a fixup and autosquash:
```bash
git commit --fixup=<sha>
git rebase -i --autosquash <sha>~1
```

## The rule: amend only unpublished commits
Amend creates a NEW commit (new sha). If the old one was pushed:
- Your push is rejected as non-fast-forward.
- Forcing it rewrites the branch for everyone who pulled.

On your own feature branch (nobody else commits to it) that is acceptable:
```bash
git push --force-with-lease --force-if-includes
```
`--force-with-lease` refuses if the remote moved since your last fetch, so you cannot
erase a teammate's push. Plain `--force` can. Never force-push a shared branch such as
`main`; protect it server-side.

## Recovering from a bad amend
The pre-amend commit is in the reflog: `git reflog` shows `commit (amend)`; the entry
before it is the original. `git reset --soft HEAD@{1}` puts you back with the amend's
changes staged.

## Gotchas
- `--amend` with something accidentally staged silently folds it in. Run
  `git status` / `git diff --cached` first.
- Amending a merge commit keeps both parents; fine, but amending during an
  in-progress rebase amends the commit being replayed, not the one you think.
- Signed commits lose their signature on amend unless signing is automatic (`commit.gpgsign=true`).

## Verify
- [ ] `git show --stat HEAD` shows the intended files and message.
- [ ] If pushed before, the force push used `--force-with-lease`.

## Checked
- Git 2.46.2: `--amend --no-edit` with a newly added file, `-m`, `--reset-author` (new email) and `--date=now` work; `--fixup` plus `rebase -i --autosquash` folded the fix into the older commit; pushing an amended commit is rejected (`non-fast-forward`) and `--force-with-lease --force-if-includes` pushes it; the reflog shows `commit (amend)` and `reset --soft HEAD@{1}` returns to the pre-amend commit; amending during a rebase `edit` stop changes the commit being replayed. A teammate-push rejection by `--force-with-lease` was not reproduced.
