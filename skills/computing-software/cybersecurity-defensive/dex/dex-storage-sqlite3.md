---
id: computing-software.cybersecurity-defensive.dex.dex-storage-sqlite3
name: dex-storage-sqlite3
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [sqlite3, storage, development, file-lock]
level: intro
status: docs-checked
description: "Use Dex sqlite3 storage for quick starts with the file option, and avoid it for real workloads."
sources:
  - https://dexidp.io/docs/configuration/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SQLite3 is the recommended storage for people who want to stand up Dex quickly. The docs state it is not appropriate for real workloads.

The configuration takes a single argument, the database file:

```yaml
storage:
  type: sqlite3
  config:
    file: /var/dex/dex.db
```

Behaviour to know:

- SQLite3 uses file locks to prevent race conditions. If you provide the value `:memory:`, Dex automatically disables support for concurrent database queries.
- As with all SQL backends, migrations run on first connection and cannot be rolled back.
- Dex saves sensitive data in its backing storage, including signing keys and bcrypt'd passwords, so protect the database file with access controls whichever storage you use.
- Dex persists state to track refresh tokens, prevent replays and rotate keys; an in-memory database does not outlive the process.

Gotcha: for anything beyond a quick start choose one of the other supported storages (Postgres, MySQL, etcd or Kubernetes CRDs).

## Checked

2026-11-08. Read in full: the Dex Storage documentation page (SQL and SQLite3 sections). Confirmed: quick-start recommendation, not for real workloads, the file option, file locks and `:memory:` behaviour, non-reversible automatic migrations, sensitive data warning, what state Dex persists. Removed: the claims about the token exchange and GitHub Actions examples and `examples/config-dev.yaml` (not on this page).

Method: documentation only; no commands were run.
