---
id: computing-software.networking-hardware-and-wireless.kea.kea-admin-database-tool
name: kea-admin-database-tool
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-admin, db-init, db-upgrade, lease-dump, mysql, pgsql]
level: practitioner
status: docs-checked
description: "Initialize, version-check and upgrade Kea lease databases with kea-admin, and dump or upload CSV leases."
sources:
  - https://kea.readthedocs.io/en/latest/arm/admin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kea-admin database tool
Commands: `db-init`, `db-version`, `db-upgrade`, `lease-dump` and `lease-upload`. Backends: `memfile`, `mysql`, `pgsql`.

```
kea-admin db-version mysql
```

- `lease-dump` writes leases as CSV with a header line.
- `lease-upload` loads a memfile-format CSV into the backend.

Database notes from the docs: MariaDB is recommended over MySQL 8, which showed a 60-90% speed drop versus 5.7. The database needs JSON support, and the system timezone should be UTC.

## Checked

2026-11-08. Read the Kea Database Administration chapter in full: the five kea-admin commands, the three backends, lease-dump and lease-upload CSV behaviour, the MySQL 8 versus MariaDB note (60-90% drop versus 5.7), JSON support and the UTC timezone recommendation. Description reworded because lease-dump reads from a database backend. Nothing else removed.

Method: documentation only; no commands were run.
