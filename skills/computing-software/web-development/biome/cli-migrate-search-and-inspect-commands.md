---
id: computing-software.web-development.biome.cli-migrate-search-and-inspect-commands
name: cli-migrate-search-and-inspect-commands
category: computing-software
field: web-development
product: biome
tags: [biome, biome-migrate, migrate-prettier, migrate-eslint, migrate-stylelint, include-inspired, include-nursery, biome-search, gritql-search, biome-inspect]
level: practitioner
status: docs-checked
description: "Use biome migrate (preview then --write; prettier, eslint, stylelint importers), biome search with GritQL patterns, and biome inspect subcommands."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**`biome migrate`** previews configuration updates required by breaking changes; add `--write`/`--fix` to apply. Subcommands import settings from other tools (also preview-only without `--write`):
- `biome migrate prettier`: imports Prettier configuration and ignore settings.
- `biome migrate eslint`: imports ESLint configuration and ignore settings from the current directory. Extra flags: `--include-inspired` (Biome rules inspired by ESLint rules) and `--include-nursery`.
- `biome migrate stylelint`: same for Stylelint, with the same two flags.

**`biome search PATTERN [PATH...]`** (EXPERIMENTAL) finds code matching a GritQL pattern; read-only, so rewrite queries are not supported. Quote the pattern in single quotes to stop the shell interpreting backticks:

```shell
biome search '`console.log($message)`' ./src
```

`-l/--language=<css|javascript|json>` picks the grammar (default javascript); a search cannot target multiple languages because GritQL patterns are grammar-specific.

**`biome inspect`** has subcommands `plugins`, `config` and `file` (listed in the command index).

**`biome lsp-proxy`** ensures the daemon is running and forwards LSP messages over stdin and stdout. `biome start` and `biome stop` manage the daemon directly.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the CST node names remark for `inspect file` and the 'used by editor extensions' remark and the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
