---
id: computing-software.systems-network-administration.glusterfs.upgrade-online
name: upgrade-online
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, upgrade, rolling-upgrade, online-upgrade, offline-upgrade]
level: advanced
status: docs-checked
description: "Generic GlusterFS upgrade: online rolling upgrade one server at a time for replicate volumes with heal checks, the offline alternative, and post-upgrade and client steps."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Upgrade-Guide/generic-upgrade-procedure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Online rolling upgrade

Only for replicated and distributed-replicate volumes; dispersed and pure distributed volumes need the offline procedure. Upgrade servers before clients; if geo-replication is used, upgrade the secondary cluster first. Make no config changes mid-upgrade.

On each server in turn:

1. Stop services and processes:

```
systemctl stop glusterd
systemctl stop glustereventsd
killall glusterfs glusterfsd glusterd
```

2. Stop gfapi applications on the server (qemu, NFS-Ganesha, Samba).
3. Install the new version; confirm with `gluster --version`.
4. `systemctl start glusterd`, then check `gluster volume status`; start `glustereventsd` if it was enabled.
5. Trigger heal on every volume: `for i in $(gluster volume list); do gluster volume heal $i; done`
6. Check `gluster volume heal <volname> info`; the backlog must be empty (or nothing needs syncing to this server) before moving to the next server.
7. Restart the gfapi applications.

Offline: stop everything on all servers, install, start glusterd everywhere, check status, restart applications. Clients have no access meanwhile.

After: raise the op-version (see op-version), upgrade clients (unmount, install, remount). For replicate volumes consider `gluster volume set <volname> fips-mode-rchecksum on`. From versions before 7.0 with quota ever enabled, restart nodes one at a time; peers may show "Peer rejected" until all are back.

## Checked

2026-11-04: pre-upgrade notes, the stop commands, the ten online steps with the heal loop and heal info check, the offline procedure, op-version and fips-mode-rchecksum post-upgrade steps, the pre-7.0 quota restart note and the client steps were read against the glusterdocs page Upgrade-Guide generic-upgrade-procedure. Nothing removed.

Method: documentation only; no commands were run.
