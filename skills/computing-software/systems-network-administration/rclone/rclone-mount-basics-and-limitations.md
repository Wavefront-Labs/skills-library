---
id: computing-software.systems-network-administration.rclone.rclone-mount-basics-and-limitations
name: rclone-mount-basics-and-limitations
category: computing-software
field: systems-network-administration
product: rclone
tags: [mount, fuse, fusermount, daemon, systemd, mount-helper]
level: practitioner
status: draft
description: "Mount a remote with rclone mount on Linux, macOS or Windows, stop it, run it under systemd and understand its limits."
sources: ["https://rclone.org/commands/rclone_mount/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
`rclone mount remote:path /path/to/mountpoint` mounts a remote as a FUSE filesystem on Linux, FreeBSD, macOS and Windows. The mountpoint must be an existing empty directory on Unix. It runs in the foreground by default and stops on Ctrl-C, SIGINT or SIGTERM; `--daemon` backgrounds it on Unix and then you unmount manually with `fusermount -u` (or `fusermount3 -u`). With `--daemon`, the parent waits up to `--daemon-wait` for the mount to appear. On Windows the mount is foreground only and the target can be `*` (auto drive), a drive letter such as `X:`, a path, or a network share.

## Limitations

Without `--vfs-cache-mode`, files can only be written sequentially and reads can only seek, so many applications fail; use `writes` or `full`. Bucket-based remotes (Azure Blob, Swift, S3, GCS, B2) cannot store empty directories, and only Azure Blob, GCS and S3 can keep them with `--xxx-directory_markers`. Filesystems expect reliability that cloud storage lacks; unlike sync and copy, mount cannot retry without local copies of uploads, which VFS caching provides.

## systemd

The service can use `Type=notify`, entering started state after the mount is ready. systemd gives no `PATH` or `HOME`, so tilde expansion fails: pass `--config` and `--cache-dir` as absolute paths. The fallback `PATH` is `/bin:/usr/bin`, which must contain `fusermount` or `fusermount3`.

## Mount helper

Symlink the binary to `/sbin/mount.rclone` (optionally `rclonefs`) and rclone translates mount options, so you can use `mount sftp1:subdir /mnt/data -t rclone -o vfs_cache_mode=writes` or a systemd `.mount` unit with `Type=rclone`, `What=sftp1:subdir` and `Options=rw,_netdev,allow_other,args2env,vfs-cache-mode=writes,config=/etc/rclone.conf,cache-dir=/var/rclone`.

On Linux, if AppArmor blocks `fusermount3` you may see "Permission denied". On macOS an NFS mount without a cache mode is read-only.
