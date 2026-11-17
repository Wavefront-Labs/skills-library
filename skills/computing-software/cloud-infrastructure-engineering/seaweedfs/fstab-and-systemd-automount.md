---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.fstab-and-systemd-automount
name: fstab-and-systemd-automount
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [fuse-weed, x-systemd-automount, mount-weed, fstab, automount]
level: practitioner
status: docs-checked
description: "Mount SeaweedFS at boot via /etc/fstab (fuse.weed) and use systemd automount options for on-demand mounts, with single or multiple filers."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/fstab-and-systemd-mount
  - https://github.com/seaweedfs/seaweedfs/wiki/FUSE-Mount
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# fstab and systemd automount

Prereq: install `weed` as the mount helper (`cp weed /sbin/mount.weed`) and put `security.toml` where weed reads it.

Single filer:
```
fuse /path/to/mountpoint fuse.weed filer=localhost:8888,filer.path=/,defaults,_netdev 0 0
```
Multiple filers (quote the list):
```
fuse /path/to/mountpoint fuse.weed filer='192.168.0.1:8888,192.168.0.2:8888',filer.path=/,defaults,_netdev 0 0
```
`systemd-fstab-generator` turns fstab lines into mount units automatically on modern systems.

On-demand mount of a root-owned mountpoint:
```
fuse /path/to/mountpoint fuse.weed filer='ip1:8888,ip2:8888',filer.path=/,x-systemd.automount,x-systemd.idle-timeout=300,autofs,defaults,_netdev 0 0
```
- `x-systemd.automount` enables automount
- `x-systemd.idle-timeout=300` disconnects when idle
- `autofs` makes weed fuse compatible with automount

For user-owned mountpoints see the page for the user-mount options.

If the mount fails, run `weed mount` directly in verbose/debug mode to see why.

Verify: after boot, or after accessing the path to trigger automount, confirm the filesystem is mounted at the mountpoint.

## Checked
Checked 2026-11-09: the mount.weed prerequisite, both fstab lines, the systemd-fstab-generator note, the root-owned automount line with its three added options, and the verbose `weed mount` troubleshooting tip match the fstab-and-systemd-mount page. Reworded the verify step (the grep command was not on the page).
Method: docs-checked 2026-11-09 against the SeaweedFS wiki page fstab-and-systemd-mount, read in full from a local clone of the wiki.
