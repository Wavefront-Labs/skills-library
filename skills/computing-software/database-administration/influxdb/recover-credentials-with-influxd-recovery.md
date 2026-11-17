---
id: computing-software.database-administration.influxdb.recover-credentials-with-influxd-recovery
name: recover-credentials-with-influxd-recovery
category: computing-software
field: database-administration
product: influxdb
tags: [recovery, influxd-recovery, password-reset, bolt-path, lockout]
level: advanced
status: docs-checked
description: "Regain access with influxd recovery user update, list and create when you lose the admin password, using --bolt-path for custom stores."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/users/recover-credentials/
  - https://docs.influxdata.com/influxdb/v2/admin/tokens/create-token/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

When no one can log in, use the `influxd` command line interface (not `influx`) to recover credentials:

```sh
influxd recovery user list
influxd recovery user update --username example-username --password NEW_PASSWORD
influxd recovery user create --username example-username --password NEW_PASSWORD
```

If you started InfluxDB with a custom `bolt-path`, pass it with the `--bolt-path` flag so the command edits the right BoltDB file.

If you are unsure of the username, list users first, or create a user for recovery purposes.

To create a new operator token without using an existing one, the token docs point to the `influxd recovery auth` CLI (subcommands `create-operator` and `list`); see that command's reference for its flags.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 pages "Recover InfluxDB user credentials" and "Create an API token", relevant sections read from the downloaded text.

Removed: the claim that these commands run offline or directly on the metadata store, and the "documented route when the operator token is lost" wording, which the pages do not state.
