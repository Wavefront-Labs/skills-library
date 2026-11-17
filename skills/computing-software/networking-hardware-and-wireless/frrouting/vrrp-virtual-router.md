---
id: computing-software.networking-hardware-and-wireless.frrouting.vrrp-virtual-router
name: vrrp-virtual-router
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, vrrpd, vrrp, macvlan, virtual-ip, high-availability, first-hop-redundancy]
level: practitioner
status: docs-checked
description: "Run VRRP with FRR vrrpd: prepare Linux macvlan devices, configure VRID, priority, advertisement interval and virtual IPs, use autoconfigure, and check state with show vrrp."
sources:
  - https://docs.frrouting.org/en/latest/vrrp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VRRP with vrrpd
Kernel prerequisites: Linux 5.1 or later; FRR does not create macvlan devices.
- Virtual MAC is `00:00:5e:00:01:<VRID>` (IPv4) and `00:00:5e:00:02:<VRID>` (IPv6), so each family needs its own macvlan.
- Macvlan must be in `bridge` mode (`private` breaks VRRP); use `addrgenmode random` for IPv6 devices (`eui64` breaks election).
- The virtual IP must not be on the parent interface; IPv4 VRRP needs an IPv4 address on the parent.
- Example: `ip link add vrrp4-2-1 link eth0 addrgenmode random type macvlan mode bridge`, then set its address to the virtual MAC, add the virtual IP and bring it up.
- If forwarding problems persist, the docs suggest `sysctl -w net.ipv4.conf.eth0.ignore_routes_with_linkdown=1`.

Interface config:
- `vrrp (1-255) [version (2-3)]` (default 3).
- `vrrp VRID priority (1-254)` (255 reserved for the acting master; ties go to highest primary IP).
- `vrrp VRID advertisement-interval (10-40950)` ms, multiples of 10.
- `vrrp VRID ip A.B.C.D` / `vrrp VRID ipv6 X:X::X:X` (address must already be on the macvlan; adding it activates the router; IPv6 fails with VRRPv2).
- `vrrp VRID preempt` (default on); `vrrp VRID checksum-with-ipv4-pseudoheader` (default on; the page says it does not affect VRRPv2 or IPv6); `vrrp VRID shutdown`.

Global: `vrrp default ...` (new routers only), `vrrp autoconfigure [version (2-3)]`, `show vrrp [interface IFNAME] [VRID] [json]`, `debug vrrp`.

## Checked

2026-11-08. Read the whole FRR VRRP page: Linux 5.1 requirement, macvlan bridge mode and addrgenmode, virtual MAC layout, interface commands and ranges, defaults, autoconfigure, show and debug commands, troubleshooting sysctl. Reworded the checksum line.
Method: docs-only read of cited pages, 2026-11-08
