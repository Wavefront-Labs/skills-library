---
id: computing-software.software-engineering.git.subtree-merging
name: subtree-merging
category: computing-software
field: software-engineering
product: git
tags: [git, git-repository-tools, git-subtree, subtree-merge, vendoring, monorepo, submodule-alternative]
level: practitioner
status: docs-checked
description: "Vendor another repository with git subtree (add, pull, split, push) as a submodule alternative, and know when subtree is the wrong tool."
sources:
  - https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging
  - https://github.com/git/git/blob/master/contrib/subtree/git-subtree.adoc
  - https://git-scm.com/docs/merge-strategies
  - https://git-scm.com/docs/git-submodule
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subtree merging

**Goal:** include another project's files directly in your tree (no extra clone step for users) while still being able to pull upstream changes and send changes back.

## 1. Add
```bash
git remote add lib https://github.com/org/lib.git
git subtree add --prefix=vendor/lib lib main --squash
```
`--squash` imports only a single commit from the subproject; without it the subproject's entire history is merged into yours.

## 2. Pull upstream updates
```bash
git subtree pull --prefix=vendor/lib lib main --squash
```
Decide on `--squash` once per prefix and use it for every `add` / `pull` on that prefix (see the git-subtree manual on how a squash merge relates to the previous one).

## 3. Contribute changes back
```bash
git subtree split --prefix=vendor/lib -b lib-export      # history of just that directory
git push lib lib-export:fix-from-app
# or in one go:
git subtree push --prefix=vendor/lib lib fix-from-app
```
Keep commits that touch `vendor/lib` separate from app changes so the split history is clean.

## 4. Extract a directory into its own repo
```bash
git subtree split --prefix=services/billing -b billing-only
git push git@github.com:org/billing.git billing-only:main
```
(`git filter-repo --subdirectory-filter <directory>` is an alternative that rewrites a fresh clone in place.)

## Subtree vs submodule
| | subtree | submodule |
|---|---|---|
| Clone / CI | nothing extra | `--recurse-submodules` |
| Pinning | files copied into your history | gitlink SHA |
| Upstream contribution | split/push, slower on big histories | normal commits in the submodule |
| Repo size | grows with vendored code | small |

Choose subtree when consumers must get everything with a plain clone and upstream changes are infrequent.

## Gotchas
- `git subtree` is shipped in Git's `contrib/` directory, so check that your Git installation includes it.
- `split` synthesises history from the prefix; `--rejoin` merges the synthetic history back so that future splits only search history added since the most recent `--rejoin`. Use the same `--annotate` value on every split or the re-created history may differ.
- The manual "subtree merge strategy" (`git merge -s subtree` / `-Xsubtree=vendor/lib`) is what the command wraps; use it when the prefix detection guesses wrong.
- Never edit vendored files without intending to upstream them; local patches are silently carried and conflict on every pull.

## Verify
- `git log --oneline -- vendor/lib | head` shows the squash commits, and the tree compare `git diff --stat lib/main HEAD:vendor/lib` is empty right after a pull.

## Checked

Checked 2026-10-25 against the git/git tree at master (latest commit 2026-10-22): contrib/subtree/git-subtree.adoc and the merge-strategies manual. Confirmed: `git subtree add|pull|push|split|merge` forms with `-P <prefix>`, `--squash` meaning (single commit), `split -b <branch>`, `--rejoin` semantics, `--annotate` consistency requirement, `git merge -s subtree` and `-Xsubtree[=<path>]`; the tool lives in `contrib/`; `git filter-repo --subdirectory-filter <directory>` exists in the git-filter-repo manual. Removed as unconfirmed: the claim that mixing squashed and unsquashed pulls is the problem and the exact error message for a missing subtree command.

Method: documentation only; no commands were run.
