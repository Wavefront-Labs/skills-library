---
id: computing-software.devops-ci-cd.turborepo.caching-git-worktree-cache-sharing
name: caching-git-worktree-cache-sharing
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, git-worktree, cache-sharing, cachedir, absolute-paths, local-cache, feature-branches]
level: advanced
status: docs-checked
description: "Turborepo shares the local cache between a main git worktree and linked worktrees automatically; an explicit cacheDir disables that, and absolute paths in outputs are a trap."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/caching.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When using Git worktrees, Turborepo automatically shares the local filesystem cache between the main worktree and linked worktrees. Benefits listed: cache hits across branches, reduced disk usage by avoiding duplicate entries, and faster iteration when switching between feature branches.

**How it works.** When you create a linked worktree with `git worktree add`, Turborepo detects it and redirects the cache to the main worktree's `.turbo/cache` directory:

```bash
git worktree add ../my-feature feature-branch
cd ../my-feature
turbo build   # cache shared with main worktree
```

When sharing is active the output includes the line `Remote caching enabled, using shared worktree cache`.

**Explicit `cacheDir` disables sharing.** If you set `cacheDir` in `turbo.json`, worktree cache sharing is disabled and each worktree uses its own directory.

**Warning: outputs containing absolute paths.** Cache artifacts are restored without rewriting their contents. If a task output contains the absolute path of its worktree, sharing can restore an output that points to another checkout. Set an explicit `cacheDir`, such as `.turbo/cache`, to keep the local cache isolated per worktree.

**With Remote Caching.** The local cache is shared between worktrees on the same machine and the remote cache across machines and CI. A task built in one worktree restores from the shared local cache in another without a network request; if the artifact is missing locally, Turborepo falls back to the Remote Cache.

Verify: build in the main worktree, then in a linked one; expect the shared-cache message and a hit.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/caching); commands, flags, key names, defaults and example values were matched against it. Removed: nothing; every claim matched.

Method: documentation only; no commands were run.
