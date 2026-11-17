---
id: computing-software.web-development.bun.update-dependencies
name: update-dependencies
category: computing-software
field: web-development
product: bun
tags: [bun-update, interactive-update, update-latest, depth-zero]
level: practitioner
status: docs-checked
description: "Update dependencies with bun update: within range, --latest, interactive selection, workspaces, globs and depth 0, plus what never gets rewritten."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/update.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun update                    # within declared ranges (alias: bun up)
bun update zod
bun update '@babel/*' '!@babel/core'
bun update --latest           # -L: ignore declared ranges
bun update -i -r              # interactive across all workspaces
bun update --filter './packages/*'
bun update --depth 0 --latest # direct deps only
bun update -g typescript
bun update --dry-run
```

Interactive keys: Space toggles, Enter confirms, `a`/`n`/`i` select all/none/invert, `l` toggles target vs latest.

Gotchas:
- Ranges are never widened: `^1.0.0` never goes to 2.x without `--latest`.
- Pins, dist-tags, `*`, `1.x` stay as written unless `--latest`.
- `catalog:` references are not rewritten; the root catalog entry is updated.
- `overrides` pin versions even with `--latest`. Patched versions stay put until `--latest` or `bun audit fix`; redo `bun patch` after.
- Naming a package absent from `bun.lock` is an error.
- Without `-r`, only the current workspace's `package.json` changes.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/update.mdx: bun up alias, name globs and exclusions, --latest, interactive keys, -r and --filter, --depth 0, -g, --dry-run, range-preservation and rewrite rules, catalog handling, overrides and patched-dependency hold-back, absent-package error.

Method: documentation only; no commands were run.
