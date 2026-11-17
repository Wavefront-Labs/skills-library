---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-secrets-command
name: telegraf-secrets-command
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [secrets-command, secret-set, secret-list, secret-get, secret-remove]
level: practitioner
status: docs-checked
description: "Documents the telegraf secrets subcommands list, get, set and remove and how they find the secret store definitions. Use to manage stored credentials from the shell."
sources: ["https://docs.influxdata.com/telegraf/v1/commands/secrets/", "https://docs.influxdata.com/telegraf/v1/commands/secrets/set/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The telegraf secrets command

`telegraf secrets` manages secrets in the secret stores defined in your configuration.

## Subcommands

- `list`: list known secrets and secret stores.
- `get`: retrieve a secret's value.
- `set`: create or modify a secret.
- `remove`: remove a secret.

## Finding the configuration

The command needs the configuration that holds the secret store definitions. Without `--config` or `--config-directory`, Telegraf checks the default configuration location. Run `telegraf secrets list` to see store IDs and secret keys. If none is configured, `telegraf plugins secretstores` lists the available store plugins.

## set

```sh
telegraf secrets set SECRET_STORE_ID SECRET_KEY SECRET_VALUE
```

With a non-default configuration, put the global flag before the command:

```sh
telegraf --config CUSTOM_CONFIG_PATH secrets set SECRET_STORE_ID SECRET_KEY SECRET_VALUE
```

Not every store can be modified. Stores backed by a read-only source reject `set` and `remove`.

Global flags `--password` (unlock secret stores) and `--unprotected` (do not protect secrets in memory) also apply.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): secrets command pages (set, get, list), default configuration location, read-only stores. Removed: the sentence about passwords being visible in process listings and shell history, which the pages do not state.

Method: documentation only; no commands were run.
