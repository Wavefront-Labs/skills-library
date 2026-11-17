---
id: computing-software.systems-network-administration.proxmox-ve.apply-network-changes-ifupdown2
name: apply-network-changes-ifupdown2
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [ifupdown2, ifreload, interfaces-new, pvenetcommit, network-apply]
level: practitioner
status: docs-checked
description: "Stage and apply Proxmox VE network changes safely with interfaces.new, ifreload -a, and ifupdown2."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The whole host network is configured in `/etc/network/interfaces` (format in `interfaces(5)`). Edit via the GUI where possible because it protects against mistakes. Proxmox VE does not write GUI changes directly; it stages them in `/etc/network/interfaces.new`, so many related changes can be applied together and checked first. A wrong network config can make a node unreachable, so review the staged file before applying.

With the recommended `ifupdown2` package (default since Proxmox VE 7.0) changes apply live without a reboot:

- GUI: click Apply Configuration. This moves `interfaces.new` over `interfaces` and applies it.
- Manual edits of `/etc/network/interfaces`: run `ifreload -a`.
- Installed on plain Debian or upgraded from before 7.0: `apt install ifupdown2` first.

Alternatively reboot: the `pvenetcommit` systemd service activates the staged `interfaces.new` before networking starts.

Avoid the traditional `ifup` and `ifdown` when unsure. For example `ifdown vmbrX` interrupts all guest traffic on that bridge, and a later `ifup` does not reconnect those guests.

Naming conventions: `en*` systemd names for new installs (eno1, enp3s0f1), `ethN` for hosts installed before 5.0, bridges `vmbrN` (any alphanumeric name of up to 10 characters starting with a letter), bonds `bondN`, VLAN devices as `eno1.50`. Names that make the device type obvious help troubleshooting.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-sysadmin.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
