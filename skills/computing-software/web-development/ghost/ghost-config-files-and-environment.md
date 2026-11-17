---
id: computing-software.web-development.ghost.ghost-config-files-and-environment
name: ghost-config-files-and-environment
category: computing-software
field: web-development
product: ghost
tags: [ghost, configuration, config-production-json, environment-variables, nconf, debug]
level: advanced
status: docs-checked
description: "Configure Ghost with config.production.json, config.development.json and local overrides, env variables, and debug output."
sources:
  - https://github.com/TryGhost/docs/blob/main/config.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change Ghost settings safely.

Ghost reads JSON config via nconf from the install root. Two environments: development (default) and production. Files: `config.development.json`, `config.production.json`, plus `config.local.json` for local development tweaks that git ignores and that merges on top of the development file. Apply changes with `ghost restart`.

Three required options: `url`, `database` (set at install) and `mail` (configure after install).

Run production mode manually with `NODE_ENV=production node index.js`. To debug configuration output start Ghost with `DEBUG=ghost:*,ghost-config node index.js`.

Environment variables: all options can be overridden, and env values take priority over config files. Match the option name and case, for example `url=http://ghost.local:2368 node index.js`. Nested options use two underscores (`database__connection__host=mysql node index.js`), and list values are passed as JSON (`logging__transports='["stdout","file"]'`).

Other sections the page covers: URL and SSL, database and connections, mail, admin URL, server, privacy, security, paths, referrer policy, adapters, logging, spam, caching, compress and image optimization.

Verify: `ghost config url` returns the expected value after restart.

## Checked

2026-11-04. Confirmed: file names, nconf, environments, config.local.json merge, required options, NODE_ENV and DEBUG commands, env-variable overrides, double underscore nesting, JSON list values, ghost restart and ghost config (configuration and Ghost CLI pages). Removed: the secrets and containers practice line.

Method: documentation only; no commands were run.
