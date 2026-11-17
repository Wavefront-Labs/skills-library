---
id: computing-software.systems-network-administration.proxmox-ve.ct-restore-simple-vs-advanced
name: ct-restore-simple-vs-advanced
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [lxc, pct-restore, vzdump-archive, extractconfig]
level: advanced
status: docs-checked
description: "Restore Proxmox VE container backups with pct restore, and know how simple and advanced restore modes treat mount points."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pct.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Container backups made with vzdump are restored with `pct restore`. By default it restores as much of the backed up configuration as possible, and you can override settings with command line options. To inspect the configuration stored in a vzdump archive, use `pvesm extractconfig`.

There are two restore modes, differing only in how mount points are handled.

Simple mode applies when neither `rootfs` nor any `mpX` parameter is set. This is also what the web interface uses. It:

1. Extracts mount points and their options from the backup.
2. Creates volumes for storage-backed mount points on the storage given by the `storage` parameter (default `local`).
3. Extracts the files from the archive.
4. Adds bind and device mount points to the configuration (limited to the root user).

Bind and device mount points are never backed up, so only their configuration is restored. The assumption is that such data is protected another way, for example NFS space bind mounted into many containers.

Advanced mode is switched on automatically by setting `rootfs` and optionally any `mpX` parameters. It completely ignores the `rootfs` and `mpX` options stored in the archive and uses only those you pass. This lets you pick target storages and volume sizes per mount point, redistribute files across a new mount point layout, or restore to device or bind mount points (root user only).

## Checked

2026-11-09. Compared with the Restoring Container Backups section of https://pve.proxmox.com/pve-docs/chapter-pct.html; simple and advanced mode behaviour matches.

Method: documentation only; no commands were run.

