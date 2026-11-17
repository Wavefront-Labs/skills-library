---
id: computing-software.web-development.hasura.hasura-cli-init-and-config
name: hasura-cli-init-and-config
category: computing-software
field: web-development
product: hasura
tags: [hasura, cli, config-yaml, init, console]
level: intro
status: docs-checked
description: "Initialize a Hasura CLI project with hasura init, edit config.yaml keys, and run the CLI console that records migrations and metadata changes."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/hasura-cli/commands/hasura_init.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/hasura-cli/commands/hasura_console.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/hasura-cli/config-reference.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/hasura-cli/install-hasura-cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set up a project directory for version-controlled Hasura.

Init:

```bash
hasura init my-project --endpoint <HASURA_URL> --admin-secret <ADMIN_SECRET>
```
This creates a project directory with the files and directories needed to configure an instance (`hasura init .` uses the current directory). `--version` sets the config version (default 3); for v3 projects it also creates an AGENTS.md guide, and an existing one is kept.

`config.yaml` keys documented: `version`, `endpoint`, `admin_secret`, `admin_secrets`, `insecure_skip_tls_verify`, `certificate_authority`, `api_paths`, `metadata_directory`, `migrations_directory`, `seeds_directory`, `actions`. Precedence: command flag, then environment variable, then `.env` file, then config file, then default.

Flags shown on `init` and `console`: `--admin-secret`, `--endpoint`, `--envfile` (default `.env`), `--project` (directory where commands run).

Console through the CLI:

```bash
hasura console
```
Defaults: Console on port 9695 (`--console-port`), migrate API on port 9693 (`--api-port`), address `localhost` (`--address`).

Install the CLI first from the install page (curl script, or the `hasura-cli` npm package).

## Checked

2026-11-04. Confirmed against the cited pages: hasura_init, hasura_console, config-reference and install pages: init synopsis and example, --version default 3, config keys and precedence, .env/--envfile, console port defaults, install methods. Removed or corrected: folder list for init, `--database-name`/`--disable-interactive` as global flags (they are documented on migrate/deploy), the CLI-console migration-writing claim and the Verify step.

Method: documentation only; no commands were run.
