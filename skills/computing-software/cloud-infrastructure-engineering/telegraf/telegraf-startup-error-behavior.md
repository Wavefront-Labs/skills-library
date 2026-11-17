---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-startup-error-behavior
name: telegraf-startup-error-behavior
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [startup-error-behavior, retry, probe, resilience, plugins]
level: advanced
status: docs-checked
description: "Describes the startup_error_behavior option (error, ignore, retry, probe) for plugins that connect to external services. Use when a dependency may be down at agent start."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/plugin-options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# startup_error_behavior

Plugins that connect to external services support `startup_error_behavior`, controlling what Telegraf does when the plugin fails to start.

| Value | Effect |
| --- | --- |
| `error` (default) | Telegraf stops and exits. |
| `ignore` | Telegraf disables that plugin and continues with all others. |
| `retry` | Telegraf retries starting the plugin on every gather or write cycle. The plugin stays disabled until startup succeeds. |
| `probe` | Telegraf probes the plugin, if it supports probing, and disables it if the probe fails. Without probe support it behaves like `ignore`. |

```toml
[[outputs.influxdb_v3]]
  urls = ["http://localhost:8181"]
  startup_error_behavior = "retry"
```

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Plugin options page, Startup error behavior section. Removed: the advice on choosing retry or ignore and the claim about buffering during startup retry, which the page does not state.

Method: documentation only; no commands were run.
