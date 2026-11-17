---
id: computing-software.systems-network-administration.virtualisation.proxmox-container-features-nesting
name: proxmox-container-features-nesting
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [lxc-nesting, lxc-features, keyctl, fuse, mknod, apparmor-profile, lxc, pct, docker-in-lxc, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Set Proxmox container features (nesting, keyctl, fuse, mknod, mount types) for systemd, Docker or FUSE workloads, with their security trade-offs and raw lxc.* overrides."
sources:
  - https://pve.proxmox.com/pve-docs/pct.conf.5.html
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pct_options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container features: nesting, keyctl, fuse

**Goal:** enable only the container capabilities a workload needs.

## Features
```sh
pct set 200 --features nesting=1,keyctl=1
pct set 201 --features fuse=1,mknod=1
pct set 202 --features 'mount=nfs;cifs'
```
| Feature | Needed for | Trade-off |
|---|---|---|
| `nesting=1` | Nested containers; systemd also uses it to isolate services | Exposes host procfs and sysfs contents to the guest |
| `keyctl=1` | Unprivileged CTs only: allows keyctl(); required to use Docker inside a container | Keyring syscalls allowed |
| `fuse=1` | FUSE file systems in the container | Interactions between fuse and the freezer cgroup can cause I/O deadlocks |
| `mknod=1` | Lets unprivileged CTs call mknod() for certain device nodes; needs a kernel with seccomp trap to user space (5.3 or newer) | Experimental |
| `mount=<fs;fs>` | Allow mounting listed file system types (for example nfs, cifs) | Negative effect on security; an NFS mount can block host I/O and stop it rebooting |
| `force_rw_sys=1` | Mount /sys as rw instead of mixed in unprivileged CTs | Can break networking with systemd-networkd (v245 or newer) |

## Raw LXC overrides
Advanced settings go in `/etc/pve/lxc/<id>.conf` as `lxc.*` lines, e.g. AppArmor profile
`lxc.apparmor.profile = unconfined` (not recommended for production; it brings security risks), or cgroup device allow rules for passthrough.

## Docker inside LXC?
Docker in an unprivileged container needs `keyctl=1`, and the docs say nesting is best used with unprivileged containers with additional id mapping. For maximum isolation, nest containers inside a VM.

## Gotchas
- Restart the container after changing features so the new settings apply.
- Privileged containers are considered unsafe by the LXC team; use them only in trusted environments.
- Container backups don't capture host-side AppArmor or cgroup tweaks.

## Verify
`pct config 200 | grep features` shows only the intended flags; the workload starts
(`systemctl --failed` empty inside the CT, `docker run hello-world` if applicable).

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: pct.conf.5-opts.adoc features option, pct.adoc AppArmor and Privileged Containers sections) and confirmed the feature names, defaults and trade-offs. Removed the unconfirmed privileged-only claim for mount=, the Debian 12 default claim and the Docker-breakage claim; quoted the semicolon list so the shell does not split it.

Method: documentation only; no commands were run.
