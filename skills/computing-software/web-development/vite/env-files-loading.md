---
id: computing-software.web-development.vite.env-files-loading
name: env-files-loading
category: computing-software
field: web-development
product: vite
tags: [dotenv-files, env-priority, dotenv-expand, local-env-gitignore]
level: practitioner
status: docs-checked
description: "Vite .env file loading: the four file names, priority rules, existing process env wins, dotenv-expand escaping, restart needs, and Bun interference."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/env-and-mode.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Loaded from the env directory (`envDir`):

```
.env                # loaded in all cases
.env.local          # loaded in all cases, ignored by git
.env.[mode]         # only loaded in specified mode
.env.[mode].local   # only loaded in specified mode, ignored by git
```

Priority: mode-specific files beat generic ones, but variables only in `.env` or `.env.local` stay available. Variables already in the environment when Vite starts win and are never overwritten (`VITE_SOME_KEY=123 vite build`).

Files load at Vite start; restart the server after changes.

Expansion uses dotenv-expand; escape a literal `$` with a backslash:

```
KEY=123
NEW_KEY1=test$foo   # test
NEW_KEY2=test\$foo  # test$foo
NEW_KEY3=test$KEY   # test123
```

Reverse-order expansion (`VITE_FOO=foo${VITE_BAR}` before `VITE_BAR=bar`) works but is best avoided; docker compose and shells do not support it.

Add `*.local` to `.gitignore`. Under Bun, its automatic `.env` loading fills `process.env` first and can interfere.

## Checked

2026-11-04. Confirmed against the Vite Env Variables and Modes guide (docs/guide/env-and-mode.md): the four file names, priority rules, existing environment wins, restart note, dotenv-expand escaping, reverse-order note, *.local gitignore advice, Bun warning. Nothing removed.

Method: documentation only; no commands were run.
