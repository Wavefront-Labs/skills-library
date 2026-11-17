---
id: computing-software.software-engineering.pnpm.git-branch-lockfiles
name: git-branch-lockfiles
category: computing-software
field: software-engineering
product: pnpm
tags: [git-branch-lockfile, merge-git-branch-lockfiles, lockfile-merge-conflicts, branch-lockfile-pattern, branch-lockfile-name]
level: practitioner
status: docs-checked
description: "Avoid lockfile merge conflicts with gitBranchLockfile: per-branch pnpm-lock.<branch>.yaml names, character escaping, --merge-git-branch-lockfiles and branch-pattern auto merge."
sources:
  - https://pnpm.io/git_branch_lockfiles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable in `pnpm-workspace.yaml`:

```yaml
gitBranchLockfile: true
```

The lockfile is then named after the branch: branch `feature-1` writes `pnpm-lock.feature-1.yaml` next to `pnpm-lock.yaml`. Commit it and merge later.

Name rules: every character other than ASCII letters, digits, `_`, `.`, `-` becomes `!`, and the name is lowercased, so `Feature/1` gives `pnpm-lock.feature!1.yaml`. A character outside the Basic Multilingual Plane, such as an emoji, becomes `!!`.

Merge all branch lockfiles into `pnpm-lock.yaml` (the branch files are deleted):

```sh
pnpm install --merge-git-branch-lockfiles
```

Merge automatically on matching branches:

```yaml
mergeGitBranchLockfilesBranchPattern:
  - main
  - release*
```

`pnpm install` then merges when run on `main` or any branch starting with `release`. The CLI form is `--merge-git-branch-lockfiles-branch-pattern <glob>` (repeatable).

## Checked

2026-11-04. Confirmed against pnpm.io/git_branch_lockfiles and pnpm.io/cli/install: gitBranchLockfile, lockfile naming and character rules, --merge-git-branch-lockfiles deleting branch files, mergeGitBranchLockfilesBranchPattern, repeatable --merge-git-branch-lockfiles-branch-pattern. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
