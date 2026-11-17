---
id: computing-software.systems-network-administration.wireshark.icmpv6-nd-and-ra-analysis
name: icmpv6-nd-and-ra-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, icmpv6-analysis, neighbor-discovery, router-advertisement, dad, slaac, rogue-ra]
level: practitioner
status: verified
description: "Diagnose IPv6 addressing and reachability from captures: Router Advertisement flags and prefixes, NS/NA resolution, duplicate address detection, and rogue RAs."
sources:
  - https://www.rfc-editor.org/rfc/rfc4861
  - https://www.rfc-editor.org/rfc/rfc4862
  - https://www.wireshark.org/docs/dfref/i/icmpv6.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ICMPv6 ND and RA analysis

## Message types
| Type | Name | Filter |
|---|---|---|
| 133 | Router Solicitation | `icmpv6.type == 133` |
| 134 | Router Advertisement | `icmpv6.type == 134` |
| 135 | Neighbor Solicitation | `icmpv6.type == 135` |
| 136 | Neighbor Advertisement | `icmpv6.type == 136` |
| 137 | Redirect | `icmpv6.type == 137` |
| 2 | Packet Too Big (PMTUD) | `icmpv6.type == 2` |

## Router Advertisements: why hosts got (or did not get) addresses
Check in each RA:
- `icmpv6.nd.ra.flag.m` (Managed: use DHCPv6 for addresses) and `.o` (Other: DHCPv6 for DNS etc).
- Prefix Information option: `icmpv6.opt.prefix`, `A` flag (autonomous: SLAAC allowed), `L` flag,
  valid/preferred lifetimes. A=0 means no SLAAC address from that prefix.
- Router lifetime: 0 = not a default router (RFC 4861).
- RDNSS option (RFC 8106, `icmpv6.opt.rdnss`) for DNS without DHCPv6.
```
icmpv6.type == 134 && icmpv6.nd.ra.router_lifetime == 0
icmpv6.type == 134 && eth.src != 00:00:5e:00:02:01     # RAs not from the expected router MAC
```

## Rogue RAs
More than one RA source MAC on a segment, unexpected prefixes, or high-preference RAs from a host:
```
icmpv6.type == 134
```
Statistics > Endpoints filtered on that shows every RA sender. Hosts that forward or bridge traffic (internet sharing, VM bridges) can start sending RAs by
accident. Fix with RA Guard (RFC 6105) on the switch.

## NS/NA (address resolution)
NS to the solicited-node multicast `ff02::1:ffXX:XXXX`, NA unicast reply with target link-layer
address. NS repeated with no NA = neighbour down or filtering (ACL dropping ICMPv6, or MLD snooping
dropping solicited-node multicast).

## Duplicate Address Detection
NS from `::` (unspecified source) for the host's tentative address. An NA answering it means a
duplicate: the host will not use the address (`Duplicate address detected` in OS logs).
```
icmpv6.type == 135 && ipv6.src == ::
```

## Verify
- [ ] Exactly the expected routers send RAs, with flags/prefixes matching the design, and NS for
  the gateway get NA replies.

## Checked (2026-10-22)
- Built RA, NS, NA and RS packets with scapy (RA from the expected MAC with M=0/O=1 and prefix 2001:db8:1::/64 A=1 L=1, a rogue RA from 02:aa:bb:cc:dd:ee with M=1 and lifetime 0, an NS from `::`) and ran on Wireshark 4.4.1: `icmpv6.type == 134 && icmpv6.nd.ra.router_lifetime == 0` returned only the rogue RA (flags m True, o False), `icmpv6.type == 134 && eth.src != 00:00:5e:00:02:01` returned the rogue source MAC, `icmpv6.type == 135 && ipv6.src == ::` matched the DAD NS, `-z endpoints,eth` filtered to RAs listed both senders; `icmpv6.opt.prefix`, `.flag.a`, `.flag.l`, `.valid_lifetime`, `.preferred_lifetime`, `icmpv6.opt.rdnss`, `icmpv6.nd.ra.flag.m/.o` exist in `tshark -G fields` and decoded as injected (A=True, valid lifetime 2592000).
- RFC 4861: Router Lifetime 0 means the router is not a default router; RFC 4862: DAD NS uses the unspecified source and the solicited-node destination; RFC 6105 (RA Guard) and RFC 8106 (RDNSS) exist as cited. ICMPv6 type numbers 133-137 and 2 are standard (RFC 4443/4861). 00:00:5e:00:02:01 is the VRRPv3 IPv6 virtual MAC pattern (00-00-5E-00-02-VRID); it is only the skill's example router.
- Not tested: Packet Too Big, MLD snooping or ACL causes of repeated NS (interpretation).
