---
id: computing-software.systems-network-administration.virtualisation.proxmox-host-configuration-backup
name: proxmox-host-configuration-backup
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-host-backup, pmxcfs, proxmox-backup-client, config-backup, disaster-recovery, proxmox]
level: practitioner
status: docs-checked
description: "Back up Proxmox VE node and cluster configuration (/etc/pve, network, storage, corosync) that vzdump does not cover, and restore a rebuilt node from it."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pmxcfs.html
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
  - https://pbs.proxmox.com/docs/backup-client.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backing up Proxmox VE host configuration

vzdump backs up guests, not the host. A rebuilt node needs its network, storage and
cluster config, which live outside the guest backups.

## What to capture
| Path | Contents |
|---|---|
| `/etc/pve/` (pmxcfs, cluster-wide) | guest configs (`qemu-server/`, `lxc/`), `storage.cfg`, `user.cfg`, `datacenter.cfg`, firewall, HA, SDN, certificates |
| `/var/lib/pve-cluster/config.db` | the pmxcfs database file behind /etc/pve (SQLite) |
| `/etc/network/interfaces`, `/etc/hosts`, `/etc/hostname`, `/etc/resolv.conf` | node networking |
| `/etc/corosync/` | node-local corosync configuration and authkey |
| `/etc/apt/sources.list*`, `/etc/apt/sources.list.d/` | repositories |
| `/etc/vzdump.conf`, `/etc/cron.d/`, `/etc/modprobe.d/`, `/etc/kernel/cmdline`, `/etc/default/grub` | tuning, passthrough |
| `/etc/ssh/`, `/root/.ssh/` | host keys and cluster SSH trust |
| ZFS layout | `zpool status`, `zfs list -o name,mountpoint,compression` as text |

## Automate
```sh
#!/bin/sh
D=/root/hostbackup/$(hostname)-$(date +%F); mkdir -p $D
cp -a /var/lib/pve-cluster/config.db $D/config.db
tar czf $D/etc.tgz /etc/pve /etc/network /etc/hosts /etc/hostname /etc/corosync \
    /etc/apt /etc/vzdump.conf /etc/modprobe.d /etc/kernel /etc/default /etc/ssh /root/.ssh 2>/dev/null
zpool status > $D/zpool.txt; pvesm status > $D/pvesm.txt; ip -d addr > $D/ip.txt
```
Ship off-node: `proxmox-backup-client backup etc.pxar:/etc --repository <repository>` (the repository string comes from the datastore's connection information; encrypt with `--keyfile`) or rsync to another site. Schedule it, for example with a systemd timer.

## Restore a single rebuilt node (cluster still running)
1. Reinstall PVE same version, same hostname/IP.
2. Restore `/etc/network/interfaces`, hosts, apt sources, modprobe/kernel tweaks; reboot.
3. Remove the old node from the cluster (`pvecm delnode <node>` from a remaining node), clean up its leftovers (`/etc/pve/nodes/<node>`, known_hosts, `/etc/pve/priv/authorized_keys`, HA rules), then rejoin the reinstalled node with `pvecm add <IP-of-cluster-node>`; /etc/pve repopulates from the cluster. If SSH errors appear after rejoining with the same IP or hostname, run `pvecm updatecerts` once on the re-added node.
4. Re-import local storage pools so local guest disks reappear.

Standalone or whole-host recovery (the documented pmxcfs procedure): on the new host with nothing running, stop `pve-cluster`, replace `/var/lib/pve-cluster/config.db` (permissions 0600), adapt `/etc/hostname` and `/etc/hosts` to the lost host, reboot and check; guest disk data must be restored separately.

## Verify
Quarterly restore test: rebuild a lab node from the archive and confirm guests and
storage entries appear.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: pmxcfs.adoc Recovery and file table, pvecm.adoc node removal and rejoin) and the Proxmox Backup Server client documentation (github.com/proxmox/proxmox-backup docs/backup-client.rst) and confirmed that config.db backs /etc/pve, the recovery procedure for config.db, the pvecm delnode, pvecm add and pvecm updatecerts steps, and the proxmox-backup-client backup <name>.pxar:<path> --repository and --keyfile syntax. Removed the unconfirmed sqlite3 .backup, corosync-duplication and live-cluster config.db claims.

Method: documentation only; no commands were run.
