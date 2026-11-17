---
id: computing-software.systems-network-administration.network-design.mtu-mss-and-pmtud-black-holes
name: mtu-mss-and-pmtud-black-holes
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, osi-model, encapsulation, mtu, mss, fragmentation, pmtud, pmtud-black-hole, tcp-mss-clamping, df-bit, icmp-fragmentation-needed, packet-too-big, tunnel-overhead, jumbo-frames, ping-df-bit]
level: practitioner
status: verified
description: "Plan and debug MTU end to end: header overheads for VLAN/GRE/IPsec/VXLAN, MSS clamping, PMTUD and the ICMP it needs, finding black holes with DF pings, and jumbo-frame rollouts."
sources:
  - https://datatracker.ietf.org/doc/html/rfc1191
  - https://datatracker.ietf.org/doc/html/rfc8201
  - https://www.cisco.com/c/en/us/support/docs/ip/generic-routing-encapsulation-gre/25885-pmtud-ipfrag.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# MTU, MSS and PMTUD black holes

## Overheads to budget
| Encapsulation | Adds (bytes) |
|---|---|
| 802.1Q tag | 4 (Layer 2, does not reduce IP MTU on modern switches) |
| PPPoE | 8 (IP MTU 1492) |
| GRE | 24 |
| IPsec ESP tunnel mode | 54-57 (AES-GCM), 58-73 (AES-CBC + HMAC-SHA1-96); +8 with NAT-T |
| GRE over IPsec (ESP tunnel mode) | 78-97 (24 + the ESP figure above, before NAT-T) |
| VXLAN | 50 (underlay must carry 1550+) |
| WireGuard | 60 (IPv4) / 80 (IPv6) |
TCP MSS = IP MTU - 40 (IPv4+TCP headers) or - 60 for IPv6.

## Path MTU discovery
Hosts send with DF set; a router that cannot forward replies **ICMP type 3 code 4
"fragmentation needed"** (IPv6: ICMPv6 type 2 Packet Too Big) with the next-hop MTU; the
sender lowers its packet size. If that ICMP is filtered (firewall "block all ICMP"), large
packets vanish silently: a **PMTUD black hole**.

Symptoms: ping works, SSH login works, but web pages/hang after headers, file copies stall,
TLS handshakes with large certificates fail, VPN users can reach some sites only.

## Find it
```
# Linux: largest DF ping that passes (payload + 28 = IP packet size)
ping -M do -s 1472 <dest>     # 1500 total
ping -M do -s 1400 <dest>
# Windows
ping -f -l 1472 <dest>
# tracepath shows the hop where PMTU drops
tracepath <dest>
```
Binary-search the payload until it passes; the result + 28 is the path MTU. Wireshark:
`icmp.type==3 && icmp.code==4` or `icmpv6.type==2` to see whether PTB messages exist at all.

## Fix
1. Allow ICMP type 3 code 4 / ICMPv6 type 2 through every firewall (never block them).
2. Clamp TCP MSS at the tunnel edge so TCP never sends oversize segments:
   most router and firewall OSes have a per-interface MSS clamp (look up the command for your platform);
   Linux `iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu`
   (netfilter's iptables-extensions page gives exactly this rule; clamp-mss-to-pmtu uses path MTU - 40 for IPv4, - 60 for IPv6 and misbehaves with asymmetric routes).
3. Set the tunnel interface IP MTU (e.g. 1400, or the computed value above) so the router fragments or signals correctly.
4. Raise underlay MTU where you own it (VXLAN fabrics: 9216 on switch ports).
MSS clamping does nothing for UDP (DNS over large responses, QUIC, some VPNs): those need
working PMTUD or application-level size limits.

## Jumbo frames
Only inside a domain you control end to end (storage, vMotion, VXLAN underlay). Every hop,
including hypervisor vSwitches and NICs, must match; a single 1500-byte hop creates a black hole
for 9000-byte packets. Test with `ping -M do -s 8972`.

## Verify
- [ ] DF ping at the expected path MTU succeeds end to end; one byte larger fails with an ICMP reply (not a timeout).
- [ ] TCP SYNs across tunnels show the clamped MSS in Wireshark (`tcp.options.mss_val`).
