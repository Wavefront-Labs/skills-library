---
id: computing-software.software-engineering.git.client-side-hooks-and-pre-commit
name: client-side-hooks-and-pre-commit
category: computing-software
field: software-engineering
product: git
tags: [git, git-customization, git-hooks, pre-commit-hooks, pre-commit-framework, commit-msg, core-hookspath, husky, lefthook]
level: practitioner
status: verified
description: "Automate local checks with client-side Git hooks: hook types, sharing via core.hooksPath, the pre-commit framework, and keeping hooks fast and skippable."
sources:
  - https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
  - https://git-scm.com/docs/githooks
  - https://pre-commit.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client-side hooks and the pre-commit framework

**Goal:** catch formatting, lint and secret mistakes before they leave the developer's machine, without slowing commits to a crawl.

## 1. Hook types that matter
| Hook | When | Typical use |
|---|---|---|
| `pre-commit` | before the message editor | format/lint staged files, secret scan |
| `prepare-commit-msg` | before editor opens | prefill ticket id from branch name |
| `commit-msg` | after message written | enforce Conventional Commits |
| `pre-push` | before objects are sent | run fast tests, block pushes to main |
| `post-checkout`, `post-merge` | after switching / pulling | reinstall deps if lockfile changed |

Hooks are executables in `.git/hooks/` (not versioned); non-zero exit aborts the operation (for `pre-*` and `commit-msg`).

## 2. Share hooks with the repo
```bash
mkdir .githooks && git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
```
Example `commit-msg`:
```sh
#!/bin/sh
grep -qE '^(feat|fix|docs|refactor|perf|test|build|ci|chore)(\(.+\))?!?: .{1,72}$' "$1" || {
  echo "commit message must follow Conventional Commits" >&2; exit 1; }
```

## 3. The pre-commit framework
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks: [{id: trailing-whitespace}, {id: end-of-file-fixer}, {id: check-added-large-files}]
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.0
    hooks: [{id: ruff, args: [--fix]}, {id: ruff-format}]
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.0
    hooks: [{id: gitleaks}]
```
```bash
pip install pre-commit && pre-commit install --hook-type pre-commit --hook-type commit-msg
pre-commit run --all-files     # first run and in CI
pre-commit autoupdate          # bump pinned revs
```
It runs only on staged files, stashes unstaged changes during the run, and caches tool environments.
JS projects often use husky + lint-staged or lefthook for the same job.

## Gotchas
- Hooks are advisory: anyone can `git commit --no-verify`. Repeat the checks in CI (`pre-commit run --all-files`).
- Keep `pre-commit` under a few seconds; move test suites to `pre-push` or CI.
- Hooks run with the repo root as cwd and a minimal environment in GUI clients; use absolute tool paths or the framework's managed envs.
- Windows: hooks need a shebang and run under Git's bundled sh.

## Verify
- Stage a file with trailing whitespace and a fake AWS key: the commit is blocked with clear messages, and `--no-verify` bypasses only locally.
- Checked: `pre-commit install --hook-type pre-commit --hook-type commit-msg` writes both hooks into `.git/hooks`; pinned revs v5.0.0 (pre-commit-hooks), v0.7.0 (ruff-pre-commit) and v8.21.0 (gitleaks) exist as tags (they are old: run `pre-commit autoupdate`).
