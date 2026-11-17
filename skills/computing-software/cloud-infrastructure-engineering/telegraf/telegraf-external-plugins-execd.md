---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-external-plugins-execd
name: telegraf-external-plugins-execd
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [external-plugins, execd, shim, go, custom-plugin]
level: advanced
status: docs-checked
description: "Explains external Telegraf plugins run through execd and how to extract an internal plugin to a stand-alone binary using the Go shim."
sources: ["https://docs.influxdata.com/telegraf/v1/configure_plugins/external_plugins/", "https://docs.influxdata.com/telegraf/v1/configure_plugins/external_plugins/shim/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# External plugins and the execd shim

External plugins are programs built outside Telegraf and run through `inputs.execd`, `processors.execd` or `outputs.execd`. They can be written in any language, use non-Go or CGO libraries, include licensed software or large dependencies, and run without waiting for the Telegraf team to review and publish them.

## Extracting a plugin with the shim

1. Move the plugin to its own repo, keeping the path (for example `plugins/inputs/cpu`).
2. Copy the shim example `main.go` into `cmd/` and import your plugin. The shim runs one plugin only, so use one plugin per repo.
3. Add a `plugin.conf` with plugin-specific settings. Keep it separate from other Telegraf configs and out of any shared directory, or Telegraf will read it without knowing which plugin it belongs to.

## Build and test

```bash
go build -o plugin-name cmd/main.go
./plugin-name -config plugin.conf
```

For a processor or output, feed valid metrics on STDIN first; metrics are written to STDOUT. Press Ctrl-C to end.

## Wire into Telegraf

```toml
[[inputs.execd]]
  command = ["/path/to/plugin-name", "-config", "/path/to/plugin.conf"]
  signal = "none"
```

Community plugins can be listed by opening a pull request to the EXTERNAL_PLUGINS list in the Telegraf repo.

## Checked

Method: docs-checked 2026-11-09 against the influxdata docs-v2 sources for "Integrate with external plugins" and "Use the execd shim", both read in full. An unsupported claim about delivery acknowledgement was removed.
