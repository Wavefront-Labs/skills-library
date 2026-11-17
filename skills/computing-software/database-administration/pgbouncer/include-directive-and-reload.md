---
id: computing-software.database-administration.pgbouncer.include-directive-and-reload
name: include-directive-and-reload
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, include, reload, sighup, config-file]
level: intro
status: docs-checked
description: "The ini file format, %include directive, conffile, and how RELOAD or SIGHUP re-reads configuration."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: split and reload configuration.

pgbouncer.ini is in ini format with sections in square brackets ([databases], [users], [peers], [pgbouncer]). Lines starting with `;` or `#` are comments; those characters are not special later in the line.

Include another file with:

```
%include filename
```

A relative filename is taken relative to the current working directory, not the including file.

`conffile` shows the current config file location; changing it makes PgBouncer use another file at the next RELOAD or SIGHUP. Its default is the file from the command line.

Reloading: the console command `RELOAD;` or SIGHUP re-reads the main configuration and the files named by auth_file and auth_hba_file, and updates changeable settings. If a reload changes a database's connection parameters, existing server connections to the old destination are closed when next released (per pooling mode) and new connections use the new parameters immediately.

Not every setting can change at runtime. SHOW CONFIG lists key, value, default and a changeable column (yes or no); no means boot-time only. Use `SET key = arg;` on the console for runtime changes, for example `SET log_connections = 1;`.

After rotating the log file, send HUP or run RELOAD so PgBouncer reopens it.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
