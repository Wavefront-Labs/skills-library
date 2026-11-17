---
id: computing-software.web-development.biome.cli-global-flags-diagnostics-and-exit-behaviour
name: cli-global-flags-diagnostics-and-exit-behaviour
category: computing-software
field: web-development
product: biome
tags: [biome, global-flags, max-diagnostics, diagnostic-level, error-on-warnings, no-errors-on-unmatched, skip-parse-errors, config-path, use-server, colors]
level: practitioner
status: docs-checked
description: "Global CLI flags controlling diagnostics volume and level, exit codes, parse errors, unmatched paths, config path, colours and verbosity."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Global flags available to many commands:
- `-h/--help`, `-V/--version`.
- `--colors=<off|force>`: `off` disables ANSI styling; `force` enables it even when output does not appear to support it.
- `--use-server`: connect to a running daemon.
- `--verbose`: show extra diagnostic details and list processed or modified files.
- `--config-path=PATH` (env `BIOME_CONFIG_PATH`): a configuration file, or a directory in which to look for `biome.json`/`biome.jsonc`. It **disables default configuration resolution**.
- `--max-diagnostics=<none|NUMBER>`: default 20; `none` removes the limit.
- `--skip-parse-errors`: skip files with syntax errors instead of an error diagnostic.
- `--no-errors-on-unmatched`: do not fail when no files were processed.
- `--error-on-warnings`: exit with an error if any warning diagnostic is emitted.
- `--diagnostic-level=<info|warn|error>`: minimum severity displayed; default `info`. `--diagnostic-level=error` shows only errors.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the diagnostics severities and tags paragraph and the combined CI recipe line and the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
