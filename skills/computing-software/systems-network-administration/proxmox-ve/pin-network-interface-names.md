---
id: computing-software.systems-network-administration.proxmox-ve.pin-network-interface-names
name: pin-network-interface-names
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [nic-naming, pve-network-interface-pinning, link-file, systemd-naming, update-initramfs]
level: advanced
status: docs-checked
description: "Prevent NIC names changing after upgrades by pinning names with pve-network-interface-pinning or .link files."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Systemd names Ethernet devices from driver, slot and bus (eno1, enp3s0f1). A newer systemd or a kernel/driver update can change names, which breaks `/etc/network/interfaces`. Two protections exist.

1. Pin the naming scheme version with the kernel parameter `net.naming-scheme=<version>`, for example `net.naming-scheme=v252`. This does not stop all changes caused by kernel or driver updates.
2. Override names per device, which is the robust option.

Automatic tool:

```
pve-network-interface-pinning generate
pve-network-interface-pinning generate --prefix myprefix
pve-network-interface-pinning generate --interface enp1s0 --target-name if42
```

It writes `.link` files to `/usr/local/lib/systemd/network` for physical NICs without one (default prefix `nic`, giving nic1, nic2) and writes `.new` copies of the files it rewrites: `/etc/network/interfaces`, `/etc/pve/nodes/<nodename>/host.fw`, `/etc/pve/sdn/controllers.cfg` and `/etc/pve/sdn/fabrics.cfg`. Compare with `diff -y /etc/network/interfaces /etc/network/interfaces.new`. To revert before rebooting, delete the `.new` files and the link files. The datacenter firewall file `/etc/pve/firewall/cluster.fw` is not updated automatically, as the mapping is node-local. Reboot to apply.

Manual alternative: create `/etc/systemd/network/10-enwan0.link` with `[Match]` (`MACAddress=...`, `Type=ether`) and `[Link]` (`Name=enwan0`), edit `interfaces`, run `update-initramfs -u -k all`, reboot. Names starting with `en` or `eth` are recognised as physical NICs in the GUI.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-sysadmin.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
