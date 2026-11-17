---
id: computing-software.devops-ci-cd.nx.nx-env-vars-common
name: nx-env-vars-common
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, environment-variables, nx-cache-directory, nx-daemon, nx-verbose-logging, ci]
level: practitioner
status: docs-checked
description: "Everyday Nx environment variables: NX_BAIL, NX_BASE/HEAD, cache and graph directories, NX_PARALLEL, NX_TUI, NX_VERBOSE_LOGGING, NX_PROFILE, and variables Nx sets for tasks."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/environment-variables.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find the right `NX_*` switch without guessing. Where a flag is named below, the page says the flag overrides the variable.

Execution:
- `NX_BAIL=true`: stop after the first failed task (flag `--nxBail`).
- `NX_PARALLEL=<n>`: tasks in parallel; overrides nx.json.
- `NX_BATCH_MODE=true`: batch tasks for executors that support it.
- `NX_IGNORE_CYCLES=true`: ignore task-graph cycle errors (`--nxIgnoreCycles`).
- `NX_DEFAULT_OUTPUT_STYLE`: default output style (`--outputStyle`).
- `NX_TUI=true|false`; `NX_TUI_AUTO_EXIT=true|false|<seconds>`.
- `NX_PROCESS_KILL_GRACE_PERIOD`: ms before force-killing children, default 5000.

Affected: `NX_BASE`, `NX_HEAD` (flags `--base`, `--head`); `NX_LEGACY_AFFECTED` overrides `affected.legacy` for one run.

Cache: `NX_CACHE_DIRECTORY` (default shared `~/.nx/<id>/cache`), `NX_CACHE_FAILURES=true` caches failing tasks, `NX_SKIP_NX_CACHE` / `NX_DISABLE_NX_CACHE` rerun regardless of cache, `NX_SKIP_REMOTE_CACHE` / `NX_DISABLE_REMOTE_CACHE` disable all remote caches (Nx Cloud and self-hosted), `NX_MAX_CACHE_SIZE` alternative to `maxCacheSize`. Self-hosted: `NX_SELF_HOSTED_REMOTE_CACHE_SERVER` (URL) and `NX_SELF_HOSTED_REMOTE_CACHE_ACCESS_TOKEN` (bearer token).

State: `NX_WORKSPACE_DATA_DIRECTORY` moves graph database, daemon logs etc. (and opts the cache out of its shared location); `NX_PROJECT_GRAPH_CACHE_DIRECTORY` is its alias. `NX_CACHE_PROJECT_GRAPH=false` disables graph cache (plugin development). `NX_DAEMON=false` disables the daemon. `NX_SOCKET_DIR` relocates sockets.

Debug: `NX_VERBOSE_LOGGING=true`, `NX_PERF_LOGGING=true`, `NX_PROFILE=profile.json` (load in Chrome dev tools), `NX_NATIVE_LOGGING` / `NX_NATIVE_FILE_LOGGING` (Rust logs to `.nx/workspace-data/nx.log`).

Migrate: `NX_MIGRATE_CLI_VERSION`, `NX_MIGRATE_SKIP_INSTALL`, `NX_MIGRATE_USE_LOCAL`, `NX_MULTI_MAJOR_MODE` (`direct` or `gradual`).

Set by Nx for processes: `NX_TASK_TARGET_PROJECT`, `NX_TASK_TARGET_TARGET`, `NX_TASK_TARGET_CONFIGURATION`, `NX_GRAPH_CREATION` (true during graph creation), `NX_DRY_RUN`, `NX_INTERACTIVE`.

Others: `NX_SKIP_FORMAT=true` skips generator formatting (Biome/dprint repos); `NX_MAX_MESSAGE_SIZE` default 2 GiB, `0` unlimited (run `nx reset` after changing).

## Checked

2026-11-07. Confirmed: every NX_* variable, default and flag pairing listed against the Environment variables page. Removed: an invented Verify step and the blanket claim that flags override variables (now limited to flags the page names).

Method: documentation only; no commands were run.
