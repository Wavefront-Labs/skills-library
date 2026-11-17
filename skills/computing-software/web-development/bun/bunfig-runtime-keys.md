---
id: computing-software.web-development.bun.bunfig-runtime-keys
name: bunfig-runtime-keys
category: computing-software
field: web-development
product: bun
tags: [bunfig-toml, preload, define-loader, run-config]
level: practitioner
status: docs-checked
description: "Configure the Bun runtime in bunfig.toml: preload, jsx, define, loader, serve port, run options, console depth, telemetry, and which file wins."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/bunfig.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```toml
preload = ["./preload.ts"]     # runs before the entry file; register plugins here
smol = true                    # lower memory, slower
jsx = "react"                  # also jsxFactory, jsxFragment, jsxImportSource
logLevel = "warn"              # debug | warn | error
telemetry = false              # like DO_NOT_TRACK
env = false                    # disable automatic .env loading

[define]
"process.env.bagel" = "'lox'"  # values parsed as JSON; single-quoted strings accepted

[loader]
".bagel" = "tsx"

[console]
depth = 2

[serve]
port = 3000                    # BUN_PORT, PORT or --port override

[run]
shell = "bun"                  # "system" default outside Windows
bun = true                     # node alias to Bun for scripts, like --bun
silent = true
noOrphans = true
```

Precedence and gotchas:
- Project root `bunfig.toml` is optional. A global `$HOME/.bunfig.toml` (or `$XDG_CONFIG_HOME/.bunfig.toml`) is read only by package manager commands; `bun run` loads only the project file.
- Local keys override global; CLI flags override both. Files Bun cannot read are skipped.
- Disabling `.env` loading still loads files passed with `--env-file`.

## Checked

2026-11-04. Confirmed against bun docs runtime/bunfig.mdx: global versus local files and XDG_CONFIG_HOME, package-manager-only global file, local override and CLI flag precedence, unreadable files skipped, preload, jsx keys, smol, logLevel, define value parsing, loader, telemetry, env = false and --env-file exception, console.depth default 2, serve.port default 3000 with BUN_PORT/PORT/--port, run.shell default, run.bun, run.silent, run.noOrphans. Removed the word silently (page only says skipped) and added the jsx keys named in the description.

Method: documentation only; no commands were run.
