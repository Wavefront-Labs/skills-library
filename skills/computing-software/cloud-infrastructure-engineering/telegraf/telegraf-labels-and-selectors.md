---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-labels-and-selectors
name: telegraf-labels-and-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [labels, selectors, select-flag, fleet, glob]
level: advanced
status: docs-checked
description: "Explains plugin labels and the --select flag for enabling subsets of a shared Telegraf configuration, including AND/OR rules and matching behaviour."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/labels-selectors/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Labels and selectors

Labels let many Telegraf instances share one configuration while each enables only some plugins. Add a `labels` table to any plugin and pass `--select` at startup.

```toml
[[inputs.cpu]]
  [inputs.cpu.labels]
    app = "payments"
    region = "us-east"
```

Keys and values are plain strings of alphanumerics, dots, dashes and underscores; no wildcards. `labels` is a TOML table, so with explicit table syntax it must be last in the plugin definition.

## Selecting

```bash
telegraf --config config.conf --config-directory directory/ \
  --select="app=payments;region=us-*" --select="env=prod"
```

- Pairs inside one `--select` are ANDed; multiple `--select` flags are ORed.
- Values accept `*` and `?`; keys do not. Repeating a key within one `--select` is a startup error.

## Behaviour

With `--select`, a labelled plugin is enabled only if a selector matches. An unlabelled plugin is always enabled. Without `--select`, every plugin is enabled. A selector matches when every pair in it matches a label; labels it does not mention are ignored. For example `app=web;region=us-west` skips a plugin labelled `app=web, region=us-east`.

## Checked

Method: docs-checked 2026-11-09 against the Select Telegraf plugins with labels and selectors page (raw markdown in github.com/influxdata/docs-v2, read in full). All claims confirmed.
