---
id: computing-software.systems-network-administration.network-design.encapsulation-overhead-calculation
name: encapsulation-overhead-calculation
category: computing-software
field: systems-network-administration
product: network-design
tags: [encapsulation-overhead, mtu, vxlan, ipsec, gre, mss, tunnel-design, jumbo-frames]
level: practitioner
status: verified
description: "Calculate header overhead for VLAN, QinQ, MPLS, GRE, VXLAN, GENEVE, IPsec and WireGuard, derive the safe MTU/MSS for each design, and verify end to end."
sources:
  - https://www.rfc-editor.org/rfc/rfc7348
  - https://www.rfc-editor.org/rfc/rfc4459
  - https://www.cisco.com/c/en/us/support/docs/ip/generic-routing-encapsulation-gre/25885-pmtud-ipfrag.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encapsulation overhead calculation

Every tunnel steals bytes from the payload. Get the numbers right in the design, not after users
report "small pings work, file copies hang".

## Overhead table (bytes added to an IPv4 packet)
| Encapsulation | Overhead | Notes |
|---|---|---|
| 802.1Q tag | 4 | on the Ethernet frame, not the IP MTU |
| QinQ | 8 | |
| MPLS label | 4 each | L3VPN = 2 labels = 8 |
| GRE | 24 | 20 outer IPv4 + 4 GRE (+4 with key) |
| IP-in-IP | 20 | |
| VXLAN | 50 | 14 inner Ethernet + 8 VXLAN + 8 UDP + 20 outer IPv4 (70 with outer IPv6); outer Ethernet header (and any outer VLAN tag) is on top of this |
| GENEVE | 50 + options | same layout as VXLAN with an 8-byte fixed header (RFC 8926) plus variable options in 4-byte units |
| IPsec ESP tunnel, AES-GCM (16-byte ICV) | 54-57 | outer IP 20 + ESP header 8 + IV 8 + padding 0-3 + pad-length/next-header 2 + ICV 16; 62-65 with NAT-T UDP (8 more) |
| IPsec ESP tunnel, AES-CBC + HMAC-SHA1-96 | 58-73 | same but IV 16, ICV 12, padding 0-15; 66-81 with NAT-T |
| GRE over IPsec (ESP transport mode) | 58-61 (AES-GCM), 62-77 (AES-CBC + SHA1-96) | GRE 24 + ESP without a second IP header; add 8 for NAT-T |
| WireGuard | 60 (IPv4) / 80 (IPv6) | outer IP + UDP 8 + WG 32 (16-byte data header + 16-byte tag, before 16-byte padding of the payload) |
| PPPoE | 8 | the classic 1492 MTU |

## Derive MTU and MSS
Inner MTU = path MTU - overhead. TCP MSS = inner MTU - 40 (IPv4 + TCP headers) or - 60 for IPv6.

Examples on a 1500-byte internet path:
- GRE: 1500 - 24 = 1476 MTU, MSS 1436.
- GRE over IPsec with NAT-T: the worst case above is 24 + 65 = 89 (GCM) or 24 + 81 = 105 bytes in tunnel-mode CBC, so a tunnel MTU of 1400 with MSS 1360 is a comfortable round figure, not a computed one.
- WireGuard: MTU 1420 (the Linux module's default is 1500 minus 80, i.e. sized for an IPv6 outer header), MSS 1380 for inner IPv4.
- VXLAN in a DC: raise underlay MTU to 9216 so 1500-byte tenant frames fit, or to at least 1550.

## Options
1. Increase underlay MTU (best in DCs and private WANs you control).
2. Lower tunnel MTU and clamp MSS (internet tunnels).
3. Rely on PMTUD (fragile: ICMP filtered, GRE/IPsec PMTUD bugs).
UDP and other non-TCP protocols do not benefit from MSS clamping; size their payloads or ensure
fragmentation works.

## Verify
```
ping -M do -s 1372 10.20.0.1          # Linux: 1372 + 28 = 1400-byte packet, DF set
ping -f -l 1372 10.20.0.1             # Windows
```
- [ ] The largest DF ping that succeeds equals the designed inner MTU.
- [ ] A bulk TCP transfer through the tunnel reaches expected throughput with no fragments in a
  capture (`ip.flags.mf == 1 || ip.frag_offset > 0`; this filter was tested in tshark on a fragmented pcap).
