---
id: computing-software.systems-network-administration.virtualisation.proxmox-lxc-raw-config-and-device-passthrough
name: proxmox-lxc-raw-config-and-device-passthrough
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [lxc-raw-config, lxc-device-passthrough, lxc, proxmox]
level: advanced
status: docs-checked
description: "Add raw lxc.* keys and device passthrough to Proxmox VE containers for GPUs, /dev/net/tun and USB serial devices, in privileged and unprivileged modes."
sources:
  - https://pve.proxmox.com/pve-docs/pct.conf.5.html
  - https://github.com/lxc/lxc/blob/main/doc/lxc.container.conf.sgml.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raw lxc config keys and device passthrough

**Goal:** give a container access to host devices (render GPU, TUN, serial adapters) that the GUI options do not cover.

## Built-in device passthrough
```bash
pct set 210 -dev0 /dev/dri/renderD128,gid=104     # gid of 'render' inside the CT
pct set 210 -dev1 /dev/ttyUSB0,mode=0660,uid=0,gid=20
```
The `devN` option takes `path`, `uid`, `gid`, `mode` and `deny-write`; uid, gid and mode set the ownership and access mode of the device node in the container. Prefer it to raw keys where it covers your case.

## Raw keys
Lines beginning `lxc.` in `/etc/pve/lxc/<id>.conf` are passed to LXC as native options (edit with the CT stopped):
```
# GPU for transcoding
lxc.cgroup2.devices.allow: c 226:* rwm
lxc.mount.entry: /dev/dri dev/dri none bind,optional,create=dir
# TUN for VPN clients
lxc.cgroup2.devices.allow: c 10:200 rwm
lxc.mount.entry: /dev/net/tun dev/net/tun none bind,create=file
```
Find major:minor numbers with `ls -l /dev/dri /dev/net/tun`.

## Unprivileged containers
The device node appears owned by `nobody` because host uid/gid are outside the CT's map. Fix by: using `devX` with `uid`/`gid`; or `lxc.idmap` entries mapping the host group (and allowing it in `/etc/subgid`); or host udev rules that set group ownership to the mapped id (the host-side id is the container gid plus the start of the idmap range, usually 100000).

## Gotchas
- A wrong raw key can stop the CT from starting; check `pct start 210 --debug`.
- Use the cgroup v2 prefix `lxc.cgroup2.*`: cgroup v1 was deprecated in Proxmox VE 7.0 and removed entirely in 9.0, so old `lxc.cgroup.*` lines from guides do not apply.
- A running container cannot be live-migrated; a restart migration needs the device to exist on the target node.
- Device passthrough and AppArmor or cgroup overrides widen the attack surface; prefer unprivileged containers.

## Verify
Inside the CT, `ls -l /dev/dri` shows the device with the expected group, and the application (for example `vainfo`) can open it.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: pct.conf.5-opts.adoc dev[n] option, pct.adoc cgroup section) plus the LXC lxc.container.conf documentation (github.com/lxc/lxc doc) and confirmed the dev[n] sub-options, the lxc.cgroup2.devices.allow and lxc.mount.entry (optional, create=dir, create=file) syntax, and the cgroup v1 removal in Proxmox VE 9.0. Removed the unconfirmed PVE 8.1 gate.

Method: documentation only; no commands were run.
