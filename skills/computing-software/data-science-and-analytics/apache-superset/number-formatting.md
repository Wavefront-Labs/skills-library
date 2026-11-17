---
id: computing-software.data-science-and-analytics.apache-superset.number-formatting
name: number-formatting
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [number-formatting, d3-format, smart-number, duration, memory]
level: intro
status: docs-checked
description: "Format numbers in Superset charts: SMART_NUMBER, ~g, D3 format strings, DURATION, MEMORY and LENGTH presets, and exact decimals in SQL Lab."
sources:
  - https://github.com/apache/superset/blob/master/docs/docs/using-superset/number-formatting.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: show numbers the way readers expect.

Most chart types have a Number format control (labelled D3 Format, Y Axis Format or similar), in the Customize tab or a metric's popover editor. Pick a preset or type a custom D3 format string. If an axis control's chart has Comparison display set to Percentage, the choices narrow to percentage-only presets, hiding `SMART_NUMBER`, `~g` and the duration, memory and length presets.

General presets:
- `SMART_NUMBER`: adaptive formatting that picks a reasonable precision from the value.
- `~g`: original value in D3 general format (trims trailing zeros; may switch to exponential for very large or small values).

D3 strings in the dropdown: `,d` (integer, comma-grouped), `.1s` and `.3s` (SI prefix), `,.1%`, `.2%`, `.3%` (percentages), `.4r` (4 significant digits), `,.1f`, `,.2f`, `,.3f` (fixed-point, comma-grouped), `+,` (always shows sign) and `$,.2f` (currency).

Duration (input in ms): `DURATION` (66000 => 1m 6s), `DURATION_SUB` (sub-second precision), `DURATION_COL` (10500 => 0:00:10.5).

Memory (input in bytes): `MEMORY_DECIMAL` (1024B => 1.024kB), `MEMORY_BINARY` (1024B => 1KiB), and `MEMORY_TRANSFER_RATE_DECIMAL` / `MEMORY_TRANSFER_RATE_BINARY` for rates (/s).

Length: `LENGTH` (meters to km, 12345m => 12.35km), `LENGTH_CM_KM` (cm to km), `LENGTH_CM_M` (cm to m).

Currency: some charts also offer currency formatting, including a dynamic mode that reads the currency from a column value.

Exact decimals in SQL Lab: database DECIMAL and NUMERIC results show as exact fixed-point text with trailing zeros and never in scientific notation. JSON responses use strings so the browser does not round long values; sorting stays numeric and CSV exports keep all digits.

## Checked

2026-11-08: read number-formatting.mdx in full. Removed claims not on the page: custom formats being reusable, "percent only on 0-1 ratios", per-control troubleshooting advice.
Method: documentation only; no commands were run.
