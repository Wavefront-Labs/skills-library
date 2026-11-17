---
id: computing-software.systems-network-administration.proxmox-ve.ct-mount-points-and-bind-mounts
name: ct-mount-points-and-bind-mounts
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [lxc, mount-point, bind-mount, mp0]
level: practitioner
status: docs-checked
description: "Add storage-backed, bind and device mount points to Proxmox VE containers and understand their backup and snapshot limits."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pct.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A container can have several mount points, so each application can sit on the best suited storage, for example a cheap root file system and a fast distributed volume for a database. Storage-backed volumes use the `mpX` options, and a size-allocating example from the docs is:

```
pct set 100 -mp0 thin1:10,mp=/path
```

Bind mounts expose a host directory with practically zero overhead and can share data between containers:

```
pct set 100 -mp0 /mnt/bindmounts/shared,mp=/shared
```

Rules for bind mounts:

- Use a directory reserved for the purpose, such as a tree under `/mnt/bindmounts`. Never bind mount system directories like `/`, `/var` or `/etc`.
- The source path must not contain symlinks.
- They are not managed by the storage subsystem, so no snapshots or quotas from inside, and their contents are not backed up by vzdump.
- With unprivileged containers, the user mapping can cause permission problems and ACLs cannot be used.

Device mount points mount a host block device directly into the container.

To include a storage-backed mount point in backups, set `backup=1` on it:

```
mp0: guests:subvol-100-disk-1,mp=/root/files,size=8G,backup=1
```

Replication copies extra mount points with the root disk by default. Replication needs a zfspool storage, so a mount point on another storage type requires the Skip replication option.

## Checked

2026-11-09. Compared with the Container Storage, Bind Mount Points, Device Mount Points and Backup sections of https://pve.proxmox.com/pve-docs/chapter-pct.html; the command lines and the replication note match.

Method: documentation only; no commands were run.

