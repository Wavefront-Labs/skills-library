---
id: computing-software.web-development.bun.env-files
name: env-files
category: computing-software
field: web-development
product: bun
tags: [dotenv, env-file, import-meta-env, env-expansion]
level: intro
status: docs-checked
description: "Use .env files in Bun: load order per NODE_ENV, --env-file, --no-env-file, variable expansion, quoting, reading variables, and typing Bun.env in TypeScript."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/environment-variables.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Load order (later wins): `.env`; `.env.production` / `.env.development` / `.env.test`; `.env.local` (skipped when `NODE_ENV=test`); `.env.<mode>.local`. Bun reads `.env` natively, so `dotenv` is unnecessary.

```bash
bun --env-file=.env.1 src/index.ts      # repeatable; overrides defaults
bun install --env-file=.env.ci
bun --env-file=<(./fetch-secrets.sh) src/index.ts
bun --no-env-file run dev               # or env = false in bunfig.toml
```

Values: `FOO='x'`, `FOO="x"` and backticks all work. Expansion: `BAR=hello$FOO`; escape as `BAR=hello\$FOO`.

Read via `process.env`, `Bun.env` or `import.meta.env` (aliases). Type a required variable:

```ts
declare module "bun" { interface Env { AWESOME: string } }
```

Gotchas:
- `--no-env-file` does not block explicit `--env-file` paths.
- A pipe can be read only once. `Worker` threads reuse the values, but a `--watch` reload or a `child_process.fork()`/`cluster.fork()` child reads the path again: a pipe is then empty and a FIFO waits for a new writer.
- Node-style invocation (`bun --bun`, `bunx --bun`, a `node` symlink) disables automatic `.env` loading.
- Unescaped `$VAR` in values expands automatically.

## Checked

2026-11-04. Confirmed against bun docs runtime/environment-variables.mdx: file load order and NODE_ENV variants, .env.local test exception, --env-file forms and bun install use, process-substitution pipes, --no-env-file and env = false, explicit --env-file still loading, node-style invocation disabling auto-load, quoting, expansion and escaping, process.env/Bun.env/import.meta.env aliases, Env interface merging. Corrected the pipe gotcha: workers reuse the values; watch reloads and forked children re-read the path.

Method: documentation only; no commands were run.
