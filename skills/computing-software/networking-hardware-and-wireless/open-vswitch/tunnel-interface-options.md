---
id: computing-software.networking-hardware-and-wireless.open-vswitch.tunnel-interface-options
name: tunnel-interface-options
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, remote-ip, tunnel-options, geneve, gre, vxlan, in-key, out-key, csum, ttl, tos, gtpu, erspan]
level: advanced
status: docs-checked
description: "Reference for Open vSwitch tunnel Interface types and options: remote_ip, local_ip, key, in_key/out_key, dst_port, tos, ttl, df_default, csum, packet_type, exts, ERSPAN."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
  - https://docs.openvswitch.org/en/latest/faq/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tunnel interface options
Interface `type` values for tunnels: `geneve`, `gre` (over IPv4), `ip6gre`, `vxlan` (UDP port 4789), `gtpu` (UDP port 2152), `bareudp`, `srv6`; `erspan` interfaces have their own options. The types a given instance supports are listed in the Open_vSwitch `iface_types` column.

Example: `ovs-vsctl add-port br0 gre0 -- set interface gre0 type=gre options:remote_ip=192.168.1.10`

Each tunnel must be uniquely identified by type, `remote_ip`, `local_ip` and `in_key`; the more specific port matches first (`in_key` is more specific than `local_ip`). `in_key` is not used for bareudp and srv6.

Common options (geneve, bareudp, gre, ip6gre, vxlan, srv6):
- `remote_ip`: required; an IPv4/IPv6 address (not a DNS name; unicast only) or `flow`. With `flow` the tunnel accepts packets from any remote endpoint and flow actions must set `tun_dst` or `tun_ipv6_dst` when sending.
- `local_ip`: optional; the destination IP received packets must match; default matches all addresses. May be `flow`, but only on tunnels also using `remote_ip=flow`.
- `key`: shorthand for setting `in_key` and `out_key` together.
- `in_key`: 0 (same as unset), a positive 24-bit (Geneve, VXLAN) or 32-bit (GRE) number, or `flow` (any key; placed in `tun_id`).
- `out_key`: 0 (no key, same as unset), a positive 24-bit or 32-bit number as above, or `flow` (set via `set_tunnel`; 0 if no action).
- `dst_port`: transport destination port for UDP tunnels (Geneve, VXLAN).
- `tos`: DSCP and ECN bits for the outer packet (ECN part must be zero), default 0; `inherit` copies from an inner IPv4/IPv6 packet. ECN fields are always inherited.
- `ttl`: default is the system default TTL; `inherit` copies from an inner IPv4/IPv6 packet.
- `df_default`: true or false; default enabled, sets Don't Fragment on outer headers to allow path MTU discovery.
- `egress_pkt_mark`: pkt_mark set on the encapsulating packet.

Other options:
- vxlan `exts`: comma-separated `gbp` and/or `gpe`. Without `gpe` a VXLAN packet always encapsulates an Ethernet frame.
- vxlan and gre `packet_type`: `legacy_l2` (default), `legacy_l3`, `ptap`. For vxlan, `legacy_l3` requires `gpe` in `exts`, and ptap needs `gpe` to send non-Ethernet packets.
- gre only `seq`: 4-byte sequence number field, default disabled.
- gre, ip6gre, geneve, bareudp, vxlan `csum`: when unset, outer checksums are computed for UDP IPv6 tunnels and not for GRE or IPv4 UDP; incoming checksums are validated regardless. With the Linux kernel datapath, geneve and vxlan checksums need kernel 4.0 or higher.
- erspan only: `erspan_ver` (1 for type II, 2 for type III), `erspan_idx` (20-bit), `erspan_dir` (v2 only: 1 egress, 0 ingress), `erspan_hwid` (6-bit, v2).
- bareudp only: `payload_type`, the ethertype of the L3 protocol tunnelled.
- IPsec (gre, geneve, vxlan): `psk`, `remote_cert`, `remote_name`.

FAQ examples:
- IPv6 GRE (L2 only; L3 GRE over IPv6 is not supported): `ovs-vsctl add-port br0 at_gre0 -- set int at_gre0 type=ip6gre options:remote_ip=fc00:100::1 options:packet_type=legacy_l2`
- GTP-U (userspace datapath, OVS 2.13 and later; the TEID is the tunnel key): `ovs-vsctl add-port br0 gtpu0 -- set int gtpu0 type=gtpu options:key=<teid> options:remote_ip=172.31.1.1`

## Checked
2026-11-04. Confirmed against ovs-vswitchd.conf.db(5) Interface table (types, Tunnel Options sections) and the configuration FAQ (IPv6 GRE, GTP-U). Removed the Verify line (`ovs-appctl tnl/ports/show` is not on the pages), and corrected `packet_type` to cover the legacy_l3 and gpe requirement.
Method: documentation only; no commands were run.
