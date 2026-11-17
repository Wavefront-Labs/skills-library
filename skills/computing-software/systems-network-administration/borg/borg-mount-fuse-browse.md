---
id: computing-software.systems-network-administration.borg.borg-mount-fuse-browse
name: borg-mount-fuse-browse
category: computing-software
field: systems-network-administration
product: borg
tags: [borg, borg-mount, fuse, borgfs, umount, versions, fstab, browse-backups]
level: practitioner
status: docs-checked
description: "Browse Borg backups as a FUSE filesystem with borg mount: whole repo or one archive, versions view, uid and gid options, foreground mode, borgfs fstab, and umount."
sources: ["https://borgbackup.readthedocs.io/en/stable/usage/mount.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Borg mount and umount

```
borg mount /path/to/repo /path/to/mountpoint
borg mount /path/to/repo::root-2016-02-15 /path/to/mountpoint
borg mount -o versions --glob-archives '*-my-home' --last 10 /path/to/repo /path/to/mountpoint
borg mount /path/to/repo /path/to/mountpoint only/that/path
borg umount /path/to/mountpoint
```

Mounting a repository shows one directory per archive, loaded on demand, so entering them can be slow; mount a single archive or paths to speed it up. Without `--foreground` the process daemonizes (output goes to /dev/null; use `-f` or `BORG_LOGGING_CONF` to debug) and keeps running until unmounted. It does not unmount on signals or crashes. In the foreground, Ctrl+C unmounts cleanly.

Mount options via `-o`: `versions` (merged per-file view across archives; experimental), `allow_damaged_files` (read files patched by `check --repair`, otherwise EIO), `ignore_permissions`, `uid=`/`gid=` overrides. `--numeric-ids` skips name-to-ID mapping. Also `--consider-checkpoints`, archive filters and include/exclude patterns. `BORG_MOUNT_DATA_CACHE_ENTRIES` tunes the chunk cache (default CPU cores).

Caveats: FUSE restores do not support special flags or ACLs. Symlinks are stored as-is and can resolve outside the mountpoint to live host data; on Linux remount with `nosymfollow` or use a container/chroot.

fstab via borgfs: `/path/to/repo /path/to/mnt fuse.borgfs defaults,noauto 0 0`.

## Checked

2026-11-03. Confirmed against the Borg 1.4.5 documentation (usage/mount): mount options, foreground/daemon behaviour, symlink caveat, borgfs fstab line, BORG_MOUNT_DATA_CACHE_ENTRIES. Removed: nothing.

Method: documentation only; no commands were run.
