---
id: computing-software.systems-network-administration.backup-and-recovery.pbs-host-file-backup-client
name: pbs-host-file-backup-client
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [pbs-host-backup, proxmox-backup-client, proxmox-backup-server, pxar, linux-backup, pbs]
level: practitioner
status: docs-checked
description: "Back up Linux hosts (including PVE nodes) to Proxmox Backup Server with proxmox-backup-client: pxar archives, excludes, image backups, scheduling, restore and mount."
sources:
  - https://pbs.proxmox.com/docs/backup-client.html
  - https://pbs.proxmox.com/docs/command-syntax.html#proxmox-backup-client
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Host file backup with proxmox-backup-client

**Goal:** file-level backups of physical Linux servers and PVE host configs into PBS with dedup and encryption.

## Environment
```sh
export PBS_REPOSITORY='hostbackup@pbs!web01@pbs1.example.net:store1'
export PBS_PASSWORD='<token secret>'
export PBS_FINGERPRINT='aa:bb:...'
```

## Back up
```sh
proxmox-backup-client backup root.pxar:/ etc.pxar:/etc --include-dev /boot --exclude /var/cache \
  --backup-id web01 --keyfile /root/pbs-enc.key
proxmox-backup-client backup disk.img:/dev/vg0/data       # block image of a device
```
- One `.pxar` per archive name; the client does **not** cross mount points unless `--include-dev` lists them.
- `.pxarexclude` files in directories (gitignore-style) or `--exclude` patterns.
- `--change-detection-mode metadata` skips re-reading unchanged files using previous metadata; big speedup for large file trees.
- Run from a systemd timer; exit code non-zero on failure.

## PVE nodes
Back up `/etc/pve` (the pmxcfs mount), `/etc/network/interfaces`, `/etc/corosync`, `/var/lib/pve-cluster/config.db` with a node-specific `--backup-id`.

## Browse and restore
```sh
proxmox-backup-client snapshot list
proxmox-backup-client catalog shell host/web01/2026-10-17T02:00:00Z root.pxar   # find, select, restore-selected
proxmox-backup-client restore host/web01/2026-10-17T02:00:00Z etc.pxar /tmp/etc-restore
proxmox-backup-client mount host/web01/2026-10-17T02:00:00Z root.pxar /mnt/r     # FUSE
```

## Gotchas
- Databases need a dump or snapshot first; pxar copies files as they are.
- The token needs DatastoreBackup on the datastore/namespace; it then owns its groups.
- Lose the keyfile and encrypted host backups are gone; store a paperkey.

## Verify
`proxmox-backup-client snapshot list` shows daily snapshots, and a catalog-shell restore of a known file matches its checksum.

## Checked

2026-10-28

Confirmed: PBS backup client docs and command syntax: --include-dev, .pxarexclude, --change-detection-mode metadata, --backup-id, catalog shell, mount, restore.

Removed or corrected: the PBS 3.2 version gate.

Method: documentation only; no commands were run.
