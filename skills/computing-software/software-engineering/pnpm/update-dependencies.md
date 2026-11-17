---
id: computing-software.software-engineering.pnpm.update-dependencies
name: update-dependencies
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-update, update-latest, interactive-update, update-patterns, update-depth, no-save, update-recursive]
level: practitioner
status: docs-checked
description: "Update dependencies with pnpm update: ranges versus --latest, patterns and negation, --depth, --interactive, --recursive, --no-save, and what gets rewritten (catalogs, tags)."
sources:
  - https://pnpm.io/cli/update
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Aliases: `up`, `upgrade`.

| Command | Meaning |
|---|---|
| `pnpm up` | update all within `package.json` ranges |
| `pnpm up --latest` | latest versions, possibly across majors |
| `pnpm up foo@2` | latest on v2 |
| `pnpm up "@babel/*"` | all in a scope |

Patterns combine, and `!` negates (the docs escape it as `\!`): `pnpm update "@babel/*" "\!@babel/core"`.

Options: `--depth 0` direct deps only (default Infinity); `-i` pick interactively; `-r` every subdirectory with a `package.json` (`pnpm --recursive update typescript@latest`); `--prod`, `--dev`, `--optional`, `--peer` select fields; `-E` with `--latest` writes no operator; `--lockfile-only`; `--no-save` moves the lockfile and leaves ranges alone.

What it writes:
- The existing operator is kept (`^1.1.0` stays caret).
- `catalog:` deps update the entry in `pnpm-workspace.yaml`, not `package.json`.
- A dist-tag dep (`"foo": "latest"`) keeps tracking the tag; only the lockfile moves.
- `jsr:` prefixes are kept.

`pnpm update foo@1.2.3` on a transitive dependency fails with `ERR_PNPM_UPDATE_VERSION_ON_INDIRECT_DEP`; use `overrides`.

## Checked

2026-11-04. Confirmed the TL;DR table, what an update writes, pattern syntax, --depth, --latest, -r, --prod, --dev, --optional, --peer, -E, --lockfile-only, --no-save and ERR_PNPM_UPDATE_VERSION_ON_INDIRECT_DEP against pnpm.io/cli/update. Aligned the -r wording with the page. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
