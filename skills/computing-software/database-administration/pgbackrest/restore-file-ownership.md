---
id: computing-software.database-administration.pgbackrest.restore-file-ownership
name: restore-file-ownership
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, restore, ownership, root, manifest]
level: advanced
status: docs-checked
description: "How restore assigns file ownership when run as root or as a normal user."
sources:
  - https://pgbackrest.org/user-guide.html
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid ownership surprises after restore.

Non-root (typical): all restored files belong to the user and group running pgBackRest. If existing files are not owned by that user and group, an error results when ownership cannot be updated. A privileged user must fix ownership before retrying.

Root: pgBackRest tries to recreate the ownership recorded in the manifest at backup time. Only user and group names are stored, so the same names must exist on the restore host. Fallbacks: if the name is not found locally, the user and group of the PostgreSQL data directory is used, and finally root if that directory's owner cannot be mapped to a name.

`restore` is the only command allowed to run as root by default (`allow-root=n` blocks the others), because it manages ownership carefully. Other commands as root can create root-owned files in the repository that later commands cannot use.

```
sudo -u postgres pgbackrest --stanza=demo --delta restore
```

Running as the cluster owner is the usual choice; the docs say it is far better to run pgBackRest as the user that owns the repository and PostgreSQL cluster.

## Checked

2026-11-08: non-root and root ownership behaviour confirmed in the User Guide restore File Ownership section; allow-root default and the restore-only exception confirmed in the Configuration page. Partial reads: the User Guide, Command Reference and Configuration pages are long, so only the sections relevant to this skill were read, not every page end to end.

Method: documentation only; no commands were run.
