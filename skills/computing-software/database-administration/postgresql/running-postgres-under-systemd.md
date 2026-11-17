---
id: computing-software.database-administration.postgresql.running-postgres-under-systemd
name: running-postgres-under-systemd
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgres-systemd, systemd-unit-postgres, systemd, pg-ctlcluster, postgres-server-setup, service-management, drop-in]
level: practitioner
status: docs-checked
description: "Run and customise PostgreSQL as a systemd service on Debian and RHEL layouts: unit names, drop-in overrides, timeouts, multiple clusters and boot ordering."
sources:
  - https://www.postgresql.org/docs/current/server-start.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostgreSQL under systemd

**Goal:** the service starts on boot, stops cleanly, and local tweaks survive package upgrades.

## Unit names
Unit names and data directories depend on the packaging; list them with `systemctl list-units 'postgresql*'`. The examples below use `postgresql-17` as a placeholder.

## Override with a drop-in, never edit the vendor unit
```bash
systemctl edit postgresql-17
```
```ini
[Service]
Environment=PGDATA=/data/pg17
TimeoutStopSec=600          # a long shutdown checkpoint must not be SIGKILLed
OOMScoreAdjust=<value>      # see systemd.exec for the range
```
`systemctl daemon-reload && systemctl restart postgresql-17`. A drop-in is separate from the vendor unit, so package upgrades do not overwrite it.


## Gotchas
- Two clusters on one host need distinct ports (`port` in each postgresql.conf).
- RemoveIPC: `RemoveIPC` in logind.conf controls whether IPC objects are removed when a user fully logs out; system users are exempt, and the default is on in stock systemd (some distributions default it off). If the postgres account is not a system user, set `RemoveIPC=no` (see the PostgreSQL kernel resources chapter).

## Verify
- `systemctl is-enabled postgresql-17` = enabled; `systemctl status` shows active.
- `systemctl show postgresql-17 -p TimeoutStopUSec` reflects the drop-in.
- Reboot test: server is accepting connections (`pg_isready`) after boot.

## Checked

2026-10-28. Confirmed against PostgreSQL docs (version 18) kernel resources chapter (systemd RemoveIPC, system users exempt, logind.conf) and the systemd.service man page (TimeoutStopSec, OOMScoreAdjust). Removed unconfirmed: Debian and RPM unit names and paths, LimitNOFILE, RequiresMountsFor and network-online ordering, drop-in file path, reload mapping, Debian port assignment, pg_ctl-vs-systemd note.

Method: documentation only; no commands were run.
