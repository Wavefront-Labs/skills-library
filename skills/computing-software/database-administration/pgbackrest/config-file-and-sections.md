---
id: computing-software.database-administration.pgbackrest.config-file-and-sections
name: config-file-and-sections
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, configuration, pgbackrest-conf, sections, stanza]
level: practitioner
status: docs-checked
description: "How pgbackrest.conf is organised: global, command and stanza sections, and where the default file lives."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: put each option in the right section.

The default configuration file is /etc/pgbackrest/pgbackrest.conf; the older /etc/pgbackrest.conf location is still checked as a fallback. Sections:

- `[global]` applies to all stanzas and commands.
- `[global:command]` applies to all stanzas for one command, such as `[global:archive-push]`.
- `[stanza]` applies to one stanza, such as `[demo]`.

```
[demo]
pg1-path=/path/to/pgdata

[global]
process-max=4
repo1-path=/var/lib/pgbackrest

[global:archive-push]
compress-level=3
process-max=2
```

Command sections are useful when one option should differ per command. The user guide sets `process-max` under `[global:archive-get]` and `[global:archive-push]` so backup and restore are not affected, and lets archive-push and archive-get use different values.

Show the effective values with the `--log-level-console=info` begin line of any command, which prints the options in force.

Option names in the file omit the leading dashes, so `--process-max=4` becomes `process-max=4`. Booleans use `y` and `n`.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html) (command sections). Removed: the INI-style claim and the section precedence order, which the fetched pages do not state, and the [stanza:command] section. 

Method: documentation only; no commands were run.
