---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-test-and-once-modes
name: telegraf-test-and-once-modes
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [test-mode, once-mode, test-wait, validation, dry-run]
level: intro
status: docs-checked
description: "Explains telegraf --test and --once, what each runs and writes, and --test-wait for service inputs. Use to validate a config before running the service."
sources: ["https://docs.influxdata.com/telegraf/v1/administer/troubleshoot/", "https://docs.influxdata.com/telegraf/v1/commands/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# --test and --once

## --test

```bash
telegraf --config telegraf.conf --test
```

Gathers metrics once, prints them to standard output and exits. It runs inputs, processors and aggregators, but not outputs, so nothing reaches your destinations. It is also the one mode that does not require an output plugin.

Service inputs that wait for pushed data may not emit before Telegraf exits. Give them time with `--test-wait <seconds>`; the flag also applies to once mode.

## --once

```bash
telegraf --config telegraf.conf --once
```

Runs one complete execution of every plugin, including processors, aggregators and outputs, then exits. Unlike `--test`, it writes to the configured outputs.

## Workflow

1. `--test` to confirm the expected metrics appear.
2. If data does not arrive at the destination, add a file output to see exactly what is sent:

```toml
[[outputs.file]]
  files = ["stdout"]
```

3. `--once` to exercise the real output path.

Use `--input-filter` and `--output-filter` to narrow a run to the plugins under test.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Commands page (--test, --once, --test-wait), Configuration file page (--test needs no output), troubleshoot page (file output to stdout). Removed: nothing.

Method: documentation only; no commands were run.
