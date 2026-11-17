---
id: computing-software.database-administration.dragonfly.dbfilename-timestamp-macro
name: dbfilename-timestamp-macro
category: computing-software
field: database-administration
product: dragonfly
tags: [dbfilename, timestamp-macro, snapshot-files, dragonfly]
level: practitioner
status: docs-checked
description: "Control Dragonfly snapshot file names with dbfilename, the {timestamp} macro and date macros, and disable save and load with an empty value."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/backups.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`dbfilename` sets the name Dragonfly uses to save and load snapshots.

- Give the filename only, without extension. For `dump.dfs` (the Dragonfly snapshot extension) set `dump`.
- Default is `dump-{timestamp}`.
- `{timestamp}` is replaced with the local server time on each save, in a lexicographically sortable format. The flag reference also lists `{Y}`, `{m}` and `{d}` macros.
- An empty `dbfilename` disables both automatic backup on shutdown and automatic loading at startup.
- `dir` is the directory for snapshot files; it can also be an `s3://` URL.
- `df_snapshot_format` is `true` by default, which saves snapshots in the Dragonfly file format.

Example:

```shell
./dragonfly --logtostderr --dir my-snapshot-dir --dbfilename my-snapshot-file-{timestamp}
```

Two `SAVE` commands about 5 seconds apart plus a shutdown about 5 seconds later yield three timestamped snapshots, each with a `-0000.dfs` file and a `-summary.dfs` file.

## Checked

2026-11-04: confirmed against the Saving Backups page and the flags page (dbfilename default, `{timestamp}`, `{Y}`/`{m}`/`{d}`, empty value, dir, df_snapshot_format, example). Removed "set it false for RDB" and the claim that a static name avoids unbounded disk growth, which the pages do not state.
Method: documentation only; no commands were run.
