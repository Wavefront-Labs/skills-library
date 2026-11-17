---
id: computing-software.collaboration-platform-administration.matrix-synapse.port-sqlite-to-postgres
name: port-sqlite-to-postgres
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, sqlite, postgresql, synapse-port-db, migration, vacuum, homeserver-db]
level: advanced
status: docs-checked
description: "Migrate a Synapse SQLite database to PostgreSQL with synapse_port_db: snapshot, repeated runs, final run after shutdown, config swap, never VACUUM the SQLite file between runs."
sources:
  - https://element-hq.github.io/synapse/latest/postgres.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `synapse_port_db` script converts a SQLite-backed Synapse to PostgreSQL in two phases: run it against an offline copy of the SQLite file, then stop the server, run it once more to catch data written since, and restart against Postgres. The script can be killed and restarted at any time and is designed to be re-run against newer snapshots.

Never `VACUUM` the SQLite database between runs. That can produce an inconsistent copy in Postgres. The script checks that SQLite `auto_vacuum` is off but cannot detect a manual VACUUM or one from an automated task, so check for those yourself.

Procedure from the docs:

```sh
synctl stop
cp homeserver.db homeserver.db.snapshot
synctl start
cp homeserver.yaml homeserver-postgres.yaml
```

Edit the `database` section in `homeserver-postgres.yaml` to the Postgres settings, then:

```sh
synapse_port_db --sqlite-database homeserver.db.snapshot \
    --postgres-config homeserver-postgres.yaml
```

`--curses` shows a coloured progress UI, but it errors out if your terminal is too small. If it took long, repeat with a fresh snapshot. For the final pass, stop Synapse and run the script against the live `homeserver.db`, then swap configs:

```sh
synctl stop
mv homeserver.yaml homeserver-old-sqlite.yaml
mv homeserver-postgres.yaml homeserver.yaml
synctl start
```

Plan disk: the database can use 25% to 100% more space after porting. Create the target database with the correct encoding and locale first; see the Postgres setup skill.

## Checked

2026-11-04. Confirmed against the Synapse Using Postgres page (Porting from SQLite): two-phase process, VACUUM warning, auto_vacuum check, --curses, 25% to 100% extra space, command sequence. Nothing removed.
Method: documentation only; no commands were run.
