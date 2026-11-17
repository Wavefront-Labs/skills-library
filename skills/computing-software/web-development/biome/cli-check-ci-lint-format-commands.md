---
id: computing-software.web-development.biome.cli-check-ci-lint-format-commands
name: cli-check-ci-lint-format-commands
category: computing-software
field: web-development
product: biome
tags: [biome, biome-check, biome-ci, biome-lint, biome-format, cli, write-fix, enforce-assist, stdin-file-path, profile-rules]
level: practitioner
status: docs-checked
description: "What biome check, ci, lint and format do, their --write/--unsafe/--formatter-enabled/--enforce-assist flags, stdin mode and rule profiling."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run via package manager (`npx @biomejs/biome check .`, `pnpx`, `yarn exec biome`) or as a standalone binary with no Node.js. `biome --help` and `biome <command> --help` list flags.

**`biome check [PATH...]`** checks formatting, linting and assist actions (current directory if no path).
- `--write`/`--fix`: applies formatting, safe lint fixes and safe assist actions; `--unsafe` also allows unsafe ones.
- `--formatter-enabled`, `--linter-enabled`, `--assist-enabled` (true/false) toggle each tool for the run.
- `--enforce-assist` (default true): fail if required assist actions are not applied.
- `--profile-rules`: reports time per rule, excluding preparation such as building the semantic model.
- `--watch`: reprocess modified files after the initial run.

**`biome ci`** runs the same checks in CI **without modifying files**. It shares `--formatter-enabled`, `--linter-enabled`, `--assist-enabled`, `--enforce-assist`, `--changed`/`--since`, `--only`, `--skip`, and adds `--threads=NUMBER` (also `BIOME_THREADS`) for limited runners.

**`biome lint`**: `--write`, `--unsafe`, `--suppress` (write suppression comments instead of fixes), `--reason=STRING` (needs `--suppress`), `--only`, `--skip`, `--staged`, `--changed`, `--since`, `--profile-rules`, `--watch`, `--stdin-file-path`.

**`biome format`**: `--write`/`--fix`, `--staged`, `--changed`, `--since`, `--watch`, `--stdin-file-path`.

**Stdin.** `--stdin-file-path=PATH` reads code from stdin and writes the processed code to stdout. `PATH` selects settings and input type by extension; virtual paths need not exist and bypass `files.includes` and VCS ignore checks:

```shell
echo 'let a;' | biome check --stdin-file-path=file.js --write
```

**Other commands.** `init [--jsonc]` creates the config; `version`; `stop`/`start` for the daemon; `clean` removes daemon logs; `explain NAME` (a rule name or `daemon-logs`).

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
