---
id: computing-software.software-engineering.git.splitting-a-commit
name: splitting-a-commit
category: computing-software
field: software-engineering
product: git
tags: [git, split-commit, interactive-rebase, reset-head, add-patch, atomic-commits, rewriting-history]
level: practitioner
status: verified
description: "Split one commit into several focused commits during interactive rebase: mark edit, reset HEAD^, stage hunks with add -p, recommit, and verify every intermediate commit builds."
sources:
  - https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History
  - https://git-scm.com/docs/git-rebase
  - https://git-scm.com/docs/git-add
  - https://git-scm.com/docs/git-reset
  - https://git-scm.com/docs/git-commit
  - https://git-scm.com/docs/git-stash
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Splitting a commit

**Goal:** turn a "refactor + feature + typo" commit into separate reviewable,
bisectable commits.

## Recipe
```bash
git rebase -i <commit>^          # parent of the commit to split (or origin/main for a branch)
# change 'pick' to 'edit' (e) on that commit, save
git reset HEAD^                  # undo the commit, keep its changes unstaged (mixed reset)
git add -p src/parser.py         # stage hunks for the first logical change
git commit -m "Extract tokenize() from parse()"
git add -p                       # next change
git commit -m "Support escaped quotes in tokenizer"
git add -A && git commit -m "Fix typo in README"
git rebase --continue
```
For the HEAD commit, no rebase needed: `git reset HEAD^` and recommit.

## Hunk staging tips
- In `add -p`: `s` splits the current hunk into smaller hunks, `e` edits it manually, `?` shows help.
- New files: `git add -N file` (intent to add) first, then `add -p` works on them.
- Keep the original message and authorship for the first piece with
  `git commit -C ORIG_HEAD` (`reset` sets `ORIG_HEAD` to the old tip; `-C` reuses the
  message and authorship information, including the timestamp).

## Make each piece build
Partial staging can produce commits that never existed as a working tree. Check them:
```bash
git stash push --keep-index -u   # hide unstaged changes, test exactly what is staged
make test && git commit ...
git stash pop
# afterwards, test every commit on the branch:
git rebase -x 'make test' origin/main
```

## Gotchas
- New commits get the current time as author date unless you reuse a commit with `-C`; the first piece can keep the original via `-C ORIG_HEAD`.
- If you get lost: `git rebase --abort`, or after finishing, `git reflog` / `ORIG_HEAD`.
- Already pushed: needs `git push --force-with-lease` and reviewer awareness.

## Verify
- [ ] `git log --stat <base>..HEAD` shows one concern per commit.
- [ ] `git rebase -x '<test cmd>' <base>` passes.
- [ ] `git diff <backup-ref> HEAD` empty: the split changed no content.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22). Confirmed: the SPLITTING COMMITS procedure in git-rebase (`rebase -i <commit>^`, `edit`, `git reset HEAD^`, stage with `git add`, commit, continue); `rebase -x` / `--exec`; `git add -p` hunk commands `s` and `e`; `git add -N`; `git reset` sets `ORIG_HEAD`; `git commit -C` reuses message and authorship; `git stash push --keep-index --include-untracked`. Removed as unconfirmed: the description of hand-editing hunks (turning `-` lines into context) and the `/tmp/msg` message-saving recipe.

2026-11-01, run with Git 2.46.2 (Windows, Git Bash) in throwaway repos with a local bare remote. Confirmed: `reset HEAD^` leaves the changes unstaged and sets `ORIG_HEAD` to the old tip; `git add -N` makes a new file visible to `add -p`; `git commit -C ORIG_HEAD` reuses message and author; `stash push --keep-index -u` and `stash pop`; the final tree equals the original commit (`git diff <orig> HEAD` empty); `git rebase -x` passes; `rebase -i` with `edit` stops at the marked commit and `--abort` returns. Interactive `add -p` keys `s` and `e` are docs only.

Method: documentation checked, then the commands were run as above (Git 2.46.2, local repositories only).
