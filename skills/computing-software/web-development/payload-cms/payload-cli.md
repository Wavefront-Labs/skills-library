---
id: computing-software.web-development.payload-cms.payload-cli
name: payload-cli
category: computing-software
field: web-development
product: payload-cms
tags: [cli, payload-cli, generate-types, importmap, json-output]
level: practitioner
status: docs-checked
description: "Run built-in payload CLI commands such as generate:types, generate:importmap, migrate and jobs:run, and use --json output for scripts."
sources:
  - https://payloadcms.com/docs/configuration/cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Payload CLI

Goal: run project tasks from the terminal.

```sh
pnpm payload --help
pnpm payload generate:types
```

Core commands: `build` (importmap plus types, then the project build), `generate:db-schema` (not every adapter supports it), `generate:importmap`, `generate:types`, `help [command]`, `info` (Node, packages, OS, memory, CPU), `jobs:handle-schedules`, `jobs:run`, `run <script-path> [args...]` (execute a local script in the Payload environment).

Migration commands: `migrate`, `migrate:create [name]`, `migrate:down`, `migrate:fresh`, `migrate:refresh`, `migrate:reset`, `migrate:status`.

JSON mode for scripts and coding agents:

```sh
pnpm payload generate:types --json
export PAYLOAD_CLI_JSON=1   # always JSON
```

The response has `command`, `result` and `success`; failures return `success: false` with an error code and message. In JSON mode stdout holds exactly one JSON response and logs go to stderr, so do not merge streams with `2>&1`.

The CLI loads the config from the current directory; set `PAYLOAD_CONFIG_PATH` if it lives elsewhere. Custom commands can be registered through the `cli` config option.

Verify: `pnpm payload info --json` prints a single JSON object.

## Checked

2026-11-04. Read configuration/cli and configuration/overview. Confirmed: the core and migration command lists with their descriptions, the global --json option, the response shape (command, result, success), failures returning success false with an error code and message, stdout holding one JSON response with logs on stderr and the warning against 2>&1, PAYLOAD_CLI_JSON, loading the config from the project directory, PAYLOAD_CONFIG_PATH, and registering custom commands through the cli config option.
Method: documentation only; no commands were run.
