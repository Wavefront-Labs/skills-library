---
id: computing-software.software-engineering.git.commit-templates-and-prepare-commit-msg
name: commit-templates-and-prepare-commit-msg
category: computing-software
field: software-engineering
product: git
tags: [git, commit-template, prepare-commit-msg, commit-msg-hook, ticket-id-prefix, git-hooks]
level: practitioner
status: verified
description: "Guide commit messages with commit.template, insert ticket IDs via prepare-commit-msg, validate with commit-msg, and share hooks via core.hooksPath."
sources: ["https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration", "https://git-scm.com/docs/githooks#_prepare_commit_msg", "https://git-scm.com/docs/git-config#Documentation/git-config.txt-committemplate"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Commit templates and prepare-commit-msg

**Goal:** better commit messages by default: a template that prompts for the why, a
ticket ID inserted automatically, and a check that rejects bad messages.

## commit.template
```
# .gitmessage (repo root)
# <type>(<scope>): <summary, imperative, <=50 chars>
#
# Why is this change needed?
#
# Refs: 
```
```bash
git config commit.template .gitmessage        # per repo (relative to repo root)
git config --global commit.template ~/.gitmessage
```
Lines starting with `#` are stripped (`core.commentChar`). The template is used only when
the editor opens; `git commit -m` bypasses it.

## prepare-commit-msg: insert ticket from branch name
Runs before the editor opens. Args: `$1` message file, `$2` source (`message`,
`template`, `merge`, `squash`, `commit`), `$3` sha for amend.
```sh
#!/bin/sh
# .githooks/prepare-commit-msg
case "$2" in merge|squash|commit) exit 0 ;; esac   # leave merges and amends alone
ticket=$(git rev-parse --abbrev-ref HEAD | grep -oE '[A-Z]+-[0-9]+' | head -1)
[ -n "$ticket" ] || exit 0
grep -q "$ticket" "$1" || { sed -i.bak "1s/^/$ticket: /" "$1"; rm -f "$1.bak"; }
```
`sed -i.bak` keeps it portable between GNU and BSD sed.

## commit-msg: validate
Runs after the message is written; non-zero exit aborts the commit.
```sh
#!/bin/sh
# .githooks/commit-msg
head -1 "$1" | grep -qE '^([A-Z]+-[0-9]+: )?(feat|fix|docs|refactor|test|chore|perf)(\(.+\))?!?: .{1,72}$' || {
  echo "commit-msg: use Conventional Commits, e.g. 'fix(parser): handle empty input'" >&2
  exit 1; }
```
The optional `[A-Z]+-[0-9]+: ` prefix is required when the hook above is active: without it the
prefilled ticket makes `ABC-123: fix: x` fail a plain Conventional Commits regex (hit when run).
Or use commitlint via the pre-commit framework (`stages: [commit-msg]`).

## Sharing hooks
Hooks in `.git/hooks` are not versioned. Commit them in `.githooks/` and:
```bash
git config core.hooksPath .githooks && chmod +x .githooks/*
```
Add that line to your bootstrap script; hooks are client-side and skippable
(`--no-verify`), so enforce the rule again in CI or a server-side hook.

## Verify
- [ ] On branch `feature/ABC-123-x`, `git commit` opens the editor with `ABC-123: ` prefilled.
- [ ] `git commit -m "wip"` is rejected locally and the same rule runs in CI.
