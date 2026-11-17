---
id: computing-software.devops-ci-cd.turborepo.caching-troubleshooting-dry-summarize-force
name: caching-troubleshooting-dry-summarize-force
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, cache-troubleshooting, dry-run, run-summary, summarize, force-flag, cache-false, no-cache, slow-caching]
level: practitioner
status: docs-checked
description: "Debug cache misses with --dry and --summarize, bypass with --force or cache false, and know when caching a task is slower than running it."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/caching.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Dry runs.** `turbo run <task> --dry` shows what would happen without running anything; useful when unsure which tasks you are running.

**Run Summaries.** `--summarize` produces an overview of a task's inputs, outputs and more. Comparing two summaries shows why two hashes differ. Use it to debug inputs (a task misses when you expect a hit) and outputs (cache hits do not restore expected files). There is no native summaries UI viewer; community tools listed: turbo.nullvoxpopuli.com, `turborepo-summary` and `turborepo-summary-action`.

**Turning caching off.** Per task with `"cache": false`, or for a whole run with the `--cache <options>` flag.

**Overwriting a cache.** `--force` makes `turbo` re-execute a cached task. It disables **reading** the cache, **not writing**.

**When caching is slower than executing.** Rare, but:
- Tasks that run faster than a network round-trip to the Remote Cache.
- Tasks with enormous outputs, such as a complete Docker container, where upload or download exceeds regeneration.
- Scripts with their own internal caching, which complicates combining caches.

Test your projects to see whether disabling caching in specific places helps.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/caching); commands, flags, key names, defaults and example values were matched against it. Removed: the invented diff-the-summaries Verify step.

Method: documentation only; no commands were run.
