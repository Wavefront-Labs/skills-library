---
id: computing-software.systems-network-administration.jellyfin.network-storage-and-nfs
name: network-storage-and-nfs
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, storage, nfs, samba, dotnet-file-locking, nolock]
level: practitioner
status: docs-checked
description: "Mount network media into the OS, keep the Jellyfin database local, and fix slow playback start on NFSv3 caused by file locking."
sources: ["https://jellyfin.org/docs/general/administration/storage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Network storage and NFS

Jellyfin reads media straight from the filesystem. A Samba or NFS share must be mounted into the operating system; Jellyfin does not talk to network storage itself. Keep the Jellyfin database on local storage, not on a network device.

**Caution:** scheduled maintenance tasks remove items from your library if they run while media storage is unavailable.

**Slow start on NFSv3.** If files take a long time to begin playing over NFSv3, the cause can be .NET file locking without NFSv3 locking enabled. The docs list four fixes:

- Disable .NET locking with the `DOTNET_SYSTEM_IO_DISABLEFILELOCKING` environment variable (introduced in .NET 6).
- Mount with the `nolock` option.
- Enable the lock service.
- Use NFSv4, which has built-in lock support.

## Checked

2026-11-03. Confirmed against the Jellyfin Storage page: mount into the OS, local database, maintenance-task caution, NFSv3 locking and its four fixes. Removed: systemd advice, an unsupported recommendation and the invented check.

Method: documentation only; no commands were run.
