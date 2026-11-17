---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-convert-command
name: grafana-alloy-convert-command
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [alloy-convert, source-format, convert-report, bypass-errors, extra-args, config-conversion]
level: practitioner
status: docs-checked
description: "Convert Prometheus, Promtail, Grafana Agent Static and OpenTelemetry Collector configs to Alloy with alloy convert, report output and defaults handling."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/cli/convert.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# alloy convert

Public preview. Converts a supported config to Alloy syntax.

```shell
alloy convert --source-format=prometheus --output=/path/to/config.alloy --report=/path/to/report.txt /path/to/prometheus.yml
```
With no file or `-` it reads stdin. Flags:
- `--source-format` / `-f` (required): `otelcol`, `prometheus`, `promtail`, `static`.
- `--output` / `-o`: where to write the converted config.
- `--report` / `-r`: where to write a diagnostic report.
- `--bypass-errors` / `-b`: continue past non-critical conversion errors where output can still be generated. Review the result, since it may not be equivalent.
- `--extra-args` / `-e`: pass flags of the original tool.

## Source versions
- `prometheus`: Prometheus v2.45 features (`scrape_config`, `relabel_config`, `metric_relabel_configs`, `remote_write`, many `*_sd_configs`).
- `promtail`: Promtail v2.8.x, nearly all features.
- `static`: Grafana Agent Static. `--extra-args="-enable-features=integrations-next"` converts integrations-next configs and `-config.expand-env` expands environment variables; combine with spaces.
- `otelcol`: many OpenTelemetry Collector components, mapped to `otelcol.*`.

## Defaults
Source values equal to Alloy defaults are omitted. If an unset source default differs from the Alloy default, the Alloy default value is written explicitly. Unsupported features raise errors; warnings flag options needing attention.

## Checked

2026-11-04. Confirmed against the convert CLI reference (reference/cli/convert.md): flags and short forms, source formats, stdin behaviour, defaults handling, Prometheus v2.45 and Promtail v2.8.x versions, static extra-args. No claims changed.

Method: documentation only; no commands were run.
