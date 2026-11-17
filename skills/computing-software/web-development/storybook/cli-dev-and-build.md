---
id: computing-software.web-development.storybook.cli-dev-and-build
name: cli-dev-and-build
category: computing-software
field: web-development
product: storybook
tags: [cli, storybook-dev, storybook-build, port, flags]
level: intro
status: docs-checked
description: "Run and build Storybook from the CLI, with the useful dev and build flags for ports, config dir, output and CI."
sources:
  - https://storybook.js.org/docs/api/cli-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Storybook dev and build CLI

Goal: start the dev server and produce a static build with the right flags.

```shell
storybook dev -p 6006 --ci
storybook build -o storybook-static
```

Common `dev` options:
- `-p, --port [number]` and `--exact-port` (exit instead of picking another port)
- `-h, --host [string]` (default `127.0.0.1`; `0.0.0.0` listens on all interfaces and is insecure)
- `-c, --config-dir [dir-name]` (default `.storybook`)
- `--https` with `--ssl-cert`, `--ssl-key`, optional `--ssl-ca`
- `--ci` skips prompts and does not open the browser; `--open` opens it
- `--smoke-test` exits after a successful start
- `--docs` starts documentation mode; `--initial-path [path]`
- `--preview-only` skips the manager for unsupported browsers
- `--loglevel [level]`: trace, debug, info (default), warn, error, silent
- `--disable-telemetry`, `--no-version-updates`

`build` options: `-o, --output-dir`, `-c`, `--docs`, `--test` (optimise for tests), `--stats-json [dir]`, `--preview-only`, `--quiet`.

With npm scripts, forward options after `--`: `npm run storybook build -- -o ./out --quiet`. The old `-s` static dir flag was removed in Storybook 8; use `staticDirs`.

Verify: `storybook build` writes a `storybook-static` folder with `index.html`.

## Checked
Date: 2026-11-04. Read the CLI options page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: dev and build option tables, defaults, removal of `-s` in Storybook 8, `storybook-static` default output.
Method: documentation only; no commands were run.
