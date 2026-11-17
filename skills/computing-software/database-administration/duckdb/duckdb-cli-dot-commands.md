---
id: computing-software.database-administration.duckdb.duckdb-cli-dot-commands
name: duckdb-cli-dot-commands
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, cli, dot-commands, output, once, import, progress-bar, highlighting]
level: intro
status: docs-checked
description: "DuckDB CLI dot commands: .mode, .output and .once redirection, .tables and .schema, .timer, .read, .import, progress bar components and highlighting."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/clients/cli/dot_commands.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/clients/cli/output_formats.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: drive the DuckDB shell efficiently with dot commands.

Syntax: a dot command starts at column 0 with `.`, takes space-separated arguments (quote args containing spaces), stays on one line and needs no semicolon. `.help` lists them; `.help m` filters by text; `.show` prints current settings. Unambiguous prefixes autocomplete silently (`.mo ma` = `.mode markdown`), but avoid shorthands in scripts.

Frequently used:
- Navigation and schema: `.databases`, `.tables [LIKE-pattern]` (`.tables %l%`), `.schema [PATTERN]`, `.indexes TABLE`, `.open [OPTIONS] FILE`, `.cd DIR`.
- Output: `.mode MODE [TABLE]` (bare `.mode` reports current, default `duckbox`), `.headers on|off` (not duckbox), `.nullvalue STRING`, `.separator COL ROW`, `.maxrows COUNT` (default 40, duckbox), `.maxwidth COUNT` (0 = terminal width), `.width N1 N2 ...`, `.columns` / `.rows`, `.large_number_rendering all|footer|off` (default footer).
- Timing and errors: `.timer on|off` (statements joined by `;` on one line are timed together), `.bail on|off` (stop on error, default off), `.echo on|off`, `.changes on|off`.
- Scripts and shell: `.read FILE`, `.print STRING`, `.shell CMD` or `.system CMD`, `.log FILE|stderr|stdout|off`, `.exit CODE`, `.quit`, `.safe_mode` (see duckdb-cli-arguments-safe-mode).

Redirect results:

```sql
.mode markdown
.output my_results.md      -- all later output; each result overwrites the file
SELECT 'taking flight' AS output_column;
.output                    -- back to stdout
.mode csv
.once my_output_file.csv   -- only the next result
```
`.once -e` opens the result in the default text editor, `.once -x` (same as `.excel`) opens a CSV in the spreadsheet app, and `.once |pbcopy` pipes to the macOS clipboard.

Importing (deprecated, kept for compatibility; prefer `read_csv` or `COPY`): create the table first, then `.import FILE TABLE [--skip N] [--csv]`. It uses the current `.mode` and `.separator` unless `--csv` is given.

Progress bar: `SET progress_bar_time = 100;` (ms before showing). Components are additive: `.progress_bar --add "{align:right}{min_size:20}{color:red}Time: {sql:select (current_time::varchar).split('.')[1]}{color:reset} "`; `.progress_bar --clear` resets.

Highlighting: `.highlight on|off`; colors `.keyword red`, `.constant blue` or raw codes `.keywordcode 033[31m`; result tables `.highlight_colors layout red`, `.highlight_colors column_name yellow bold_underline`, components `layout`, `column_type`, `column_name`, `numeric_value`, `temporal_value`, `string_value`, `footer`; `.highlight_results off`.

## Checked

2026-11-07. Read the Dot Commands page in full and confirmed the syntax rules, command list and defaults (`.maxrows` 40, `.large_number_rendering` footer, `.bail` off), `.output` and `.once` behaviour including `-e`, `-x` and `.once |pbcopy`, schema commands, progress bar `--add` and `--clear`, `progress_bar_time`, highlighter commands and components, shorthands and the deprecated `.import` with `--skip` and `--csv`. The bare `.mode` report and the duckbox default are on the Output Formats page (added to sources). Removed the Verify step.

Method: documentation only; no commands were run.
