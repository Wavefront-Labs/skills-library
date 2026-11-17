---
id: computing-software.qa-testing-engineering.test-automation.git-bisect-regression-isolation
name: git-bisect-regression-isolation
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [git-bisect, regression-isolation, bug-investigation, automated-bisect, first-bad-commit]
level: practitioner
status: verified
description: "Find the commit that introduced a regression with git bisect: manual and scripted runs, skip unbuildable commits, first-parent bisect on merges, and reporting."
sources:
  - https://git-scm.com/docs/git-bisect
  - https://git-scm.com/book/en/v2/Git-Tools-Debugging-with-Git
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Isolating regressions with git bisect

**Goal:** pinpoint the first bad commit in O(log n) steps, giving the developer exactly what changed.

## Manual
```bash
git bisect start
git bisect bad                 # current HEAD has the bug
git bisect good v4.1.3         # last known good tag/commit
# git checks out a midpoint: build, test, then
git bisect good    # or: git bisect bad, or git bisect skip (cannot test this commit)
# ... repeat until "<sha> is the first bad commit"
git bisect log > bisect.log    # keep for the report
git bisect reset
```
1000 commits need about 10 steps. Ran on a 20-commit scratch repo: `git bisect run` found the first bad commit, a path-limited bisect (`-- src/pricing/`) found the same commit, and `--first-parent` was accepted.

## Automated
```bash
git bisect start HEAD v4.1.3
git bisect run ./bisect-check.sh
```
Script exit codes: `0` good, `1-127` except `125` bad, `125` skip (cannot build/test), anything else (such as `130`, `>=128`) aborts the bisect (checked with Git 2.46: exit 127 counted as bad, exit 130 gave `bisect run failed`).
```bash
#!/usr/bin/env bash
npm ci --silent || exit 125
npx vitest run src/pricing/discounts.test.ts -t "stacked codes" >/dev/null 2>&1
```
Write the reproducer test before bisecting and keep it outside the repo (or untracked) so checkouts do not remove it.

## Useful options
- `git bisect start --first-parent` follows only merge commits on main: find the bad PR, then bisect inside it.
- `git bisect start --term-new fixed --term-old broken` to find when something was *fixed* (then mark with `git bisect broken` / `git bisect fixed`). `git bisect terms` only prints the terms in use; it does not set them.
- Limit to a path: `git bisect start HEAD v4.1.3 -- src/pricing/`.

## Beyond git history
Same idea for dependency upgrades (bisect lockfile changes) or for artefact builds (bisect deployed versions when builds are expensive).

## Gotchas
- Flaky reproducers send bisect the wrong way; make the check deterministic or repeat it N times inside the script.
- Build caches/node_modules from another commit cause false results; clean in the script.
- Data migrations may make old commits fail for unrelated reasons; use skip.

## Verify
Reverting the identified commit on HEAD makes the reproducer pass, and the bisect log is attached to the defect.
