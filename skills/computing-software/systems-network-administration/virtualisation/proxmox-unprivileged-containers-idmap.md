---
id: computing-software.systems-network-administration.virtualisation.proxmox-unprivileged-containers-idmap
name: proxmox-unprivileged-containers-idmap
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [unprivileged-container, idmap, subuid, subgid, lxc, pct, user-namespaces, file-permissions, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Run unprivileged LXC containers on Proxmox: uid/gid shifting by 100000, custom lxc.idmap to map a host user into a container, subuid/subgid, and converting privileged ones."
sources:
  - https://pve.proxmox.com/wiki/Unprivileged_LXC_containers
  - https://github.com/proxmox/pve-docs/blob/master/pct.adoc
  - https://pve.proxmox.com/pve-docs/pct.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unprivileged containers and ID mapping

**Goal:** containers whose root is not host root, while still sharing files with the host
or other containers with correct ownership.

## How it works
Unprivileged containers use user namespaces: root (UID 0) inside the container is mapped to an unprivileged user outside, usually starting at host UID **100000** (so container UID 0-65535 maps to host 100000-165535). A file owned by container `www-data` (33) is then owned by host UID 100033. Escaping the container lands as an unprivileged host user. The docs describe unprivileged as the default when creating a new container; on the CLI `pct create --unprivileged` defaults to 0, so pass `--unprivileged 1`.

## Map a specific host user into the container
Goal: container UID/GID 1000 = host UID/GID 1000 (to share a bind-mounted directory).
In `/etc/pve/lxc/<id>.conf`:
```
lxc.idmap: u 0 100000 1000
lxc.idmap: g 0 100000 1000
lxc.idmap: u 1000 1000 1
lxc.idmap: g 1000 1000 1
lxc.idmap: u 1001 101001 64535
lxc.idmap: g 1001 101001 64535
```
And allow root to map that ID on the host: add `root:1000:1` to both `/etc/subuid` and
`/etc/subgid`. The ranges must cover 0-65535 exactly once with no overlaps or the container
won't start.

## Simpler alternative
Leave the default map and make the host directory owned by the shifted ID:
`chown -R 101000:101000 /tank/share` (container UID 1000 → host 101000).

## Privileged → unprivileged conversion
Back up with vzdump, then restore with `pct restore <id> <archive> --unprivileged 1`
(add `--ignore-unpack-errors 1` if extraction stops on errors such as device nodes). Check services that relied on host devices.

## Gotchas
- AppArmor prohibits mount system calls in containers; the `mount=` feature allows chosen file system types but can weaken security (an NFS mount can block host I/O), so prefer mounting on the host and bind-mounting in.
- Docker inside an unprivileged container needs `keyctl=1` (and nesting is best used with unprivileged containers with additional id mapping).
- Device passthrough (e.g. `/dev/dri` for transcoding) uses `dev0:` entries with `gid`/`uid`; use the right group IDs.

## Verify
`pct start` succeeds; inside the container `ls -ln` on the shared path shows UID 1000 for
files created on the host by UID 1000; on the host, files created in the container show
the expected UID.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: pct.adoc Unprivileged Containers, AppArmor and Privileged Containers sections; pct.conf.5-opts.adoc features and dev[n]) and the Proxmox VE wiki page Unprivileged LXC containers (last edited 2021; idmap and subuid example). Confirmed that root maps to an unprivileged outside user, usually 100000, that the idmap ranges in the example cover 0-65535 exactly once, and that root:1000:1 style entries are needed in subuid and subgid. Replaced the unconfirmed default claim.

Method: documentation only; no commands were run.
