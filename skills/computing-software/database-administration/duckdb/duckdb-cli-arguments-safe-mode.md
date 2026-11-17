---
id: computing-software.database-administration.duckdb.duckdb-cli-arguments-safe-mode
name: duckdb-cli-arguments-safe-mode
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, cli, command-line, safe-mode, readonly, scripting]
level: practitioner
status: docs-checked
description: "DuckDB CLI command-line arguments (-c, -f, -init, -readonly, output flags), ordered processing, and safe mode restrictions."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/clients/cli/arguments.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/clients/cli/safe_mode.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/clients/cli/dot_commands.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: script the DuckDB CLI non-interactively, and lock it down when needed.

Run `duckdb -help` for the full list. Key arguments:
- Execution: `-c COMMAND` or `-s COMMAND` run and exit; `-cmd COMMAND` runs before reading stdin; `-f FILENAME` runs a script and exits (the init script is read first if it exists); `-init FILENAME` replaces the default init script; `-no-stdin` exits after options; `-batch` / `-interactive` force I/O style; `-bail` stops on first error; `-echo` prints commands.
- Database: `-readonly` (also supports attaching remote databases over HTTPS), `-append`, `-nofollow` (refuse symlinked database files), `-storage-version VER`, `-unsigned` (load unsigned extensions; for extension development, see duckdb-securing-duckdb), `-ui` (start the DuckDB UI, installing the `ui` extension if needed).
- Output mode flags: `-ascii -box -column -csv -html -json -line -list -markdown -quote -table`; `-header` / `-noheader`; `-separator SEP` (default `|`); `-newline SEP` (default `\n`); `-nullvalue TEXT` (default `NULL`). `-version` prints the version.

Arguments are processed in order, like the SQLite shell, so options only affect later commands:

```batch
duckdb -csv -c 'SELECT 42 AS hello' -json -c 'SELECT 84 AS world'
```
prints `hello` / `42` as CSV, then `[{"world":84}]` as JSON.

Safe mode (activated with the `.safe_mode` dot command): the CLI may only use the database file it first connected to and cannot touch the host file system.
- Disabled dot commands: `.cd`, `.excel`, `.import`, `.log`, `.once`, `.open`, `.output`, `.read`, `.sh`, `.system`.
- Autocomplete stops scanning the file system; the `getenv` function is disabled.
- `enable_external_access` becomes false: `ATTACH` cannot open database files, `COPY` cannot read or write files, and `read_csv`, `read_parquet`, `read_json` and similar cannot read external sources.
- It cannot be turned off again within that CLI session.

## Checked

2026-11-07. Read the Command Line Arguments, Safe Mode and Dot Commands pages. Confirmed every listed argument and its default (`-separator`, `-newline`, `-nullvalue`), the in-order processing example and its output, the list of disabled dot commands, auto-complete and `getenv` changes, `enable_external_access` effects and that safe mode cannot be turned off in the same session. Safe mode activation is shown only as the `.safe_mode` dot command (Dot Commands page, added to sources), so the unsupported 'or at startup' wording was removed, and so was the Verify step (no such error is documented).

Method: documentation only; no commands were run.
