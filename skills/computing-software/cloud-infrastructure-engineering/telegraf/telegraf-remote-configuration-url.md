---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-remote-configuration-url
name: telegraf-remote-configuration-url
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [config-url, remote-config, watch-interval, telegraf-controller, retry]
level: practitioner
status: docs-checked
description: "Covers loading Telegraf configuration from an HTTP or HTTPS URL, retry attempts and the watch interval. Use for centrally served configs."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/file/", "https://docs.influxdata.com/telegraf/v1/commands/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Loading configuration from a URL

Pass an HTTP or HTTPS URL to `--config` to load configuration from a remote endpoint such as a configuration service or object store. Telegraf Controller serves managed configurations over a URL; point each agent's `--config` at the URL the Controller provides for it.

```sh
telegraf --config "http://example.com/telegraf.conf"
```

## Flags

- `--config-url-retry-attempts`: how many times to try fetching the remote configuration during startup. Default 3; `-1` means unlimited.
- `--config-url-watch-interval`: how often to check the URL for an update. Disabled by default. At each interval Telegraf sends an HTTP HEAD request and compares the `Last-Modified` header. If it changed, Telegraf reloads with the new configuration. If the check fails, Telegraf logs a warning and keeps running the existing configuration.

For a remote configuration, `telegraf config migrate` stores the migrated copy in the current directory, using the URL as the file name with a `.migrated` suffix.

Because a remote source can change what the agent collects and where it sends data, serve it over HTTPS and restrict who can change it.

## Checked

Method: docs-checked 2026-11-09 against the influxdata docs-v2 sources for the Telegraf configuration file page (URL section read in full) and the commands reference (config-url flag rows), plus the config migrate page for the remote-migration note.
