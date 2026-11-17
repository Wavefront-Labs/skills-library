---
id: computing-software.systems-network-administration.virtualisation.proxmox-nic-name-pinning
name: proxmox-nic-name-pinning
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [nic-name-pinning, pve-network, systemd-link, predictable-interface-names, pve-upgrade, proxmox]
level: practitioner
status: docs-checked
description: "Stop Proxmox NIC names changing after kernel or hardware changes: pin with systemd .link files or pve-network-interface-pinning, and recover a node that lost network."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.link.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pinning network interface names

Predictable names (`enp65s0f0`, `eno1`) can change after a kernel or systemd upgrade (new
naming scheme), a BIOS/firmware update, or adding a PCIe card. Then `vmbr0` references a
non-existent port and the node is unreachable after reboot.

## Pin with a .link file (matches by MAC)
```ini
# /etc/systemd/network/10-nic0.link
[Match]
MACAddress=3c:ec:ef:12:34:56
Type=ether

[Link]
Name=nic0
```
Repeat per port (`nic1`, ...), update `/etc/network/interfaces` to the new names, then
`update-initramfs -u -k all` (names are applied early in boot) and reboot in a window.

Proxmox VE ships `pve-network-interface-pinning` (see the admin guide's network chapter), which generates these files and rewrites the
PVE network config:
```sh
pve-network-interface-pinning generate          # all physical NICs -> nicN
pve-network-interface-pinning generate --interface enp65s0f0 --target-name mgmt0
```

## Recover a node with renamed NICs
From IPMI console:
```sh
ip -br link                      # see the new names and MACs
nano /etc/network/interfaces     # replace old names with new ones (bond-slaves, bridge-ports)
ifreload -a
```
Then pin the names so it doesn't recur.

## Gotchas
- Names must not collide with kernel names (`eth0`) to avoid races; use `nicN` or
  descriptive names, max 15 chars.
- Bond members change the MAC of slaves to the bond MAC at runtime; match on `PermanentMACAddress=` if needed
  or match by `Path=` (PCI path) instead of MAC.
- Replacing a NIC changes the MAC: update the .link file.

## Verify
After reboot, `ip -br link` shows pinned names, `ifreload -a` applies cleanly, and a test kernel
upgrade + reboot keeps the names.

## Checked

2026-10-28

Confirmed: Admin guide sysadmin chapter (pve-network-interface-pinning generate, --interface, --target-name, update-initramfs -u -k all, reboot) and systemd.link (PermanentMACAddress, 15-character name limit).

Removed or corrected: the PVE 8 to 9 upgrade anecdote, PVE 9 version claim, systemd 254 claim, ifquery check.

Method: documentation only; no commands were run.
