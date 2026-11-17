---
id: computing-software.database-administration.pgbackrest.option-types-and-reset
name: option-types-and-reset
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, options, option-types, boolean, size]
level: practitioner
status: docs-checked
description: "Option value types (boolean, size, time, list, key/value) and the no- prefix for booleans."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write option values pgBackRest will accept.

Types defined in the configuration reference:

- string and path: plain text; paths are absolute.
- boolean: `y` or `n` in the file. On the command line, `--option` sets it and `--no-option` clears it.
- integer: whole numbers within a documented range.
- size: a number with an optional unit from KiB up to PiB; fractions are not allowed (use `2560MiB`, not `2.5GiB`).
- time: seconds, so `--io-timeout=90`.
- list: the option is repeated (for example `--exclude`).
- key/value: given as `key=value` and repeated (for example `--recovery-option`).

On the command line `--no-` negates a boolean:

```
pgbackrest --stanza=demo --no-start-fast backup
```

Repository options are indexed (`repo1-path`, `repo2-path`), as are PostgreSQL options (`pg1-path`, `pg2-path`).

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html). Removed: the --reset- prefix, which is not documented on the fetched pages, and example values not on the page. 

Method: documentation only; no commands were run.
