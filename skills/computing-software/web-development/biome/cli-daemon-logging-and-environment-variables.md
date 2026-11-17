---
id: computing-software.web-development.biome.cli-daemon-logging-and-environment-variables
name: cli-daemon-logging-and-environment-variables
category: computing-software
field: web-development
product: biome
tags: [biome, environment-variables, biome-log-level, biome-log-path, biome-watcher-kind, biome-binary, biome-config-path, biome-threads, biome-distribution, rust-backtrace]
level: practitioner
status: docs-checked
description: "Biome environment variables for logging, daemon logs, watcher mode, thread count, config path, binary override and upgrade detection."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/environment-variables.md
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The env vars below match CLI flags where noted.

- `BIOME_LOG_LEVEL` (flag `--log-level`): `none` (default), `info`, `warn`, `error`, `debug`, `tracing` (most detailed, span timing). Applies to check, lint, format and ci.
- `BIOME_LOG_KIND` (`--log-kind`): `pretty` (default), `compact`, `json`; needs `BIOME_LOG_LEVEL` to log, e.g. `BIOME_LOG_LEVEL=info BIOME_LOG_KIND=json biome ci .`.
- `BIOME_LOG_FILE` (`--log-file`): write CLI logs to a file: `BIOME_LOG_FILE=biome-debug.log BIOME_LOG_LEVEL=debug biome check .`.
- `BIOME_LOG_PATH` (`--log-path`): directory of daemon logs (default: `biome-logs` in the platform cache directory). `BIOME_LOG_PREFIX_NAME` (`--log-prefix-name`): prefix of daemon log names, default `server.log`.
- `BIOME_CONFIG_PATH`: a configuration file or directory, for shared config outside the current directory.
- `BIOME_THREADS`: worker threads for `biome ci`, default automatic; set it low on constrained runners.
- `BIOME_WATCHER_KIND` (`--watcher-kind`): `recommended` (default, OS watcher), `polling` (slower but better on network or mounted filesystems), `none` (daemon and editors will not detect changes). `BIOME_WATCHER_POLLING_INTERVAL`: milliseconds for the polling watcher, default 2000.
- `BIOME_BINARY`: makes the `@biomejs/biome` npm package run a system or locally built binary: `BIOME_BINARY=/usr/local/bin/biome npx @biomejs/biome check`.
- `BIOME_DISTRIBUTION`: `npm`, `homebrew` or `standalone`, overriding what `biome upgrade` detects (for example Homebrew under a custom prefix).
- `RUST_BACKTRACE=1`: Rust's variable; include the backtrace when reporting a panic.

**Support commands.** `biome rage` prints a troubleshooting report (CLI, platform, environment, configuration, workspace, daemon); `--daemon-logs`, `--formatter` and `--linter` add sections. `biome explain daemon-logs` prints the daemon log directory and `biome clean` removes daemon logs. `biome upgrade` upgrades a standalone binary or runs `brew upgrade biome`; it cannot update npm installs, so update `@biomejs/biome` with the package manager.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
