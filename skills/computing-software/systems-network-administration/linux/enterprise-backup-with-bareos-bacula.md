---
id: computing-software.systems-network-administration.linux.enterprise-backup-with-bareos-bacula
name: enterprise-backup-with-bareos-bacula
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, bareos, bacula, bconsole, backup-director, file-daemon, storage-daemon]
level: practitioner
status: draft
description: "Run Bareos or Bacula enterprise backups: director, storage and file daemons, jobs, filesets, schedules, pools and retention, restores from bconsole, and common failures."
sources:
  - https://docs.bareos.org/
  - https://docs.bareos.org/TasksAndConcepts/TheRestoreCommand.html
  - https://www.bacula.org/documentation/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Enterprise backup with Bareos/Bacula

Bareos is a fork of Bacula with the same architecture and config language:
- **Director** (bareos-dir): schedules jobs, holds the catalog (PostgreSQL).
- **Storage daemon** (bareos-sd): writes volumes to disk, tape or S3 (droplet backend).
- **File daemon** (bareos-fd): on each client, reads/restores files.
- **bconsole** / Bareos WebUI: operator interface.

## Config layout (Bareos)
`/etc/bareos/bareos-dir.d/{client,job,jobdefs,fileset,schedule,pool,storage}/*.conf` - one resource per file.
```
# client/web1.conf
Client { Name = web1-fd  Address = web1.example.com  Password = "..." }
# fileset/linux-server.conf
FileSet { Name = "LinuxServer"
  Include { Options { Signature = XXH128  Compression = LZ4  One FS = No }
            File = /etc  File = /srv  File = /var/lib/pgsql/backups }
  Exclude { File = /proc  File = /sys  File = /tmp } }
# job/web1.conf
Job { Name = "backup-web1"  JobDefs = "DefaultJob"  Client = web1-fd  FileSet = "LinuxServer" }
# schedule
Schedule { Name = "WeeklyCycle"
  Run = Full 1st sat at 21:00
  Run = Differential 2nd-5th sat at 21:00
  Run = Incremental mon-fri at 21:00 }
# pool
Pool { Name = Full  Pool Type = Backup  Volume Retention = 365 days  Maximum Volume Bytes = 50G
       Label Format = "Full-"  Auto Prune = yes  Recycle = yes }
```
Client side: `/etc/bareos/bareos-fd.d/director/bareos-dir.conf` must hold the matching password. Port 9102 (fd), 9103 (sd), 9101 (dir). Use TLS-PSK (default in Bareos) or certificates.

## Operating with bconsole
```
reload                         # after config changes (test first: bareos-dir -t)
status dir                     # running and scheduled jobs
status client=web1-fd          # connectivity check
run job=backup-web1 level=Full yes
messages                       # job reports
list jobs client=web1-fd
list volumes pool=Full
```

## Restore
```
restore client=web1-fd select current          # build tree from the catalog
  cd /etc/nginx; mark nginx.conf; done
  # modify: Where=/tmp/bareos-restores (default) or restore to another client
restore client=web1-fd restoreclient=web2-fd fileset=LinuxServer before="2026-10-10 00:00:00"
```
Database dumps are best taken by a `ClientRunBeforeJob = "/usr/local/bin/pg-dump.sh"` script, then backing up the dump; or use Bareos plugins (PostgreSQL, MariaDB, VMware).

## Retention rules that surprise people
- Three retentions: File (catalog file records), Job, Volume. Pruning happens only when volumes are needed or on `prune`.
- An incremental is useless once its Full is recycled; Full retention must exceed the cycle length.
- Catalog backup job (`BackupCatalog`) must run after nightly jobs, and the bootstrap file should be copied off-host.

## Common failures
| Message | Fix |
|---|---|
| `Authorization key rejected by File Daemon` | password/name mismatch between dir and fd configs |
| `Waiting for a mount request` / `Cannot find any appendable volumes` | pool full: add volumes, check retention, `Maximum Volumes` |
| `Fatal error: Network error with FD during Backup` | firewall or idle timeouts; set `Heartbeat Interval = 60` |

## Verify
- [ ] Weekly test restore of a random file to a scratch location succeeds and checksums match.
- [ ] Catalog backup and bootstrap files exist off the backup server.
