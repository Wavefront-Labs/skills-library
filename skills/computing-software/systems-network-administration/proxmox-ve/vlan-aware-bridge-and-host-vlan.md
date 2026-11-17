---
id: computing-software.systems-network-administration.proxmox-ve.vlan-aware-bridge-and-host-vlan
name: vlan-aware-bridge-and-host-vlan
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [vlan, bridge-vlan-aware, bridge-vids, vlan-tag, trunk]
level: practitioner
status: docs-checked
description: "Set up VLAN-aware bridges and put the host management address on a VLAN in Proxmox VE."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VLANs split a physical network into isolated layer-2 domains identified by a tag. Proxmox VE supports four guest-side approaches: a VLAN-aware Linux bridge (each guest NIC gets a tag, handled transparently; trunk mode is possible but then the guest needs its own configuration), a traditional VLAN bridge that creates a VLAN device plus bridge per VLAN (a guest on VLAN 5 creates `eno1.5` and `vmbr0v5`, which stay until reboot), Open vSwitch VLANs, and VLANs configured inside the guest, which allows several VLANs on one virtual NIC.

For the guest, you simply set the VLAN tag in the network device when you create it.

Host management on VLAN 5 with a VLAN-aware bridge:

```
auto vmbr0.5
iface vmbr0.5 inet static
        address  10.10.10.2/24
        gateway  10.10.10.1
auto vmbr0
iface vmbr0 inet manual
        bridge-ports eno1
        bridge-stp off
        bridge-fd 0
        bridge-vlan-aware yes
        bridge-vids 2-4094
```

The same with a traditional bridge uses `iface eno1.5 inet manual` and a second bridge `vmbr0v5` with `bridge-ports eno1.5` holding the address, next to a plain `vmbr0` on `eno1`. For fail-safe setups put the VLAN on top of a bond (`bond0.5`).

General rule: configure the VLAN on the interface with the least abstraction layers between itself and the physical NIC. After editing use Apply Configuration or `ifreload -a`.

## Checked

2026-11-09. Confirmed against the Proxmox VE docs chapter Host System Administration (chapter-sysadmin), Network Configuration and VLAN sections: eno1.5 and vmbr0v5 behaviour, bridge-vids 2-4094 example, VLAN on top of a bond, ifreload -a. Reworded the abstraction-layers rule to the page wording.

Method: documentation only; no commands were run.
