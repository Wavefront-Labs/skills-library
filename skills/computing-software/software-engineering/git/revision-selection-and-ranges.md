---
id: computing-software.software-engineering.git.revision-selection-and-ranges
name: revision-selection-and-ranges
category: computing-software
field: software-engineering
product: git
tags: [git, git-tools, revision-selection, commit-ranges, triple-dot, double-dot, rev-parse, ancestry, reflog-shortnames, gitrevisions]
level: practitioner
status: verified
description: "Name exactly the commits you mean: ^ vs ~, A..B vs A...B, @{u}, @{-1}, :/message, HEAD@{date}, and how ranges differ between log and diff."
sources: ["https://git-scm.com/book/en/v2/Git-Tools-Revision-Selection", "https://git-scm.com/docs/gitrevisions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Revision selection and commit ranges

**Goal:** address commits precisely so log, diff, rebase and cherry-pick act on the set
you intended.

## Single revisions
| Syntax | Means |
|---|---|
| `HEAD~3` | 3 generations back following FIRST parents |
| `HEAD^2` | second parent of a merge (the merged-in branch) |
| `HEAD^` | same as `HEAD~1` / `HEAD^1` |
| `@{u}` / `main@{upstream}` | upstream of current / named branch |
| `@{-1}` | previously checked-out branch (`git switch -` uses it) |
| `HEAD@{2}` | where HEAD was 2 moves ago (reflog, local only) |
| `main@{yesterday}` | where main pointed yesterday in THIS clone |
| `:/fix race` | youngest commit whose message matches regex |
| `v1.2.0^{commit}` | peel a tag to its commit |
| `HEAD:src/app.py` | the blob at that path in that commit |

`git rev-parse <rev>` prints the sha; use it to check what an expression resolves to.

## Ranges (log, rev-list, rebase)
| Syntax | Commits |
|---|---|
| `A..B` | reachable from B, not from A ("what's on B that A lacks") |
| `A...B` | reachable from either, not both (symmetric difference) |
| `^A B C` / `B --not A` | from B or C, excluding anything reachable from A |
| `A^!` | just commit A |
| `A^@` | all parents of A |

`git log --left-right --oneline main...feature` marks each commit `<` or `>` by side.

## Ranges mean something different in diff
- `git diff A..B` = `git diff A B` (two endpoints, not a commit set).
- `git diff A...B` = diff from merge-base(A,B) to B: "what did B change since it forked".
  This is what a PR shows. Use it for reviews.

## Gotchas
- `HEAD~2` vs `HEAD^2` look alike; one is grandparent, the other is second parent.
- Reflog-based names (`@{yesterday}`, `HEAD@{n}`) exist only in your clone.
- In PowerShell / zsh, quote `@{u}` and `^` (`'@{u}'`, `HEAD^^`) to stop shell expansion.

## Checked
Run with Git 2.46.2 on 2026-10-18 in a scratch repo with a merge: `HEAD^2` is the merged branch tip, `HEAD^` equals `HEAD~1`, `HEAD~2` is the first-parent grandparent, `main..feat` is empty once merged, `main...other` returns the symmetric difference and `--left-right` marks sides with `<` and `>`, `A^!` is one commit and `A^@` lists all parents, `:/fix race` returns the youngest matching commit, `@{-1}` is the previously checked-out branch, `^A B C` equals `B C --not A`, `git diff A..B` equals `git diff A B`, `git diff A...B` equals a diff from the merge-base to B, and `v1^{commit}` peels an annotated tag. Not re-run: `@{u}` / `main@{upstream}` (needs a remote) and reflog expiry behaviour of `@{yesterday}` (in a young clone Git returns the oldest reflog entry).

## Verify
- [ ] `git rev-list --count <range>` returns the number of commits you expected before
      feeding the range to rebase/cherry-pick.
