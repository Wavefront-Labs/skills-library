---
id: computing-software.systems-network-administration.proxmox-ve.linux-bond-modes-lacp
name: linux-bond-modes-lacp
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [bond, lacp, 802-3ad, active-backup, bond-mode]
level: practitioner
status: docs-checked
description: "Configure Linux bonds on Proxmox VE and choose between LACP, active-backup and the other modes."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Bonding (NIC teaming) combines NICs for fault tolerance, speed, or both. The seven kernel modes are balance-rr, active-backup, balance-xor, broadcast, 802.3ad (LACP), balance-tlb and balance-alb. If the switch supports LACP use `802.3ad`; otherwise generally use `active-backup`. The tlb and alb modes should not be used with a Linux bridge that carries guests.

Bond used directly as the bridge port, which makes guest traffic fault tolerant:

```
auto bond0
iface bond0 inet manual
      bond-slaves eno1 eno2
      bond-miimon 100
      bond-mode 802.3ad
      bond-xmit-hash-policy layer2+3
auto vmbr0
iface vmbr0 inet static
        address  10.10.10.2/24
        gateway  10.10.10.1
        bridge-ports bond0
        bridge-stp off
        bridge-fd 0
```

A bond with its own fixed IP (`iface bond0 inet static` with `address`) works as a storage network.

Corosync does not need a bond for redundancy because it can switch between its own links. If a bond must carry corosync traffic, avoid balance-rr, balance-xor, balance-tlb and balance-alb. With LACP set `bond-lacp-rate fast` on both host and switch: the default slow rate sends an LACPDU every 30 seconds, so failover takes about 90 seconds, while HA nodes fence themselves after roughly one minute without stable quorum. Fast on both sides reduces failover to about 3 seconds. Active-backup avoids asymmetric connectivity but may not switch over on a silent failure.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-sysadmin.html, https://pve.proxmox.com/pve-docs/chapter-pvecm.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
