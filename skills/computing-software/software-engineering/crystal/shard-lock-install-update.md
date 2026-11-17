---
id: computing-software.software-engineering.crystal.shard-lock-install-update
name: shard-lock-install-update
category: computing-software
field: software-engineering
product: crystal
tags: [shard-lock-install-update, shards, shards-install, shards-update, shard-lock, shards-check, shards-list, shards-outdated, lock-file, lib-folder, crystal]
level: practitioner
status: docs-checked
description: "Use shards install, update, lock, check, list, outdated and prune with shard.lock, and the --frozen and --production flags for reproducible CI installs."
sources:
  - https://github.com/crystal-lang/shards/blob/master/docs/shards.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# shards install, update, check and shard.lock

Goal: reproducible dependencies.

- `shards install` resolves and installs dependencies into `lib`. If there is no `shard.lock` it writes one; if one exists it reads and enforces the locked versions and commits. It may fail if a locked version no longer matches a requirement, but succeeds if a new dependency was added without conflict (generating a new lock).
- `shards update [shards...]` resolves and updates dependencies whatever the locked versions; naming shards updates only those, as conservatively as possible for the others.
- `shards check` verifies that dependencies are installed and requirements are satisfied; exit status 0 means satisfied, 1 not.
- `shards list [--tree]` lists installed dependencies; `shards outdated [--pre]` lists outdated ones; `shards prune` removes unused dependencies from `lib`; `shards lock [--print] [--update [shards...]]` writes the lock without installing; `shards version [path]` prints the shard's version.
- `install` options: `--frozen` (strictly installs locked versions, fails if `shard.lock` is missing), `--without-development`, `--production` (same as `--frozen` and `--without-development`), `--skip-postinstall`, `--skip-executables`, `--jobs=N` (default 8, git only).
- General option `--local` uses the local cache copies instead of updating remote repositories.
- Applications commit `shard.lock`; libraries should not (add it to `.gitignore`).
- With no command, `shards` runs `install`.

Gotchas:
- CI should run `shards install --production` for a locked, no-development install.
- Dependencies install to `lib` by default (`SHARDS_INSTALL_PATH` changes it); the cache location is `SHARDS_CACHE_PATH`.

Verify: `shards check` exits 0 after install.

## Checked

2026-11-03. Confirmed against the shards(1) man page source: commands and options above, exit statuses, lock-file rules, environment variables.
Removed: "lib/ is git-ignored" (not stated), the dependency-conflict output claim, and the wrong claim that `--production` fails "if the lock is out of date" (the doc says it equals `--frozen` plus `--without-development`).
Method: documentation only; no commands were run.
