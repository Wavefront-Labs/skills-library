---
id: computing-software.database-administration.influxdb.create-and-manage-telegraf-configs
name: create-and-manage-telegraf-configs
category: computing-software
field: database-administration
product: influxdb
tags: [telegraf, influx-telegrafs, configs, load-data, agents]
level: practitioner
status: docs-checked
description: "Create stored Telegraf configurations from the influx CLI or the UI so agents can fetch their config from InfluxDB."
sources:
  - https://docs.influxdata.com/influxdb/v2/tools/telegraf-configs/create/
  - https://docs.influxdata.com/influxdb/v2/write-data/no-code/use-telegraf/auto-config/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

InfluxDB can store Telegraf configurations and serve them to agents by URL.

CLI: upload a local file as a stored configuration. Name and description are optional and default to empty strings.

```sh
influx telegrafs create -n "Example config" -d "description" -f /path/to/telegraf.conf
```

A custom file should include the `outputs.influxdb_v2` output plugin, plus any Telegraf plugins you want (not all plugins are offered in the UI).

UI: Data (Load Data), Telegraf, Create Configuration. Pick the bucket, one or more plugin groups, name the configuration, then Save and Test. The Test Your Configuration page gives start instructions, and Listen for Data confirms the connection.

Start Telegraf with the token in the `INFLUX_TOKEN` environment variable and the stored config as the `-config` argument, for example `telegraf -config http://localhost:8086/api/v2/telegrafs/<id>`. On Linux and macOS the argument can be a file path or URL; on Windows it must be a local file path. The UI setup instructions give the exact command.

## Checked

Method: docs-checked 2026-11-09 against the full body of the Create a Telegraf configuration and Automatically configure Telegraf pages (OSS v2 docs). Dropped the unconfirmed claims that the CLI also lists, updates and removes configs, that the UI generates an API token, and the output-section and https notes.
