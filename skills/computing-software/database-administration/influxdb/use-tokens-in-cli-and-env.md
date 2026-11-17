---
id: computing-software.database-administration.influxdb.use-tokens-in-cli-and-env
name: use-tokens-in-cli-and-env
category: computing-software
field: database-administration
product: influxdb
tags: [tokens, influx-config, influx-token, environment-variable, cli-auth]
level: intro
status: docs-checked
description: "Authenticate influx CLI calls with -t, the INFLUX_TOKEN variable or an influx config profile, including username and password profiles on CLI 2.4+."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/tokens/use-tokens/
  - https://docs.influxdata.com/influxdb/v2/tools/influx-cli/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Three ways to give the `influx` CLI a token:

```sh
influx write -t <token> -b BUCKET -o org-name "measurement field=1"

export INFLUX_TOKEN=my-token
influx write -t $INFLUX_TOKEN -b my-bucket -o my-org "measurement field=1"
```

Or store a connection profile with `influx config create` (see `influx config`), which holds host, org and token so you can omit them per command.

From influx CLI 2.4.0 against InfluxDB OSS 2.4+, a profile can authenticate with the UI username and password:

```sh
influx config create -n CONFIG_NAME -u http://localhost:8086 -p USERNAME:PASSWORD -o ORG
```

The CLI fetches a session cookie and stores it unencrypted in the configs path. If you omit the password, the CLI prompts after each command that needs authentication.

On macOS, Homebrew installs the CLI with `brew install influxdb-cli`. The username and password option is `--username-password` (short form `-p`), and the config command also takes `--config-name`, `--host-url`, `--org`, `--token` and `--active`.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 pages "Use tokens" and "influx CLI", article bodies read from the downloaded text (use-tokens lines 574-588, CLI page lines 585-720).

Removed: the claim that the CLI is versioned separately from influxd and the `Authorization: Token` header sentence, neither stated on these two pages.
