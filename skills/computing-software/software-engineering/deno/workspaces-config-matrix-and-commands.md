---
id: computing-software.software-engineering.deno.workspaces-config-matrix-and-commands
name: workspaces-config-matrix-and-commands
category: computing-software
field: software-engineering
product: deno
tags: [workspaces, deno-json, compiler-options, tasks, root-only-options, monorepo]
level: advanced
status: docs-checked
description: "Which deno.json options work at workspace root versus member, how settings merge, and running check, test, fmt, lint and tasks across members."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/workspaces.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Root-only options (Deno warns if set in a member): `importMap`, `scopes`, `lint.report`, `minimumDependencyAge`, `nodeModulesDir`, `vendor`, `allowScripts`, `links`, `lock`, `unstable`, `workspace`. Member-only: `name`, `version`, `exports`, and `publish: false` (excludes a member from `deno publish`). Both levels: `compilerOptions`, `imports`, `exclude`, include/exclude of lint, fmt, test, bench and publish, `tasks`.

Merging: `compilerOptions` inherit like TSConfig `extends`. `fmt` options (`useTabs`, `indentWidth`, `singleQuote`, `proseWrap`, `semiColons`): package wins. Lint `rules.tags` append; lint `rules.include/exclude` merge with package priority. Package `tasks` win over workspace tasks, and a task's cwd is its config file's directory.

```json title="deno.json"
{ "workspace": ["./web"], "compilerOptions": { "checkJs": true } }
```
```json title="web/deno.json"
{ "compilerOptions": { "lib": ["esnext", "dom"] } }
```

`web` files get both options. Run from the root:

```sh
deno check        # each member checked separately
deno test         # or: deno test my-directory/
deno fmt
deno lint
deno task --cwd=add build
```

A member's `imports` override the root's only inside that member's folder.

## Checked

2026-11-04: confirmed against the Deno docs Workspaces and monorepos page (options matrix, Running commands across workspaces, managing version conflicts). Fixed the garbled root-only option list: the page lists importMap and scopes as root-only.

Method: documentation only; no commands were run.
