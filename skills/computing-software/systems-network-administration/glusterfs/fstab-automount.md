---
id: computing-software.systems-network-administration.glusterfs.fstab-automount
name: fstab-automount
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, fstab, netdev, automount, mount]
level: intro
status: docs-checked
description: "Mount a GlusterFS volume automatically at boot with an /etc/fstab line using the glusterfs type and _netdev, plus the supported extra options."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Setting-Up-Clients.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automount in fstab

Native client entry:

```
HOSTNAME-OR-IPADDRESS:/VOLNAME MOUNTDIR glusterfs defaults,_netdev 0 0
server1:/test-volume /mnt/glusterfs glusterfs defaults,_netdev 0 0
```

Supported extra options (add after `_netdev`, comma separated): `log-level`, `log-file`, `transport`, `direct-io-mode`, and `use-readdirp=no`.

NFSv3 entry:

```
server1:/test-volume /mnt/glusterfs nfs defaults,_netdev,vers=3 0 0
```

For TCP, the page uses an entry with `mountproto=tcp` in place of `vers=3`: `server1:/test-volume /mnt/glusterfs nfs defaults,_netdev,mountproto=tcp 0 0`.

For NFS you can also use autofs: update `/etc/auto.master` and `/etc/auto.misc`, then restart the autofs service; directories mount on first access.

Check with `mount` and `df -h MOUNTDIR`. The server named in the entry only supplies the volfile; the client then talks directly to the servers it lists.

## Checked

2026-11-04: the native and NFSv3 fstab entries, the supported extra options, the TCP entry, autofs and the volfile-only note were read against the glusterdocs page Setting-Up-Clients. Replaced the unconfirmed claim that `mountproto=tcp` can sit alongside `vers=3` with the page's own entry.

Method: documentation only; no commands were run.
