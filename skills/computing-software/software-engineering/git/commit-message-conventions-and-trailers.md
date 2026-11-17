---
id: computing-software.software-engineering.git.commit-message-conventions-and-trailers
name: commit-message-conventions-and-trailers
category: computing-software
field: software-engineering
product: git
tags: [git, distributed-workflows, commit-messages, conventional-commits, git-trailers, signed-off-by, co-authored-by, changelog]
level: practitioner
status: verified
description: "Write commit messages that survive history spelunking: 50/72 format, imperative subject, why-not-what body, Conventional Commits and machine-readable trailers."
sources:
  - https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project
  - https://www.conventionalcommits.org/en/v1.0.0/
  - https://git-scm.com/docs/git-interpret-trailers
  - https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Commit message conventions and trailers

**Goal:** a log you can read in `git log --oneline`, search with `git log --grep`, and feed to changelog and release tools.

## 1. Shape (the 50/72 rule)
```
Fix connection leak when TLS handshake times out

The pool returned the socket to the idle list before the handshake
finished, so a timed-out handshake left a half-open connection that
the next caller received. Close the socket on any handshake error.

Fixes: #4182
Signed-off-by: Ana Ruiz <ana@example.com>
```
- Subject: imperative mood ("Fix", not "Fixed"/"Fixes"), about 50 chars, hard limit 72, no trailing period.
- Blank line, then a body wrapped at 72 explaining **why** and the user-visible effect; the diff already says what.
- One logical change per commit; if the subject needs "and", split it.

## 2. Conventional Commits (when the project uses it)
```
feat(api)!: drop v1 pagination parameters

BREAKING CHANGE: `page` and `per_page` are removed; use `page_token`.
```
- Types: `feat` (minor bump), `fix` (patch), `!` or `BREAKING CHANGE:` footer (major); `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `chore` do not bump.
- Enforce with commitlint in a `commit-msg` hook or CI; generate releases with semantic-release / release-please.
- Squash-merge projects: the PR title becomes the commit subject, so lint the PR title.

## 3. Trailers
Trailers are `Key: value` lines in the last paragraph. Git can add and parse them:
```bash
git commit -s                                         # Signed-off-by
git commit --trailer "Co-authored-by: Bo Li <bo@example.com>"
git interpret-trailers --parse < msg.txt
git log --format='%(trailers:key=Fixes,valueonly)'
```
Common keys: `Signed-off-by` (DCO), `Co-authored-by` (GitHub counts it as a contribution only if the email is associated with the co-author's GitHub account; use their noreply address if private), `Reviewed-by`, `Fixes`, `Refs`, `Change-Id` (Gerrit).

## Gotchas
- A blank line inside the trailer block makes Git stop treating the earlier lines as trailers.
- A closing keyword such as `Closes #12` auto-closes the issue only when it lands on the default branch (GitHub also reads these keywords in the PR description, not only commits).
- WIP subjects like "fix" or "updates" are permanent once merged without squash; use `git commit --fixup` and autosquash instead.
- Template for the team: `git config commit.template .gitmessage`.

## Verify
- `git log --oneline -20` reads as a changelog; `git log --format=%s | awk 'length > 72'` returns nothing.
