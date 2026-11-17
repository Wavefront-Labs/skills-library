---
id: computing-software.database-administration.pgbackrest.dedicated-repository-host-ssh
name: dedicated-repository-host-ssh
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, repository-host, ssh, repo-host, remote]
level: advanced
status: docs-checked
description: "Set up a dedicated repository host reached over passwordless SSH, with pg-host on the repo host and repo-host on database hosts."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: separate backups from the database server.

Layout:

- Database host: `pg1-path` is the local cluster, no `pg1-host`; set `repo1-host` to the repository host.
- Repository host: `pg1-host`, `pg1-path` (and `pg2-...` for a standby) for each database host. The database hosts can be configured in any order.

```
# repository
[demo]
pg1-host=pg-primary
pg1-path=/path/to/pgdata
[global]
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
```

```
# database host
[demo]
pg1-path=/path/to/pgdata
[global]
repo1-host=repository
```

The pgBackRest version on the repository host must exactly match the database hosts. Use a dedicated user such as pgbackrest rather than postgres, with `repo1-host-user` (default pgbackrest) and `pg1-host-user` (default postgres).

SSH keys: create a key pair per host, then add each public key to the other's authorized_keys with a forced command (`command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }"`, as in the guide) so the keys can only run pgBackRest.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html). Removed: the no-agent-forwarding/no-X11-forwarding/no-port-forwarding restriction string and the --reset-pg1-host remark, which are not on the fetched pages. 

Method: documentation only; no commands were run.
