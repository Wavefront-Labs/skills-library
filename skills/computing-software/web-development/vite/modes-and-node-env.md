---
id: computing-software.web-development.vite.modes-and-node-env
name: modes-and-node-env
category: computing-software
field: web-development
product: vite
tags: [vite-modes, node-env, staging-mode, mode-flag]
level: practitioner
status: docs-checked
description: "Vite modes versus NODE_ENV: dev runs development, build runs production, --mode staging loads .env.staging, and how PROD, DEV and MODE derive."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/env-and-mode.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The dev command runs in `development` mode and `vite build` in `production`. Override with `--mode`:

```bash
vite build --mode staging   # loads .env.staging
```

`NODE_ENV` and mode are different concepts:

| Command | NODE_ENV | Mode |
| --- | --- | --- |
| `vite build` | production | production |
| `vite build --mode development` | production | development |
| `NODE_ENV=development vite build` | development | production |
| `NODE_ENV=development vite build --mode development` | development | development |

`PROD` and `DEV` follow `NODE_ENV`: `production` gives PROD true; `development` or any other value gives DEV true. `MODE` follows `--mode`.

Run a development build by setting it in an env file:

```
# .env.testing
NODE_ENV=development
```

Setting `NODE_ENV` in the command lets Vite see it early and lets your config read `process.env.NODE_ENV`; env files load only after the config is evaluated.

## Checked

2026-11-04. Confirmed against the Vite Env Variables and Modes guide (docs/guide/env-and-mode.md): default modes, --mode, the NODE_ENV and mode table, PROD and DEV derivation, .env.testing example, early NODE_ENV detection. Nothing removed.

Method: documentation only; no commands were run.
