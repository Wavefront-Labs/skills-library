---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-datastore-options
name: k3s-datastore-options
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, datastore, sqlite, mysql, postgresql]
level: practitioner
status: docs-checked
description: "Pick a K3s datastore: embedded SQLite, embedded etcd, or an external etcd, MySQL, MariaDB or PostgreSQL database."
sources:
  - https://docs.k3s.io/datastore
  - https://docs.k3s.io/installation/requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose the datastore that fits your team and topology.

Options:

- Embedded SQLite: the default, used when no other datastore configuration exists and no embedded etcd files are on disk. Cannot be used with multiple servers. Suits simple short-lived clusters such as CI/CD.
- Embedded etcd: selected when K3s initializes or joins an etcd cluster, or etcd files exist on disk. Gives HA at the edge without running a separate database.
- External database: for teams without etcd expertise who prefer an enterprise SQL database.

Supported external datastores and certified versions:

- etcd 3.5.21
- MySQL 8.0 and 8.4
- MariaDB 10.11 and 11.4
- PostgreSQL 15.12, 16.7 and 17.3

Constraints:

- K3s requires prepared statements support from the DB, so connection poolers such as PgBouncer may need extra configuration.
- Multi-master databases that set auto_increment_increment or auto_increment_offset above 1 are not supported, because Kine expects the revision to start at 0 and move forward by exactly 1 per insert. This affects products such as Galera for MySQL/MariaDB.

For production and large clusters the Requirements page recommends HA with an external database (MySQL, PostgreSQL or etcd).

## Checked

2026-11-08. Read the full K3s Cluster Datastore page (docs/datastore/datastore.md) and the full Requirements page (docs/installation/requirements.md) in the k3s-io/docs repo. Confirmed: SQLite default and single-server limit, embedded etcd selection rules, the certified external datastore versions, prepared statement requirement, the auto_increment Kine restriction, and the large-cluster external database recommendation. Nothing removed.

Method: documentation only; no commands were run.
