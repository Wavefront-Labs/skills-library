---
id: computing-software.systems-network-administration.virtualisation.proxmox-install-on-debian
name: proxmox-install-on-debian
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-on-debian, pve-install, proxmox-installation, debian, custom-partitioning, proxmox-iso, unattended-install, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Install Proxmox VE from the ISO (ZFS/ext4 choices, automated answer file) or on top of an existing Debian with custom partitioning, including hostname/hosts requirements."
sources:
  - https://pve.proxmox.com/wiki/Install_Proxmox_VE_on_Debian_12_Bookworm
  - https://pve.proxmox.com/wiki/Automated_Installation
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#chapter_installation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing Proxmox VE (ISO or on top of Debian)

**Goal:** a node with the storage layout and network you intended, installed repeatably.

## ISO installer choices
- **Target filesystem:** ext4/xfs on LVM (local + local-lvm thin pool), or **ZFS** (RAID1
  mirror of two boot SSDs is the common choice; gives snapshots and replication). ZFS
  needs HBA/IT mode, not hardware RAID.
- Advanced options: `hdsize`, `swapsize`, `maxroot`, `minfree`, `maxvz` (LVM) or `ashift`,
  `arc max` (ZFS).
- Management network: hostname as FQDN, static IP; becomes `vmbr0`.

## Automated install (PVE 8.2+)
Prepare an answer file (`answer.toml`) with keyboard, timezone, root password hash,
network, disk setup; embed it in the ISO or fetch it via HTTP/partition:
```sh
proxmox-auto-install-assistant prepare-iso proxmox-ve.iso --fetch-from iso --answer-file answer.toml
proxmox-auto-install-assistant validate-answer answer.toml
```

## Install on Debian (custom partitioning, existing tooling)
1. Minimal Debian of the matching release (the wiki page covers Debian 12 Bookworm).
2. `/etc/hosts` must map the hostname to the **real IP**, not 127.0.1.1:
   `192.0.2.10 pve1.<domain> pve1`, check with `hostname --ip-address`.
3. Add the Proxmox repo and key, then:
```sh
apt update && apt full-upgrade
apt install proxmox-default-kernel && reboot
apt install proxmox-ve postfix open-iscsi chrony
apt remove linux-image-amd64 'linux-image-6.1*' && update-grub
apt remove os-prober
```
4. Create `vmbr0` in the GUI (or `/etc/network/interfaces`) and move the host IP onto it.

## Gotchas
- The wiki advises mapping the hostname to the real IP rather than 127.0.1.1 (the cluster system cycles through all addresses).
- Hardware RAID with ZFS on top hides disk errors from ZFS; use plain disks.
- Secure Boot is supported out of the box since PVE 8.1 (signed packages and proxmox-boot-tool).
- Hostname changes after install are painful (certificates, cluster); decide first.

## Verify
`https://<ip>:8006` loads, the version shown in the GUI matches, `systemctl status pve-cluster pveproxy`
are active, and storage shows `local` and `local-lvm`/`local-zfs`.

## Checked

2026-10-28

Confirmed: Install on Debian 12 wiki (hostname --ip-address, proxmox-default-kernel, package list, os-prober, Secure Boot), Automated Installation wiki (prepare-iso, validate-answer, --fetch-from), admin guide (Secure Boot since 8.1).

Removed or corrected: the Debian 13 / PVE 9 pairing, the cluster-certificate claim, pveversion.

Method: documentation only; no commands were run.
