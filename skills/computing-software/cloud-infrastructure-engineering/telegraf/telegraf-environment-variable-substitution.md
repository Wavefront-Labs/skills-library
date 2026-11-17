---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-environment-variable-substitution
name: telegraf-environment-variable-substitution
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [environment-variables, substitution, etc-default-telegraf, strict-env-handling, quoting]
level: practitioner
status: docs-checked
description: "Documents ${VAR} substitution in Telegraf configs, the default and error expansion forms, quoting by TOML type, and where to set variables for packages."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/environment-variables/", "https://docs.influxdata.com/telegraf/v1/commands/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Environment variable substitution

Use `${VAR}` anywhere in the configuration file. Telegraf replaces variables before parsing, so a variable can supply any part of the file.

## Quoting follows the TOML type

- Strings: quote it, `"${STR_VAR}"`.
- Numbers and booleans: leave unquoted, `${INT_VAR}`.
- In double-quoted strings escape backslashes; for a single backslash use a single-quoted literal string.

## Expansion forms

- `${VAR}`: the value.
- `${VAR:-default}`: default if unset or empty.
- `${VAR-default}`: default only if unset.
- `${VAR:?err}`: exit with `err` if unset or empty.
- `${VAR?err}`: exit with `err` if unset.

## Where to define

Set variables in the environment that starts Telegraf: a shell, systemd unit or container. With the `.deb` or `.rpm` packages use `/etc/default/telegraf`, read at service start.

```sh
# /etc/default/telegraf
INFLUX_HOST="http://localhost:8181"
INFLUX_TOKEN="replace_with_your_token"
```

```toml
[[outputs.influxdb_v3]]
  urls = ["${INFLUX_HOST}"]
  token = "${INFLUX_TOKEN}"
```

For credentials, prefer secret stores. Related global flags: `--strict-env-handling`, `--non-strict-env-handling` and `--old-env-behavior` (pre-v1.27 behaviour).

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Environment variables page: expansion forms, quoting, /etc/default/telegraf; commands page for the env flags. Removed: nothing.

Method: documentation only; no commands were run.
