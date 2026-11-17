---
id: computing-software.database-administration.patroni.patroni-bootstrap-dcs-and-initdb
name: patroni-bootstrap-dcs-and-initdb
category: computing-software
field: database-administration
product: patroni
tags: [patroni, bootstrap, initdb, dcs, data-checksums]
level: practitioner
status: docs-checked
description: "Configure the bootstrap section: bootstrap.dcs seeding, initdb options, post_bootstrap, and why later edits are ignored."
sources:
  - https://patroni.readthedocs.io/en/latest/yaml_configuration.html
  - https://patroni.readthedocs.io/en/latest/replica_bootstrap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: seed a new cluster correctly the first time.

```
bootstrap:
  dcs:
    ttl: 30
  method: initdb
  initdb:
    - data-checksums
    - encoding: UTF8
  post_bootstrap: /path/to/script
```

- `bootstrap.dcs` is written into `/<namespace>/<scope>/config` after Patroni initializes the new cluster. It may contain any parameter from dynamic configuration.
- Once the cluster is initialized and settings are stored in the DCS, all later changes to `bootstrap.dcs` have no effect. Use `patronictl edit-config` or the REST API instead.
- `method` selects a custom bootstrap script. `initdb` (or no `method`) triggers the default initdb command.
- `initdb` is a list of options passed to initdb; `data-checksums` must be enabled when pg_rewind is needed on 9.3, `encoding` and `locale` set defaults for new databases.
- `post_bootstrap` (or `post_init`) is a script run after initialization. It receives a connection string URL with the cluster superuser as user name, and the `PGPASSFILE` variable points to the pgpass file.

Bootstrap versus replica creation: Patroni creates replicas only if the `initialize` key exists in the DCS. With no `initialize` key, bootstrap runs exclusively on the first node that takes the initialize lock.

## Checked

2026-11-08: bootstrap.dcs, method, initdb options, post_bootstrap/post_init and the one-time effect of bootstrap.dcs confirmed in the YAML configuration page; the bootstrap versus replica creation rule confirmed in the replica bootstrap page. Pages were read in full except where noted. Partial read: the YAML configuration page was read for the bootstrap section only.

Method: documentation only; no commands were run.
