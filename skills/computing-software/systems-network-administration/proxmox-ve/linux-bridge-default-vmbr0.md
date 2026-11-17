---
id: computing-software.systems-network-administration.proxmox-ve.linux-bridge-default-vmbr0
name: linux-bridge-default-vmbr0
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [bridge, vmbr0, bridge-ports, routed, masquerade]
level: intro
status: docs-checked
description: "Understand the default vmbr0 bridge and the routed and NAT masquerade alternatives for Proxmox VE guests."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Linux bridge (conventionally `vmbrN`) is a software switch that connects guest NICs and physical interfaces. The installer creates `vmbr0` on the first NIC; a host can have up to 4094 bridges. Default config:

```
auto vmbr0
iface vmbr0 inet static
        address 192.168.10.2/24
        gateway 192.168.10.1
        bridge-ports eno1
        bridge-stp off
        bridge-fd 0
```

Guests appear on the LAN with their own MACs, as if plugged into a switch with the host as the switch.

Choose the model by environment:
- Private LAN behind an external gateway: bridged (default).
- Hosting provider with a public IP block: bridged or routed, whichever the provider allows. Many providers disable ports that show several MACs, so use routing. A routed setup sets `bridge-ports none` on vmbr0, enables `ip_forward` and `proxy_arp` on the uplink via `post-up` lines, and gives vmbr0 the first usable address of the guest block.
- Single public IP: masquerading plus port forwarding for inbound traffic.

Masquerade example on a private vmbr0 with `bridge-ports none`:

```
post-up   echo 1 > /proc/sys/net/ipv4/ip_forward
post-up   iptables -t nat -A POSTROUTING -s '10.10.10.0/24' -o eno1 -j MASQUERADE
post-down iptables -t nat -D POSTROUTING -s '10.10.10.0/24' -o eno1 -j MASQUERADE
```

With the firewall enabled, outgoing connections may need conntrack zones: `iptables -t raw -I PREROUTING -i fwbr+ -j CT --zone 1` (and the matching `-D` in post-down). The option `bridge-disable-mac-learning 1` (7.3 and later) turns off MAC learning; Proxmox then adds guest MACs to the bridge forwarding table itself.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-sysadmin.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
