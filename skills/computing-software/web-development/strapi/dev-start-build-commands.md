---
id: computing-software.web-development.strapi.dev-start-build-commands
name: dev-start-build-commands
category: computing-software
field: web-development
product: strapi
tags: [strapi, develop, start, build, cli, hmr, bundler, vite]
level: intro
status: docs-checked
description: "strapi develop vs start vs build: when to use each, key options, and why Content-type Builder is off under start."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# develop, start, build

Use `yarn strapi <cmd> --<option>` or `npm run strapi <cmd> -- --<option>`.

## strapi develop (alias `dev`)
Auto-reloading with a file watcher and HMR for the admin panel. Never use it in production.

```shell
strapi develop
options: [--bundler | --open | --no-watch-admin | --no-build-admin | --polling | --debug | --silent]
```

- `--bundler [bundler]`: `vite` or `webpack`.
- `--no-watch-admin`: no auto-reload on admin code changes (in Strapi 5, `develop` always runs in watch-admin mode otherwise).
- `--polling`: watch network directories.
- `--no-install-deps`: skip auto-install of missing admin peer dependencies and fail if any are missing.

## strapi start
Auto-reloading disabled; for production. Features needing restarts, such as the Content-type Builder, are disabled.

## strapi build
Builds the admin panel.

```bash
strapi build
```

Options: `--bundler` (`vite` default; `webpack` deprecated), `-d/--debug`, `--minify` (default true), `--silent`, `--sourcemap`, `--stats`, `--install-deps`.

## Checked

Checked 2026-11-04 against the Strapi CLI page (general considerations for npm and yarn option syntax, develop, start, build). Nothing removed.

Method: documentation only; no commands were run.
