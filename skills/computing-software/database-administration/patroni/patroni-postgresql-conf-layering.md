---
id: computing-software.database-administration.patroni.patroni-postgresql-conf-layering
name: patroni-postgresql-conf-layering
category: computing-software
field: database-administration
product: patroni
tags: [patroni, postgresql-conf, custom-conf, alter-system, configuration]
level: advanced
status: docs-checked
description: "How Patroni composes postgresql.conf from base file, dynamic options, ALTER SYSTEM and command-line values."
sources:
  - https://patroni.readthedocs.io/en/latest/patroni_configuration.html
  - https://patroni.readthedocs.io/en/latest/yaml_configuration.html
  - https://patroni.readthedocs.io/en/latest/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: predict which value wins and where to put manual settings.

When applying configuration, Patroni:
1. Checks for `postgresql.base.conf` or the `custom_conf` parameter.
2. If `custom_conf` is set, that file is the base and `postgresql.base.conf` and `postgresql.conf` are ignored.
3. Otherwise, if `postgresql.base.conf` exists it is the base; if not, the original postgresql.conf is renamed to `postgresql.base.conf`.
4. Dynamic options are dumped into postgresql.conf, with an include of the base file.

Priority, lowest to highest:
1. postgresql.base.conf (or the custom_conf file)
2. postgresql.conf
3. postgresql.auto.conf (ALTER SYSTEM, per node)
4. run-time parameters passed with `-o --name=value`

`custom_conf` must exist on all nodes, be readable by PostgreSQL, and is included from its location. Patroni does not monitor or back it up, but its settings can still be overridden by Patroni's own configuration.

FAQ guidance: you may edit GUCs via `$PGDATA/postgresql.base.conf`, a `custom_conf`, or ALTER SYSTEM / ALTER DATABASE / ALTER USER, but managing everything through Patroni is recommended because Patroni may overwrite manual edits.

If an option requiring restart changes, `pending_restart` is set on the node and reset on any restart.

## Checked

2026-11-08: the base file and custom_conf procedure and the parameter priority order confirmed in the Patroni configuration page; custom_conf requirements confirmed in the YAML configuration page; the FAQ guidance on editing GUCs confirmed in the FAQ. Pages were read in full except where noted. Partial read: the YAML configuration page was searched for custom_conf only.

Method: documentation only; no commands were run.
