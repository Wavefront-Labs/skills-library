---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-toml-configuration-pitfalls
name: telegraf-toml-configuration-pitfalls
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [toml, table-ordering, inline-tables, literal-strings, durations]
level: practitioner
status: docs-checked
description: "Lists the TOML details that most often break Telegraf configs: table ordering, inline tables, string escaping on Windows paths and duration syntax."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/toml/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TOML pitfalls in Telegraf configs

Validate with a TOML validator or `telegraf --test`.

## Tables and arrays of tables

`[agent]` is a single table, defined once across all files. Plugins are arrays of tables with double brackets (`[[inputs.file]]`), and each definition is an independent instance.

## Table ordering

A sub-table such as `[inputs.cpu.tags]` must come at the end of the plugin definition. Every key after a table header belongs to that table regardless of indentation:

```toml
[[inputs.cpu]]
  totalcpu = true
  [inputs.cpu.tags]
    tag1 = "foo"
  percpu = false  # becomes a tag named percpu, not an option
```

Inline tables avoid the problem and can go anywhere in the definition:

```toml
[[inputs.cpu]]
  tags = {tag1 = "foo", tag2 = "bar"}
  percpu = false
```

## Strings

In double-quoted strings backslashes and quotes must be escaped; a Windows path with single backslashes is invalid. Use escaped backslashes or a single-quoted literal string. Literal strings cannot contain a single quote.

## Durations

A string of integer plus unit: `ns`, `us` (or `µs`), `ms`, `s`, `m`, `h`, for example `"10s"` or `"1m"`.

## Checked

Method: docs-checked 2026-11-09 against the TOML syntax for Telegraf page (raw markdown in github.com/influxdata/docs-v2, read in full). Dropped the unconfirmed claim that the ordering rule extends to `tagpass`, `tagdrop` and `labels`.
