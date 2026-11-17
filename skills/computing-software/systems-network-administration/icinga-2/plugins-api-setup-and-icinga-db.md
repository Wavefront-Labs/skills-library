---
id: computing-software.systems-network-administration.icinga-2.plugins-api-setup-and-icinga-db
name: plugins-api-setup-and-icinga-db
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, icinga-db, redis, api-setup, monitoring-plugins, icingadb-feature]
level: practitioner
status: docs-checked
description: "Post-install steps for Icinga 2: monitoring plugins, icinga2 api setup, and the Icinga DB stack (Redis, icingadb feature, daemon, Web)."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/02-installation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# plugins, API setup and Icinga DB
**Plugins.** Without plugins Icinga 2 cannot check external services. The Monitoring Plugins Project provides a large set, and they are required for the example configuration to work out of the box.

**API.** Almost every setup needs the API: Icinga Web and Icinga DB connect to it, and it enables cluster communication. For a single node, run:
```
icinga2 api setup
systemctl restart icinga2
```
This enables the `api` feature, sets up certificates and adds the API user `root` with an auto-generated password in `/etc/icinga2/conf.d/api-users.conf`. For HA or distributed setups read the Distributed Monitoring chapter instead.

**Icinga DB** consists of:
- Icinga 2 with the `icingadb` feature, publishing configuration, runtime updates, check results, state changes, downtimes, acknowledgements, notifications and flapping events to Redis
- the Icinga DB daemon, synchronising Redis and a database
- Icinga Web with the Icinga DB Web module, reading Redis and the database

Only Icinga 2 master nodes or single-node setups need the feature. A Redis server from version 6.2 is required.

Enable it and restart:
```
icinga2 feature enable icingadb
systemctl restart icinga2
```
The feature file `/etc/icinga2/features-available/icingadb.conf` is pre-configured for a local setup; edit it if Redis runs on another host or needs credentials (settings are in the IcingaDB object type).

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/02-installation/. No commands were run.
