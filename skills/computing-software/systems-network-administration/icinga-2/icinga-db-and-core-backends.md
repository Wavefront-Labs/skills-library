---
id: computing-software.systems-network-administration.icinga-2.icinga-db-and-core-backends
name: icinga-db-and-core-backends
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, icinga-db, icingadb, redis, core-backends, icinga-web]
level: practitioner
status: docs-checked
description: "Understand the Icinga DB stack (icingadb feature, Redis, Icinga DB daemon, Icinga DB Web) and how it relates to the REST API and IDO."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/14-features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Icinga DB and core backends
The docs list two core backends: the REST API (documented as a core feature) and Icinga DB.

**Icinga DB** is a set of components:
1. Icinga 2 with the `icingadb` feature enabled. It publishes monitoring data to a Redis server: configuration and runtime updates, check results, state changes, downtimes, acknowledgements, notifications and events such as flapping.
2. The Icinga DB daemon, which synchronizes data between Redis and a database.
3. Icinga Web with the Icinga DB Web module, which connects to both Redis and the database to show current data.

Set up Redis and the feature by following the Icinga 2 installation guide; feature options are on the IcingaDB object type page.

The older IDO database (`ido-mysql`, `ido-pgsql`) is listed under deprecated features in the same chapter. In an HA master zone only one node writes at a time (see the HA skill).

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/14-features/.
IDO is listed under Deprecated Features. No commands were run.
