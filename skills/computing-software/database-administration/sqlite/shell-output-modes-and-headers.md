---
id: computing-software.database-administration.sqlite.shell-output-modes-and-headers
name: shell-output-modes-and-headers
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-output-mode, sqlite3-shell, sqlite-cli, output-formatting]
level: practitioner
status: verified
description: "Control sqlite3 shell output with .mode (box, table, json, markdown, csv, insert, line), .headers, .width, .nullvalue and .once/.output for reports and exports."
sources:
  - https://sqlite.org/cli.html#changing_output_formats
  - https://sqlite.org/cli.html#writing_results_to_a_file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sqlite3 output formats

## Modes
```text
.mode box          -- Unicode box table, headers on (box, json, markdown and table arrived in 3.33.0, per its release log); good for humans
.mode table        -- ASCII table
.mode markdown     -- paste into docs/PRs
.mode json         -- array of objects, for scripts (3.33+)
.mode csv          -- with .headers on for a header row
.mode tabs         -- TSV
.mode line         -- one column per line, good for wide rows
.mode insert orders  -- INSERT statements into table "orders"
.mode quote        -- SQL literals, shows blobs as X'..'
.mode list         -- default: pipe-separated (.separator to change)
```
In 3.54.1 `.mode` takes options, processed left to right: `--wrap N` (wrap columns wider than N; `--ww` is short for `--wordwrap on`), `--quote ARG` (off/on/sql/relaxed/csv/html/tcl/json), `--null STRING`, `--blob-quote ARG`, `--align`, `--border on|off`, `--limits`; list modes with `.mode --list`. Example: `.mode box --wrap 20 --wordwrap on` wrapped a 46-character value over three lines. Option availability by version was not checked.

## Supporting settings
```text
.headers on
.nullvalue NULL          -- show NULLs visibly instead of empty strings (3.54.1: set it AFTER `.mode`; `.nullvalue NULL` followed by `.mode box` showed an empty cell, while `.mode box` then `.nullvalue NULL`, or `.mode box --null NULL`, showed NULL)
.width 10 30 -8          -- column widths for column/table modes (negative = right-align)
.show                    -- current settings
```

## Sending output to files
```text
.once report.csv         -- next query only
.output all.txt          -- until .output with no argument
.once -x                 -- open next result in the system spreadsheet app (CSV)
.excel                   -- alias for .once -x
```

## Non-interactive
```bash
sqlite3 -json app.db "SELECT id, email FROM users LIMIT 5" | jq .
sqlite3 -csv -header app.db "SELECT * FROM orders" > orders.csv
sqlite3 -box app.db "SELECT count(*) FROM orders"
```
Mode flags on the command line: `-box -json -markdown -csv -table -line -html -list -quote`.

## Gotchas
- `.mode csv` quotes per RFC 4180; Excel may still mis-detect encodings: UTF-8 BOM is not added. Use `.excel` or import with explicit encoding.
- JSON mode (3.54.1) wrote the BLOB `x'DEADBEEF'` as the string `"\u00de\u00ad\u00be\u00ef"` (each byte as a code point), not hex; `--blob-quote hex` printed bare `deadbeef`, which is not valid JSON. Numbers stay numbers and an integer beyond 2^53 (9007199254740993) was written exactly, so JavaScript consumers will lose precision on parse. `.mode quote` shows the blob as `x'deadbeef'`.
- Put persistent preferences in `~/.sqliterc` (`.mode box`, `.headers on`, `.nullvalue NULL`), with `.nullvalue` after `.mode`.

## Verify
`.show` lists `mode: box` and `headers: on` (its layout in 3.54.1 is a right-aligned list with `nullvalue: ""`, `width:` and so on); a NULL in a test query displays as `NULL`.
