---
id: computing-software.software-engineering.git.interactive-and-partial-staging
name: interactive-and-partial-staging
category: computing-software
field: software-engineering
product: git
tags: [git, git-tools, git-add-patch, interactive-staging, add-p, hunk-splitting, atomic-commits, git-add-i, intent-to-add]
level: practitioner
status: gated
description: "Split a messy working tree into focused commits with git add -p: hunk commands, splitting and editing hunks, staging new files and checking the result."
sources: ["https://git-scm.com/book/en/v2/Git-Tools-Interactive-Staging", "https://git-scm.com/docs/git-add#_interactive_mode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interactive and partial staging

**Goal:** turn an afternoon of mixed changes (bug fix + refactor + debug prints) into
small commits that each do one thing, so review, revert and bisect stay easy.

## git add -p hunk commands
```
y stage hunk        n skip hunk         q quit
a stage rest of file  d skip rest of file
s split hunk into smaller hunks (only if unchanged lines separate them)
e edit hunk manually        / search hunks by regex     ? help
```
- `e` opens the hunk: to NOT stage a `+` line delete it; to NOT stage a `-` line change
  `-` to a space. Do not touch context lines or the hunk header; Git recounts.
- `git add -p path/` limits to a path. `git reset -p` and `git restore -p` / `git
  stash -p` use the same interface to unstage, discard or stash selectively.

## New files
`add -p` ignores untracked files (checked). Use intent-to-add first (then it offers "Stage addition"):
```bash
git add -N new_module.py
git add -p new_module.py
```

## Workflow for splitting work
1. `git diff` to see everything. Decide the commit sequence (usually refactor first,
   then behaviour change).
2. `git add -p`, take only hunks for commit 1.
3. `git diff --cached` to review exactly what will be committed; `git diff` for the rest.
4. Test that the staged state builds on its own:
   `git stash push --keep-index -u && run-tests && git stash pop`.
5. Commit, repeat.

## Gotchas
- Whitespace-only noise makes hunks unsplittable; consider committing a formatter run
  separately first.
- `git commit -a` after careful staging stages everything again. Use plain `git commit`.
- GUI tools (`git gui`, VS Code, lazygit, tig) do line-level staging with less friction;
  same concepts.

## Verify
- [ ] Each commit's `git show --stat` touches only files related to its message.
- [ ] Every intermediate commit builds (`git rebase -x 'make test' main` to check a series).

> Review note: some commands in this skill (Git Credential Manager, exiftool/pandoc textconv, signed tags, the `e` hunk-edit recipe) were not run during review. (gated: unconfirmed, source is paywalled or blocked)
