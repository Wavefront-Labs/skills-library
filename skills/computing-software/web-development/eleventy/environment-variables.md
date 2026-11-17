---
id: computing-software.web-development.eleventy.environment-variables
name: environment-variables
category: computing-software
field: web-development
product: eleventy
tags: [environment-variables, process-env, dotenv, eleventy-run-mode, cross-env]
level: intro
status: docs-checked
description: "Set your own environment variables for an Eleventy build on each OS, use .env safely, and read Eleventy's own ELEVENTY_* variables."
sources:
  - https://www.11ty.dev/docs/environment-vars/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Variables are read through Node's `process.env`, only in JavaScript evaluated at build time (config, JS data files, JS templates). To use one in other template languages, export it from a JS data file.

**Set your own**

- `.env` file with the `dotenv` package for private keys. Add `.env` to `.gitignore`; never commit it.
- macOS/Linux: `MY_ENVIRONMENT=production npx @11ty/eleventy`
- Windows cmd.exe: `set MY_ENVIRONMENT=production & npx @11ty/eleventy`
- PowerShell: `$env:MY_ENVIRONMENT="production"; npx @11ty/eleventy`
- Cross platform: `npm install cross-env`, then in `package.json`:

```json
{ "scripts": { "build:prod": "cross-env MY_ENVIRONMENT=production npx @11ty/eleventy" } }
```

**Eleventy supplied**

- `ELEVENTY_ROOT` (1.0.0+): absolute path of the directory where the command ran.
- `ELEVENTY_SOURCE` (1.0.0+): `cli` or `script` (programmatic API).
- `ELEVENTY_RUN_MODE` (2.0.0+): `build`, `serve` or `watch`.
- `ELEVENTY_VERSION` (3.0.0+): the current Eleventy version.

Use cases: expose to templates via a JS data file, enable `git Last Modified` dates only in production, use fewer image formats locally. `DEBUG` mode is also enabled this way.

Disable colored terminal output with Node's `NODE_DISABLE_COLORS=1`.

## Checked

2026-11-04. Confirmed against the Eleventy Environment Variables page: process.env access in build-time JavaScript only, the .env and dotenv guidance with the .gitignore warning, the macOS/Linux, cmd.exe, PowerShell and cross-env commands, the use case ideas, ELEVENTY_ROOT and ELEVENTY_SOURCE (v1.0.0), ELEVENTY_RUN_MODE (v2.0.0), ELEVENTY_VERSION (v3.0.0) and NODE_DISABLE_COLORS. Corrected the run-mode and version gates from pre-release tags.

Method: documentation only; no commands were run.
