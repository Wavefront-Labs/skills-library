---
id: computing-software.systems-network-administration.glusterfs.ganesha-export-volume
name: ganesha-export-volume
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, nfs-ganesha, ganesha, fsal, export]
level: advanced
status: docs-checked
description: "Export a GlusterFS volume with NFS-Ganesha: packages, EXPORT block fields with the GLUSTER FSAL, %include, cache invalidation, D-Bus export and showmount check."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/NFS-Ganesha-GlusterFS-Integration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export a volume with NFS-Ganesha

Packages: Gluster 3.10 or later (`glusterfs-server`, `glusterfs-api`, `glusterfs-ganesha`) and Ganesha 2.5 or later (`nfs-ganesha`, `nfs-ganesha-gluster`).

Start: `service nfs-ganesha start` (config `/etc/ganesha/ganesha.conf`, log `/var/log/ganesha.log`). The export list is empty by default.

Recommended `NFS_Core_Param`: `NSM_Use_Caller_Name = true`, `Clustered = false`, `Rquota_Port = 875`; for Mac clients the page adds `Enable_RQUOTA = false`.

1. Write an `EXPORT` block in an export file with: `Export_Id` (unique), `Path`, `FSAL` (`name = GLUSTER`, `hostname` of one pool node, `volume`), `Access_type`, `Squash`, `Disable_ACL`, `Pseudo`, `Protocols`, `Transports`, `SecType`.
2. Add a `%include` line for that file at the end of `ganesha.conf`. Shortcut: `/usr/libexec/ganesha/create-export-ganesha.sh <ganesha dir> on <volume name>`.
3. Enable cache invalidation:

```
gluster volume set <volume name> features.cache-invalidation on
```

4. Export via D-Bus (`AddExport` on `/org/ganesha/nfsd/ExportMgr`, `RemoveExport` to unexport), or `/usr/libexec/ganesha/dbus-send.sh <ganesha dir> [on|off] <volume name>`.
5. Check with `showmount -e localhost`.

Highly available setup (Pacemaker/Corosync, `ganesha-ha.conf`, `gluster nfs-ganesha enable`) is described on the same page.

## Checked

2026-11-04. Confirmed against the glusterdocs NFS-Ganesha integration page: package versions, start command, default config and log paths, empty default export list, the NFS_Core_Param values, the EXPORT block fields, the %include step, create-export-ganesha.sh, cache-invalidation, the D-Bus AddExport and RemoveExport calls, dbus-send.sh and showmount. Corrected: Enable_RQUOTA is shown as false for Mac clients, not enabled.

Method: documentation only; no commands were run.
