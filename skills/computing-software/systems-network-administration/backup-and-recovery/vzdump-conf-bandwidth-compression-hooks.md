---
id: computing-software.systems-network-administration.backup-and-recovery.vzdump-conf-bandwidth-compression-hooks
name: vzdump-conf-bandwidth-compression-hooks
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [vzdump-conf, vzdump-hook, vzdump, vzdump-mode, proxmox-backup-server, proxmox]
level: practitioner
status: docs-checked
description: "Tune Proxmox vzdump with /etc/vzdump.conf and job options: bwlimit, zstd and pigz threads, ionice, tmpdir, max-workers, retention, protection and the --script hook."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-vzdump.html
  - https://pve.proxmox.com/pve-docs/vzdump.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vzdump.conf, bandwidth, compression and hooks

## Configuration file
Global configuration is stored in `/etc/vzdump.conf`: one `OPTION: value` per line, blank lines ignored, `#` lines are comments. Values are defaults and can be overwritten on the command line. Backup jobs (created in the UI under Datacenter, Backup, or via the `/cluster/backup` API) generate entries in `/etc/pve/jobs.cfg`, run by the `pvescheduler` daemon. The manual's example:
```
tmpdir: /mnt/fast_local_disk
storage: my_backup_storage
mode: snapshot
bwlimit: 10000
```

## Performance options (from the option list)
| Option | Meaning and default |
|---|---|
| `bwlimit` | I/O bandwidth limit in KiB/s (default 0) |
| `ionice` | 0 to 8, default 7; used with the BFQ scheduler. For VM snapshot and suspend backups it affects only the compressor; 8 means idle priority |
| `zstd` | zstd threads, default 1; 0 uses half the available cores |
| `pigz` | use pigz instead of gzip when N>0; 1 uses half the cores, N>1 uses N threads (default 0) |
| `performance` | `max-workers` (VMs, 1 to 256, default 16) and `pbs-entries-max` (container backups sent to PBS, default 1048576; raise it for containers with very many files) |
| `tmpdir` | directory for temporary files |
| `lockwait` | minutes to wait for the global lock (default 180) |
| `stopwait` | minutes to wait for a guest to stop (default 10) |
| `mode` | `snapshot` (default), `stop` or `suspend` |
| `script` | hook script |
The manual recommends `--tmpdir` on a local file system when a container is on local storage and the backup target is NFS/CIFS (many-fold performance gain).

## Compression
Options are lzo, gzip and zstd. zstd is currently the fastest and is multi-threaded; lzo and gzip are more widely installed. pigz can replace gzip for multi-threading. File extensions show the algorithm: `.zst`, `.gz` or `.tgz`, `.lzo`; a name without one was not compressed by vzdump. The `compress` option takes 0, 1, gzip, lzo or zstd (default 0).

## Retention and protection
`prune-backups` takes `keep-last`, `keep-hourly`, `keep-daily`, `keep-weekly`, `keep-monthly`, `keep-yearly` (or `keep-all`, which conflicts with the others), processed in that order, each covering only backups older than those already kept:
```
vzdump 777 --prune-backups keep-last=3,keep-daily=13,keep-yearly=9
```
The manual advises configuring it at storage level when possible. A backup can be marked protected: pruning ignores protected backups and they do not count toward retention, but protection is enforced by Proxmox VE, not the file system, so anyone with write access to the storage can still delete the file. Storage option `max-protected-backups` limits protected backups per guest (-1 unlimited; default unlimited with Datastore.Allocate, 5 otherwise).

## Hook script
`--script` (or `script:` in the config) names a hook script called at various phases of the backup with parameters set accordingly. The manual points to an example in the documentation directory, `vzdump-hook-script.pl`. The phase names, parameters and environment variables are not listed on the pages read; take them from that example file.

## Related
Fleecing: see `proxmox-backup-fleecing`.

## Checked
2026-11-07. Read in full: the PVE Backup and Restore chapter (9.2.13) from Backup Modes through Configuration, Hook Scripts, File Exclusions and Examples (lines 1-330 of the fetched text). The vzdump.1 page was not re-read; it carries the same option list. Removed because the pages do not state them: the `bwlimit: 204800` and `ionice: 7` example values as recommendations, "zstd is the default for file targets", "PBS ignores compression", "PVE 8.1+" version claims, the hook phase list, the `$TARGET`/`$STOREID` variables and "non-zero exit aborts", the hook examples with curl and logger, the multi-node and root-hook gotchas, "restore bwlimit datacenter option" form (the page shows `pvesm set STORAGEID --bwlimit restore=KIBs`) and the invented Verify step.
Method: documentation only; no commands were run.
