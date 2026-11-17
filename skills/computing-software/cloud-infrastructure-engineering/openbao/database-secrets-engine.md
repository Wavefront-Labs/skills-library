---
id: computing-software.cloud-infrastructure-engineering.openbao.database-secrets-engine
name: database-secrets-engine
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, database, dynamic-roles, static-roles, rotate-root]
level: practitioner
status: docs-checked
description: "Set up the OpenBao database secrets engine: config, rotate-root, dynamic and static roles, supported plugins and the root-credential trap."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/secrets/databases/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database secrets engine

```
bao secrets enable database
bao write database/config/my-database plugin_name="..." connection_url="..." allowed_roles="..." username="..." password="..."
bao write -force database/rotate-root/my-database
bao write database/roles/my-role db_name=my-database creation_statements="..." default_ttl="1h" max_ttl="24h"
```

## Roles

- **Dynamic**: a unique username and password per request; traceable by SQL username; revoked by the lease system on expiry.
- **Static**: one role maps to an existing database user; OpenBao stores and rotates its password on a schedule.

## Root credentials

Create a dedicated database user for OpenBao with permission to create, update and delete users, then run `rotate-root`. Afterwards the original password is inaccessible and only OpenBao knows it.

## Plugins

Cassandra, InfluxDB, MySQL/MariaDB, PostgreSQL, Valkey. All support root rotation, dynamic and static roles; only Valkey lacks username customization (see username-templating).

## Warning

Never manage the same root credentials you gave `config/` with static roles; the rotated password breaks every user managed through that configuration.

## Checked

2026-11-04. Confirmed against the Databases overview page: setup commands, dynamic and static roles, rotate-root and the lost root password, the capabilities table (including Valkey lacking username customization) and the static role warning for root credentials. Removed the vague claim that static role support varies by database; the page's table lists static roles for every built-in plugin.

Method: documentation only; no commands were run.
