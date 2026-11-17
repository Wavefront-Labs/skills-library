---
id: computing-software.database-administration.duckdb.duckdb-cli-output-formats
name: duckdb-cli-output-formats
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, cli, output-format, mode, markdown, json, csv, duckbox]
level: intro
status: docs-checked
description: "Pick a DuckDB CLI output mode (.mode): csv, json, jsonlines, markdown, insert, latex, box, line and others; separators and large-number rendering."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/clients/cli/output_formats.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/clients/cli/arguments.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/clients/cli/dot_commands.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make the CLI print results in the format the next tool (or reader) needs.

Query or set the mode with `.mode` (bare `.mode` prints `current output mode: duckbox`) or the matching command-line flag such as `-csv`, `-json`, `-markdown`.

Modes: `ascii` (columns and rows delimited by 0x1F and 0x1E), `box` (unicode box drawing), `csv`, `column` (size with `.width`), `duckbox` (default, feature-rich), `html` (`<table>`), `insert TABLE` (SQL INSERT statements for TABLE, handy for later replay), `json` (array), `jsonlines` (NDJSON), `latex` (tabular environment), `line` (one value per line), `list` (values delimited by `|`), `markdown`, `quote` (SQL-escaped values), `table` (ASCII-art), `tabs`, `tcl`, `trash` (no output).

```sql
.mode markdown
SELECT 'quacking intensifies' AS incoming_ducks;
.mode insert my_table
```
Combine with `.output FILE` or `.once FILE` to save (see duckdb-cli-dot-commands). `markdown` suits documentation, `latex` suits papers.

Separators: modes that use one (`csv`, `tabs`) reset it on mode change, so `.mode csv` sets `,`. Override afterward with `.separator "|"` to emit pipe-separated rows. Non-duckbox headers are controlled by `.headers on|off`.

`duckbox` extra: `.large_number_rendering` levels: `off` (plain numbers), `footer` (default; single-row results get a human-readable footer such as `(3.14 billion)`), `all` (replace all large numbers, for example `3.14 billion`).

Pattern for scripting: `duckdb -csv -c 'SELECT 42 AS hello'` or `duckdb -json -c '...'`.

## Checked

2026-11-07. Read the Output Formats page in full and confirmed the mode list and descriptions, bare `.mode` output, separator reset on mode change, and the three `large_number_rendering` levels with the `(3.14 billion)` footer. Command-line mode flags come from the Command Line Arguments page and `.headers`, `.nullvalue`, `.width` from the Dot Commands page (both added to sources). Removed the Verify step.

Method: documentation only; no commands were run.
