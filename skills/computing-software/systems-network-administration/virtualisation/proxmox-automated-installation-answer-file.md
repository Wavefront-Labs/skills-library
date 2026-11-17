---
id: computing-software.systems-network-administration.virtualisation.proxmox-automated-installation-answer-file
name: proxmox-automated-installation-answer-file
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [proxmox-auto-install, answer-toml, proxmox-installation, pve-install, unattended-install, proxmox]
level: practitioner
status: docs-checked
description: "Install Proxmox VE unattended with an answer.toml: prepare the ISO, serve answers by partition or HTTP, disk filters, ZFS layout, first-boot hooks and validation."
sources:
  - https://pve.proxmox.com/wiki/Automated_Installation
  - https://pve.proxmox.com/pve-docs/chapter-pve-installation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox VE automated installation

Available since PVE 8.2, prepared with the `proxmox-auto-install-assistant` tool.

## Answer file
```toml
[global]
keyboard = "en-us"
country = "gb"
fqdn = "pve01.corp.example"
mailto = "ops@corp.example"
timezone = "Europe/London"
root-password-hashed = "$6$..."          # PVE 8.3+; generate with mkpasswd, for example
root-ssh-keys = ["ssh-ed25519 AAAA... ops"]

[network]
source = "from-dhcp"                      # or "from-answer" with cidr, gateway, dns, filter.ID_NET_NAME_MAC

[disk-setup]
filesystem = "zfs"
zfs.raid = "raid1"
disk-list = ["sda", "sdb"]               # or filter, e.g. filter.ID_SERIAL = "KIOXIA_KCMYXVUG1T60*"

[first-boot]                              # PVE 8.3+
source = "from-iso"
ordering = "fully-up"
```
Validate before baking: `proxmox-auto-install-assistant validate-answer answer.toml`.
List what the installer will see on the target hardware:
`proxmox-auto-install-assistant device-info -t disk`.

## Delivery modes
```sh
# embed in ISO
proxmox-auto-install-assistant prepare-iso proxmox-ve_8.x.iso --fetch-from iso --answer-file answer.toml
# from a USB partition labelled "proxmox-ais"
proxmox-auto-install-assistant prepare-iso proxmox-ve_8.x.iso --fetch-from partition
# from HTTP(S): installer POSTs hardware info (JSON), server returns per-host TOML
proxmox-auto-install-assistant prepare-iso proxmox-ve_8.x.iso --fetch-from http \
    --url https://deploy.corp.example/answer --cert-fingerprint <sha256>
```
The HTTP mode lets one ISO serve a whole fleet: map MAC or serial number to hostname/IP
server-side. DHCP option or DNS TXT record can provide the URL instead of baking it.

## First-boot script
Use it to set repositories, join the cluster, or install agents; its stage is set by
`ordering` (`before-network`, `network-online` or `fully-up`).

## Gotchas
- Disk names (`sda`) are not stable across controllers; prefer filters on
  serial/model/WWN.
- A wrong `disk-list` or filter selects the wrong disks. Test on one node.

## Verify
Node boots to the expected FQDN, `zpool status rpool` shows the intended mirror,
and the first-boot script's effects are present.

## Checked

2026-10-28

Confirmed: Automated Installation wiki: answer file keys root-password-hashed, root-ssh-keys, disk-list, filter.ID_SERIAL, zfs.raid, first-boot ordering values, 8.3 first-boot hook, device-info, prepare-iso fetch modes, proxmox-ais partition label, DHCP option and DNS TXT delivery, validate-answer.

Removed or corrected: underscore key names (the real keys use hyphens), zfs.ashift, debug-shell claim, journalctl unit, reboot-loop gotcha, pveversion.

Method: documentation only; no commands were run.
