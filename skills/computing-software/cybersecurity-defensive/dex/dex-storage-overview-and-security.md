---
id: computing-software.cybersecurity-defensive.dex.dex-storage-overview-and-security
name: dex-storage-overview-and-security
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [storage, security, migrations, persistence]
level: practitioner
status: docs-checked
description: "Pick a Dex storage backend and protect it: state, signing keys and bcrypt hashes live there, and SQL migrations run automatically."
sources:
  - https://dexidp.io/docs/configuration/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dex persists state to track refresh tokens, prevent replays and rotate keys. The storage page lists these backends: etcd v3, Kubernetes custom resource definitions, and SQL (SQLite3, Postgres, MySQL).

Select one with the top-level `storage` block:

```yaml
storage:
  type: postgres
  config:
    host: db.example.com
```

Security: storage breaches are serious. Dex saves sensitive data in the backing store, including signing keys and bcrypt'd passwords, so use both transport security and database ACLs whatever backend you choose.

SQL specifics:

- Migrations run automatically on the first connection to the SQL server and cannot be rolled back.
- Dex therefore needs privileges to add and alter tables in its database.
- Table names are not configurable, so give Dex its own database to avoid clashes.
- Older Dex versions encrypted some values with symmetric keys before writing to the database; this has not been ported to v2 and may have no migration path if added later.

Choosing: SQLite3 is the quick start, not for real workloads. Kubernetes CRDs avoid an external database inside a cluster, though the docs say they may not suit a large number of users. Installations outside Kubernetes would likely prefer another option.

Gotcha: new storage types need a strong use case, because each implementation has a large ongoing maintenance cost.

## Checked

2026-11-08: Read the Dex Storage page in full. Confirmed the persistence purposes, the backend list, the sensitive-data warning, SQL migrations and privileges, fixed table names, the unported symmetric-key note and the maintenance-cost note. Reworded the backend guidance to match the page.
Method: documentation only; no commands were run.
