---
id: computing-software.systems-network-administration.proxmox-ve.ct-migrate-restart-mode
name: ct-migrate-restart-mode
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [lxc, pct-migrate, restart-migration, offline-migration]
level: practitioner
status: docs-checked
description: "Migrate Proxmox VE containers between cluster nodes with pct migrate, using restart migration because containers cannot live migrate."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pct.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In a cluster, migrate a container with:

```
pct migrate <ctid> <target>
```

This works while the container is offline. If it has local volumes or mount points, their content is copied over the network to the target node, provided the same storage is defined there.

Running containers cannot be live migrated because of technical limitations. Instead use a restart migration, available in the web interface or with the `--restart` flag:

```
pct migrate <ctid> <target> --restart
```

A restart migration shuts the container down, killing it after a timeout (default 180 seconds), migrates it like an offline migration, and then starts it on the target node. Because containers are lightweight the downtime is normally only some hundreds of milliseconds.

Container configuration lives in `/etc/pve/lxc/<CTID>.conf`, which is replicated to all nodes automatically. CTIDs must be unique cluster wide.

Related behaviour to remember:

- Bind and device mount points are not storage managed or backed up, so handle their data separately.
- Replication of container volumes requires zfspool storage.
- The restart timeout can be changed from the 180 second default.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-pct.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
