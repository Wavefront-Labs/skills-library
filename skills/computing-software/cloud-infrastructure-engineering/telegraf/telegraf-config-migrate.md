---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-config-migrate
name: telegraf-config-migrate
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [config-migrate, deprecated-plugins, migration, upgrade]
level: advanced
status: docs-checked
description: "Documents telegraf config migrate, which rewrites deprecated plugins and options in config files into .migrated copies. Use when upgrading Telegraf."
sources: ["https://docs.influxdata.com/telegraf/v1/commands/config/migrate/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# telegraf config migrate

`telegraf config migrate` reads the configuration given by `--config` or `--config-directory` and attempts to replace deprecated plugins and options with the recommended ones. With no explicit file it reads the default locations.

## Output

Migrated files are written next to the source files with a `.migrated` suffix. For remote configurations the migrated copy is saved in the current directory, named from the URL plus `.migrated`.

Test migrated files before production use; the docs strongly recommend it.

## Usage

```sh
telegraf --config mysettings.conf config migrate
telegraf --config-directory /etc/telegraf/telegraf.d config migrate
```

`--force` overwrites an existing migration file.

## Finding what is deprecated

`telegraf --deprecation-list` prints all deprecated plugins and plugin options. Telegraf also warns at startup about some settings, for example `skip_processors_after_aggregators` until you set it explicitly.

## Checked

Method: docs-checked 2026-11-09 against the influxdata docs-v2 sources for telegraf config migrate (read in full), the commands reference (flag table) and the agent settings page (skip_processors_after_aggregators section). The `telegraf plugins --deprecated` claim was removed as unconfirmed.
