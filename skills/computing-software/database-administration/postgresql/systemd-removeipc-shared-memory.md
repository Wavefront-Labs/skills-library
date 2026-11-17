---
id: computing-software.database-administration.postgresql.systemd-removeipc-shared-memory
name: systemd-removeipc-shared-memory
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres-server-setup, removeipc, systemd, logind, shared-memory, semaphores, kernel-resources]
level: practitioner
status: docs-checked
description: "Stop systemd-logind RemoveIPC from deleting PostgreSQL semaphores and shared memory when the postgres user logs out, which crashes the server at random."
sources:
  - https://www.postgresql.org/docs/current/kernel-resources.html#SYSTEMD-REMOVEIPC
  - https://www.freedesktop.org/software/systemd/man/latest/logind.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# systemd RemoveIPC and PostgreSQL

## Symptom
The server dies or refuses connections shortly after someone ran `sudo -iu postgres`
(or an ssh/cron session as `postgres`) and logged out. Logs show:
```
FATAL:  semctl(...) failed: Invalid argument
LOG:  server process (PID ...) was terminated by signal 6
```

## Cause
`systemd-logind` with `RemoveIPC=yes` deletes all System V IPC objects and POSIX shared
memory owned by a user when that user's **last session** ends. It skips "system users"
(UID below `SYS_UID_MAX`, normally < 1000). If `postgres` was created as a normal user
(UID >= 1000, common with hand-made accounts, LDAP or some container images), its
semaphores vanish under the running server. RemoveIPC defaults to yes in stock systemd; some distributions default it to off (PostgreSQL docs).

## Fix (do one)
1. Turn it off globally:
   ```ini
   # /etc/systemd/logind.conf
   [Login]
   RemoveIPC=no
   ```
   ```bash
   systemctl restart systemd-logind
   ```
2. Or make the service account a system user: create it with `useradd --system` so the UID
   falls under `SYS_UID_MAX` (check `/etc/login.defs`). Re-owning an existing install to a
   new UID means `chown -R` of PGDATA and tablespaces during downtime.

This mostly bites hand-made accounts, LDAP users and custom images.

## Check exposure
```bash
id -u postgres                      # >= 1000 means exposed if RemoveIPC=yes
grep -i '^SYS_UID_MAX' /etc/login.defs
loginctl show-user postgres 2>/dev/null | grep -i linger
systemd-analyze cat-config systemd/logind.conf | grep -i removeipc
```
Fix it with RemoveIPC=no or a system UID.

## Verify
Log in and out as `postgres` twice, then run `ipcs -s` and `psql -c 'select 1'`: the
semaphore sets owned by postgres are still present and the server answers.

## Checked

2026-10-28. Confirmed against the PostgreSQL kernel resources page (systemd RemoveIPC: system users exempt, system user determined by SYS_UID_MAX in /etc/login.defs, RemoveIPC=no) and the logind.conf man page (RemoveIPC defaults to yes, root and system users excluded). Corrected: many distributions do not ship it on; PostgreSQL docs say some default it to off. Removed: package-install and lingering claims (not in the sources).

Method: documentation only; no commands were run.
