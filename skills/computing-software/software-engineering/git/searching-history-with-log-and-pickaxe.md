---
id: computing-software.software-engineering.git.searching-history-with-log-and-pickaxe
name: searching-history-with-log-and-pickaxe
category: computing-software
field: software-engineering
product: git
tags: [git, git-log, git-log-search, pickaxe, git-grep, log-l, history-search, archaeology]
level: practitioner
status: verified
description: "Find when and why code changed: git log -S/-G pickaxe, -L line history, --grep, path and author filters, and git grep across revisions."
sources:
  - https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History
  - https://git-scm.com/book/en/v2/Git-Tools-Searching
  - https://git-scm.com/docs/git-log
  - https://git-scm.com/docs/diff-options
  - https://git-scm.com/docs/git-grep
  - https://git-scm.com/docs/gitattributes
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Searching history: log filters, pickaxe and line history

**Goal:** answer "when did this appear/disappear, who changed it and why" in seconds,
without scrolling through `git log`.

## The pickaxe
```bash
git log -S 'MAX_RETRIES' --oneline          # commits where the COUNT of that string changed
git log -S 'MAX_RETRIES' -p -- src/         # with diffs, limited to a path
git log -G 'retr(y|ies)\s*=' --oneline      # regex over added/removed lines (any change)
git log -S foo --pickaxe-regex              # treat -S argument as regex
```
`-S` misses commits that only move or edit a line in place (count unchanged); `-G`
catches them but is noisier. When finding where a function was deleted, `-S` is ideal.

## Line and function history
```bash
git log -L 120,150:src/server.go            # evolution of a line range
git log -L :handleRequest:src/server.go     # evolution of a function (uses funcname regex)
git log --follow -p -- src/new_name.py      # through renames (single file only)
```
`-L` takes a line range or a function-name regex and cannot be combined with pathspec
limiters. To make `-L :func:` find function boundaries in other languages, set a built-in
diff driver in `.gitattributes` (for example `*.py diff=python`).

## Filtering
```bash
git log --author='alice' --since='2 weeks ago' --until=yesterday
git log --grep='JIRA-123' --grep='hotfix' --all-match -i   # message search
git log main..feature --oneline               # on feature, not on main
git log --first-parent main                   # follow only first parents at merges (hides the merged-in topic commits)
git log --diff-filter=D --name-only -- '*.sql'  # when were SQL files deleted
git log --format='%h %ad %an %s' --date=short
```
`--all` searches every branch; deleted code often lives only on an unmerged branch.

## git grep across revisions
```bash
git grep -n 'TODO' v1.2.0 -- '*.ts'           # search a tag's tree, no checkout
git grep -e 'oldApi' $(git rev-list --all)    # every commit (slow on big repos)
```

## Verify
- [ ] The result commit's diff (`git show <sha>`) actually contains the change.
- [ ] If nothing found on the current branch, repeated with `--all`.

Related: computing-software.software-engineering.git.blame-with-ignore-revs

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22). Confirmed in diff-options and git-log: `-S<string>` (change in occurrence count) and `-G<regex>` with `--pickaxe-regex`; `-L<start>,<end>:<file>` and `-L:<funcname>:<file>` (single starting revision, no pathspec limiters); `--follow` for a single file; `--grep` with `--all-match`; `--first-parent` semantics; `--diff-filter`; the built-in `python` diff driver in gitattributes. Corrected: the `--first-parent` comment previously said "merges only"; it follows only the first parent at merges.

2026-11-01, run with Git 2.46.2 (Windows, Git Bash) in throwaway repos with a local bare remote. Confirmed: `-S` finds only the commit where the count of the string changed while `-G` also finds the in-place edit; `-S ... --pickaxe-regex`; `-L 1,2:file` and `-L :func:file`; `-L` with a pathspec stops with `fatal: -L<range>:<file> cannot be used with pathspec`; `--follow` crosses a rename; `--author/--since/--until`; two `--grep` with `--all-match -i`; `main..feature`; `--first-parent`; `--diff-filter=D --name-only`; `--format` with `--date=short`; `git grep -n` against a tag; `git grep -e` over `git rev-list --all`.

Method: documentation checked, then the commands were run as above (Git 2.46.2, local repositories only).
