---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ofctl-flow-match-syntax
name: ofctl-flow-match-syntax
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, match-fields, tun-metadata, flow-masks, ovs-fields, shorthand, prerequisites, tlv-map]
level: practitioner
status: docs-checked
description: "Write OpenFlow match syntax for ovs-ofctl using ovs-fields: shorthands (ip, tcp, arp), prerequisites, value/mask bit matching, CIDR, tunnel fields, tun_metadata and add-tlv-map."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-fields.7.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-ofctl.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ofctl flow match syntax
Shorthands (ovs-fields(7)): `eth` (packet_type=(0,0), OVS 2.8+), `ip` (eth_type=0x0800), `ipv6` (0x86dd), `icmp` (eth_type=0x0800,ip_proto=1), `icmp6` (0x86dd, 58), `tcp` (0x0800, ip_proto=6), `tcp6`, `udp` (ip_proto=17), `udp6`, `sctp` (ip_proto=132), `sctp6`, `arp` (0x0806), `rarp` (0x8035), `mpls` (0x8847), `mplsm` (0x8848).

Prerequisites: a match on a field must also include its prerequisite, for example an IPv4 field needs `eth_type=0x0800` (so `ip`). TCP, UDP and SCTP need IPv4 or IPv6 plus ip_proto 6, 17 or 132 (and nw_frag must not select later fragments); ICMPv4 needs IPv4 and ip_proto=1; ICMPv6 needs IPv6 and ip_proto=58; a VLAN VID match needs `vlan_tci=0x1000/0x1000` (a VLAN header present). A match that omits the prerequisite has the field dropped (see ofctl-add-and-dump-flows).

Match forms:
- Exact: `field=value` (all fields support it).
- Bitwise: `field=value/mask`, for fields that support masking; some fields also accept other forms, for example `nw_src=10.1.0.0/255.255.0.0` may be written `nw_src=10.1.0.0/16`.
- Port range via mask: `tcp,tp_src=0x03e8/0xfff8` (example from the page).

Other fields: `in_port` (not maskable), `pkt_mark` (maskable, OVS 2.0+), `conj_id` (conjunctive matching; not maskable and not writable), registers `reg0` to `reg15` (4 bytes each, maskable; `reg16` to `reg31` need OVS 3.7+), 8-byte `xreg0`..., 16-byte `xxreg0`.... `skb_priority` is read-only and has no OXM or NXM, so it cannot be matched.

Tunnel fields (maskable, read/write): `tun_id` (8 bytes, OF 1.3+ and OVS 1.1+), `tun_src` and `tun_dst` (IPv4), `tun_ipv6_src` and `tun_ipv6_dst` (OVS 2.5+), `tun_flags` (OVS 2.5+; written with symbolic names, `tun_flags=+oam` matches only OAM packets; only the `oam` flag is defined), `tun_metadata0` to `tun_metadata63` (124 bytes each, OVS 2.5+), plus Geneve/GBP/ERSPAN/GTP-U fields such as `tun_gbp_id`, `tun_erspan_ver`, `tun_gtpu_flags`.

Geneve option mapping (ovs-ofctl(8); Nicira extension, OVS 2.5 or later):
```
ovs-ofctl add-tlv-map br0 "{class=0xffff,type=0,len=4}->tun_metadata0"
ovs-ofctl add-flow br0 tun_metadata0=1234,actions=controller
```
Commands: `add-tlv-map switch option[,option]...` (duplicate fields are rejected), `del-tlv-map switch [option[,option]]...` (all mappings if none given), `dump-tlv-map switch`. A mapping should not be changed while a flow uses it; the result is undefined.

Another example from ovs-fields(7) elsewhere: set a tunnel with `in_port=1,actions=set_tunnel:5001,set_field:192.168.1.1->tun_dst,3`.

## Checked
2026-11-04. Confirmed against ovs-fields(7) (Matching, Shorthands, prerequisites, tunnel and metadata fields, registers) and ovs-ofctl(8) (tunnel TLV table commands). Removed the invented `add-flow br0 in_port=3,tun_src=...,tun_id=5001,actions=normal` example (not on the page), the claim that tun_src/tun_dst are the only tunnel address fields, and the `reg0..reg15`-only claim.
Method: documentation only; no commands were run.
