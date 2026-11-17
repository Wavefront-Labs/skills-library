---
id: computing-software.systems-network-administration.virtualisation.proxmox-lxc-start-failure-debugging
name: proxmox-lxc-start-failure-debugging
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [lxc-start-debug, pct, lxc, unprivileged-container, apparmor, proxmox]
level: advanced
status: docs-checked
description: "Debug a Proxmox container that will not start: foreground start with debug log, common causes (mount points, idmap, AppArmor, cgroup v2, storage) and fixes."
sources:
  - https://pve.proxmox.com/pve-docs/pct.1.html
  - https://github.com/proxmox/pve-docs/blob/master/pct.adoc
  - https://github.com/lxc/lxc/blob/main/doc/lxc-start.sgml.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container fails to start

The GUI usually says only "startup for container 'N' failed". Get the real error:
```sh
pct start 201 --debug                 # enables very verbose debug log-level on start
# or run LXC in the foreground
lxc-start -n 201 -F
pct config 201
journalctl -b | grep -iE "apparmor|lxc|201" | tail
```

## Common causes
| Log hint | Cause | Fix |
|---|---|---|
| `Failed to mount ... mp0` / `No such file or directory` | bind-mount source path missing on this node | create path / mount the host storage, or move container |
| `Permission denied` on bind mount in unprivileged CT | host files owned by root (uid 0); CT root maps to an unprivileged host id | `chown` the host dir to the mapped id or add `lxc.idmap` entries |
| `newuidmap failed` / idmap errors | custom `lxc.idmap` lines not matched in `/etc/subuid` `/etc/subgid` | add `root:1000:1` etc. on host |
| `apparmor="DENIED" operation="mount"` in journal | AppArmor prohibits some system calls such as mount (nested mounts, NFS inside CT) | enable the needed features (`nesting=1`, `mount=nfs`) rather than disabling AppArmor |
| `cgroup` errors with old distros (CentOS 7, Ubuntu 16.10) | container systemd older than 231 does not support cgroup v2; cgroup v1 was removed in PVE 9.0 | upgrade the CT OS |
| ostype detection fails or mismatches | PVE checks `/etc/os-release` to detect the distribution; start fails if the configured `ostype` differs from the detected one | correct `ostype`, or set `ostype: unmanaged` to skip OS-specific setup |
| storage `volume ... does not exist` | rootfs on storage not active on this node | check `pvesm status`, restore volume |
| rootfs filesystem errors | damaged filesystem | `pct fsck 201` with the container stopped (`--force` checks even a clean filesystem) |

## Mount the rootfs to inspect
```sh
pct mount 201                  # mounts the container filesystem on the host
pct unmount 201
```
`pct mount` is for emergency maintenance only: it holds a lock that blocks everything except start and stop until you `pct unmount`.

## Gotchas
- Convert privileged to unprivileged with backup and `pct restore --unprivileged 1`, not by copying files by hand.
- Stale lock after a power failure: `pct unlock 201`, only when you are sure the locking action is finished.

## Verify
`pct start 201` succeeds; `pct enter 201` then `systemctl --failed` empty.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: pct.adoc AppArmor, cgroup, OS detection and Locks sections; generated pct.1-synopsis.adoc start --debug, fsck and mount) and the LXC lxc-start documentation (--foreground) and confirmed the pct start --debug, pct fsck, pct mount/unmount and pct unlock behaviour, the systemd 231 requirement for cgroup v2 and the cgroup v1 removal in PVE 9.0. Removed the unconfirmed PVE 7.4 gate, log-file command line, 100000 figure and pre-start hook error text.

Method: documentation only; no commands were run.
