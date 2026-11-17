---
id: computing-software.devops-ci-cd.semaphore-ui.setup-interactive-config
name: setup-interactive-config
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [setup, config-json, cli, configuration, semaphore-ui]
level: intro
status: docs-checked
description: "Generate config.json with the interactive semaphore setup command, for the server or a runner."
sources:
  - https://semaphoreui.com/docs/admin-guide/configuration/cli
  - https://semaphoreui.com/docs/admin-guide/configuration/config-file
  - https://semaphoreui.com/docs/admin-guide/configuration/env-vars
  - https://semaphoreui.com/docs/admin-guide/runners
  - https://semaphoreui.com/docs/reference/cli/migrations
  - https://semaphoreui.com/docs/introduction/security-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Generate config.json with semaphore setup

Goal: create the configuration file the first time.

Server:

```bash
semaphore setup
```

Runner:

```bash
semaphore runner setup --config /path/to/config.json
```

Both commands generate `config.json` interactively. When `semaphore runner setup` asks whether you have a Runner token, answer No if you will register from the CLI. A web-based configurator for the server and for the runner also exists on the Semaphore website.

Use the file afterwards with:

```bash
semaphore server --config ./config.json
semaphore runner start --config ./config.json
```

Notes:
- Environment variables can override any available configuration option.
- `setup` and every command that touches the database apply pending migrations automatically.

The page's example configuration contains `cookie_hash`, `cookie_encryption` and `access_key_encryption`. Keep backups of the database and of `access_key_encryption`: the security model page says the database is unreadable without it.

## Checked

2026-11-07. Read in full, from markdown sources in the semaphore-docs repository (no snippet files included): admin-guide/configuration/cli.md, config-file.md, env-vars.md, runners.md, reference/cli/migrations.md. For introduction/security-model.md only the grep context around the backup bullet was read, not the whole page. Confirmed: the setup and runner setup commands, the web configurator, the config usage commands, the environment override statement, automatic migrations, and the backup remark. Removed: the claims about which questions setup asks, the --help advice, and the claim that losing access_key_encryption makes stored keys unreadable in those words (replaced by the page's wording).
Method: documentation only; no commands were run.
