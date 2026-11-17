---
id: computing-software.web-development.bun.lockfile-migration
name: lockfile-migration
category: computing-software
field: web-development
product: bun
tags: [bun-lock, migrate-lockfile, bun-lockb, yarn-lockfile]
level: practitioner
status: docs-checked
description: "Work with bun.lock: migrate from npm, yarn, pnpm or bun.lockb, write a Yarn lockfile alongside, use --lockfile-only, and understand migration order and limits."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/lockfile.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun install                  # creates bun.lock; commit it
bun install --lockfile-only  # write lockfile without installing node_modules
bun install --no-save        # no lockfile
bun install --yarn           # also write yarn.lock
bun pm migrate               # migrate without installing
bun install --save-text-lockfile --frozen-lockfile --lockfile-only   # migrate bun.lockb
```

Also in bunfig: `[install.lockfile] print = "yarn"` (only `yarn` supported).

Migration runs when no `bun.lock` exists. Order of the first usable file: `npm-shrinkwrap.json`, `package-lock.json` (lockfileVersion 2, 3, 4), `yarn.lock` (v1 and Berry), `pnpm-lock.yaml`. Bun warns about each file it skips.

Gotchas:
- npm 6 lockfiles (version 1) are not migrated; Bun warns and resolves from `package.json` if nothing else exists.
- After migrating from `bun.lockb`, delete it. Bun keeps the original foreign lockfile; verify the result, then remove it yourself.
- `--frozen-lockfile`, `bun ci`, `--dry-run`, `--no-save` and read-only commands like `bun outdated` migrate in memory only.
- `--lockfile-only` writes the lockfile even when current and still fills the global cache.

## Checked

2026-11-04. Confirmed against bun docs pm/lockfile.mdx and pm/cli/install.mdx: bun.lock creation, --lockfile-only, --no-save, --yarn and [install.lockfile] print, migration order and supported lockfile versions, warnings, original lockfile kept, in-memory migration cases, bun.lockb conversion command, bun pm migrate.

Method: documentation only; no commands were run.
