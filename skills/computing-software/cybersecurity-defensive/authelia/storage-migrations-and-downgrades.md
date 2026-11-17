---
id: computing-software.cybersecurity-defensive.authelia.storage-migrations-and-downgrades
name: storage-migrations-and-downgrades
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, schema-migration, storage-migrate, downgrade, schema-info, database-upgrade]
level: advanced
status: docs-checked
description: "Understand Authelia's automatic schema upgrades on startup and how to list, apply and reverse migrations with authelia storage migrate before rolling back a release."
sources:
  - https://www.authelia.com/configuration/storage/migrations/
  - https://www.authelia.com/reference/cli/authelia/authelia_storage_migrate_up/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authelia upgrades the database schema automatically on startup. Downgrading Authelia is the hard direction: an older binary may not understand a newer schema, so you must migrate the schema down first with a version of Authelia that supports the current schema.

The migrations page maps schema versions to the Authelia release that introduced them. Examples: schema 1 arrived in 4.33.0 (the first managed migration), schema 2 in 4.34.0 (WebAuthn tables), schema 4 in 4.35.0 (OpenID Connect storage tables), and schema 8 in 4.38.0 (pushed authorization requests). All releases between two listed versions use the earlier schema, so to run an older release you need the schema to be at or below what it supports.

Commands under `authelia storage migrate`:

```bash
authelia storage schema-info --config /path/to/configuration.yml
authelia storage migrate history
authelia storage migrate list-up
authelia storage migrate list-down
authelia storage migrate up --target 20
authelia storage migrate down --target 8
```

`migrate up` runs the migrations available in the installed Authelia that are above the current schema version, up to the latest by default, and takes `-t, --target` to stop short. `migrate down` runs migrations below the current version to a `--target`, and has a `--destroy-data` flag confirming you accept data destruction by that migration. The schema map also has a `pre1` entry (4.0.0 to 4.32.2); the table says downgrading to it requires the `--pre1` flag on Authelia 4.37.2, while its prose says a 4.33.0 or newer binary is needed.

Back up the database before any migration, since reversing migrations can destroy data.

Check: after migration, `schema-info` reports the target version and Authelia starts cleanly on the intended release.

## Checked

2026-11-08. Read in full: storage/migrations, CLI pages for migrate up, down, history, list-up, list-down, schema-info. Added --destroy-data and the pre1 note; schema version examples verified against the table.

Method: documentation only; no commands were run.
