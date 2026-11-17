---
id: computing-software.devops-ci-cd.turborepo.caching-first-hit-and-fingerprint
name: caching-first-hit-and-fingerprint
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, caching, cache-hit, full-turbo, fingerprint, deterministic-tasks, cache-miss, local-cache]
level: intro
status: docs-checked
description: "How Turborepo caching works: a fingerprint hash of inputs, a first-run miss, a second-run FULL TURBO hit, and the determinism assumption."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/caching.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Turborepo caching ensures you **never do the same work twice**. When a task is cacheable, Turborepo restores the results from a fingerprint taken the first time the task ran. The docs' example restores 12 tasks across 3 packages in 80 milliseconds with a `>>> FULL TURBO` message.

**Assumption:** Turborepo assumes tasks are **deterministic**. If a task can produce different outputs for the same inputs Turborepo knows about, caching may not work as expected.

Try it in three steps:
1. `npx create-turbo@latest`.
2. Run a build (`turbo build` if installed globally, or the package manager's `run build` script). This is a cache miss: this set of inputs has never run in this repository. The inputs become a hash, looked up in the local filesystem cache or the Remote Cache.
3. Run `turbo build` again. The fingerprint is in the cache so tasks are restored (the docs' screenshot shows two tasks completing in 116 ms).

Turborepo stores task results in `.turbo/cache` on your machine by default. Sharing that cache with teammates and CI makes the whole organisation faster (see the remote caching skills).

Verify: the second run restores the results from cache instead of rebuilding.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/caching); commands, flags, key names, defaults and example values were matched against it. Removed: the timing claim in the Verify step.

Method: documentation only; no commands were run.
