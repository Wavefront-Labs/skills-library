---
id: computing-software.software-engineering.pnpm.git-worktrees-global-store
name: git-worktrees-global-store
category: computing-software
field: software-engineering
product: pnpm
tags: [git-worktree, bare-repository, multi-agent-development, parallel-checkouts, shared-store-trust, worktree-install]
level: practitioner
status: docs-checked
description: "Run several git worktrees of one monorepo, each with its own node_modules, sharing dependencies via pnpm's global virtual store; useful for parallel agents or maintenance."
sources:
  - https://pnpm.io/git-worktrees
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each worktree gets its own checkout and `node_modules`; with the global virtual store those folders hold only symlinks into one shared store, so extra worktrees cost almost no disk and install fast.

```sh
git clone --bare https://github.com/your-org/your-monorepo.git your-monorepo
cd your-monorepo
git worktree add ./main main
git worktree add ./feature-auth feat/auth
```

Enable the global virtual store in `pnpm-workspace.yaml`:

```yaml
packages:
  - 'packages/*'

virtualStoreType: global
```

Then run `pnpm install` inside each worktree. The first one downloads packages; later ones only create symlinks. Each worktree has its own `node_modules` tree, so branches may install different versions without interference. Find the shared store with `pnpm store path`.

Tips:
- Give each AI agent its own dedicated worktree.
- Remove finished ones with `git worktree remove ./feature-auth`.
- Worktrees and agents must share one trust boundary. Do not share one writable pnpm store between mutually untrusted agents or users.

## Checked

2026-11-04. Confirmed against pnpm.io/git-worktrees: bare clone and worktree commands, virtualStoreType: global, symlink-only node_modules, per-worktree trees, pnpm store path, trust-boundary warning, cleanup command. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
