---
id: computing-software.systems-network-administration.virtualisation.proxmox-service-ports-reference
name: proxmox-service-ports-reference
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-ports, pve-firewall, firewall-lockout, proxmox-cluster, ceph, proxmox]
level: practitioner
status: docs-checked
description: "Ports Proxmox VE, corosync, Ceph, SPICE/VNC, migration and Proxmox Backup Server use, so external firewalls and the PVE firewall allow exactly what the cluster needs."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pve-firewall.html
  - https://pbs.proxmox.com/docs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox ports reference

| Service | Port/protocol | Between |
|---|---|---|
| Web GUI / API (pveproxy) | TCP 8006 | admins → nodes, nodes ↔ nodes |
| VNC web console | TCP 5900-5999 | management hosts → nodes |
| SPICE proxy | TCP 3128 | client → node |
| SSH | TCP 22 | admins → nodes; node ↔ node (cluster actions) |
| rpcbind | UDP 111 | listed in the admin guide |
| sendmail/postfix | TCP 25 | node → relay |
| Corosync (knet) | UDP 5405-5412 | node ↔ node on each corosync link |
| Live migration (QEMU) | TCP 60000-60050 | node ↔ node on migration network |
| Proxmox Backup Server | TCP 8007 | PVE nodes → PBS, admins → PBS |

## PVE firewall defaults
With the datacenter firewall enabled and policy DROP, PVE keeps implicit "management"
rules for the `management` ipset (or local network detected from cluster config) on 8006,
22, 5900-5999, 3128. Check `pve-firewall localnet`; if it shows the wrong network, define
`[IPSET management]` explicitly before enabling, or you lock yourself out.
The firewall chapter also lists implicit rules for corosync traffic in the cluster network.

## Gotchas
- Migration over a separate network: the port range applies on that network; set
  `migration: secure,network=10.10.50.0/24` in `datacenter.cfg`.

## Verify
From each node: `nc -zv <peer> 8006 22`, `ss -ulpn | grep corosync`; from admin net
`curl -k https://node:8006`; migration test succeeds across the firewall.

## Checked

2026-10-28

Confirmed: Admin guide and firewall chapter: 8006, 5900-5999, 3128, 22, rpcbind UDP 111, sendmail 25 outgoing, corosync UDP 5405-5412, migration 60000-60050, pve-firewall localnet, [IPSET management], migration: secure,network= in datacenter.cfg; PBS web port 8007.

Removed or corrected: Ceph, VXLAN, BGP and DHCP rows (not in the fetched pages), the 111 TCP claim, websocket and migration-requirement claims, fragmented-UDP and external-RBD gotchas.

Method: documentation only; no commands were run.
