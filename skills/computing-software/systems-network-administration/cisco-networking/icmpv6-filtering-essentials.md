---
id: computing-software.systems-network-administration.cisco-networking.icmpv6-filtering-essentials
name: icmpv6-filtering-essentials
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ipv6, icmpv6-filtering, ipv6-acl, neighbor-discovery, pmtud, rfc4890, packet-too-big, firewall]
level: practitioner
status: docs-checked
description: "Which ICMPv6 types a firewall or ACL must pass, normally pass, can ignore on-link, or should drop, per RFC 4890, with Packet Too Big and Neighbor Discovery."
sources:
  - https://datatracker.ietf.org/doc/html/rfc4890
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ICMPv6 filtering (RFC 4890)

RFC 4890 is informational. It separates transit traffic (passing through the firewall, section 4.3) from local
configuration traffic (addressed to the firewall or router itself, section 4.4).

## Transit: must not be dropped (4.3.1)
| Type | Name | Note |
|---|---|---|
| 1 | Destination Unreachable | all codes |
| 2 | Packet Too Big | vital to Path MTU Discovery |
| 3 | Time Exceeded | code 0 only |
| 4 | Parameter Problem | codes 1 and 2 only |
| 128, 129 | Echo Request, Echo Response | needed for Teredo to site nodes; the RFC says IPv6 echo request need not be filtered because scanning risk is much lower than in IPv4 |

## Transit: normally should not be dropped (4.3.2)
Time Exceeded code 1, Parameter Problem code 0, and the Mobile IPv6 types 144-147 (Home Agent Address Discovery and
Mobile Prefix messages). A site can use more selective rules depending on mobility use.

## Transit: dropped anyway, no special action (4.3.3)
Link-local scope messages that must never leave the link:
- Router Solicitation 133, Router Advertisement 134, Neighbor Solicitation 135, Neighbor Advertisement 136, Redirect
  137, Inverse ND 141 and 142: must arrive with hop limit 255.
- MLD Query 130, Report 131, Done 132, Report v2 143: must have a link-local source.
- SEND certificate path 148 and 149 (hop limit 255); Multicast Router Discovery 151-153 (link-local source, hop limit 1).

Conforming routers do not forward link-local packets, and receivers check hop limit 255 and link-local source, so no
extra rules are needed. You may still add rules for insurance, logging or attack monitoring. A firewall that is a
transparent bridge must pass these types because the two sides form one logical link. An end-host firewall needs to pass
only those addressed to the host.

## Transit: define a policy (4.3.4)
- Seamoby experimental type 150: transit sites must pass it; end sites decide.
- Unallocated error types (5-99, 102-126): transit sites must pass all error types; end sites weigh a small covert
  channel and DoS risk.
- Unallocated informational types (154-199, 202-254): receivers silently discard them; transit sites must pass them;
  end sites either allow all or drop all. If you drop unallocated types, review the list when IANA allocates new ones.

## Transit: drop unless there is a good case (4.3.5)
Node Information Query and Response 139 and 140; Router Renumbering 138 (explicitly filter it at site boundaries if
unique local or global addresses become usable for it); experimental types 100, 101, 200, 201; extension types 127 and
255.

## Local traffic to the router or firewall (4.4)
- Must not be dropped (4.4.1): the same error and echo types as 4.3.1, plus ND types 133-136, 141, 142, MLD 130-132 and
  143, SEND 148 and 149, and MRD 151-153. Redirect (137) is the exception that needs an explicit policy decision
  (4.4.4).
- Normally should not be dropped (4.4.2): Time Exceeded code 1 and Parameter Problem code 0.
- A node that cannot do ND cannot participate in an IPv6 network, so a final deny in an interface ACL must not catch
  NS and NA.

## Packet Too Big (Appendix A.2)
Any node on the path that cannot forward a packet because of the next-hop MTU sends it. Routers cannot fragment, so
without it hosts keep sending oversize packets or assume congestion, and "parts of the Internet will become
inaccessible." If every packet is at most the guaranteed minimum MTU of 1280 octets and links match, Packet Too Big
might not be expected at the firewall and could be dropped; otherwise pass it.

## Platform behaviour
Some platforms add implicit permits for Neighbor Discovery ahead of the final implicit deny, and an explicit
final deny can remove that effect. The Cisco IPv6 ACL page was a 404 when checked, so confirm this and the ACL
syntax in your platform guide.

## Verify
- [ ] Large transfers across the filter work; a packet bigger than the next-hop MTU returns Packet Too Big.
- [ ] Neighbor Discovery works on every filtered interface (no incomplete neighbour entries).
- [ ] Rules distinguish transit from locally destined ICMPv6.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read RFC 4890 sections 4.1-4.4 (transit and local
recommendations, including the code-specific limits and link-local rules) and Appendix A.2 (Packet Too Big). Removed as
unconfirmed: all IOS ACL syntax and the implicit-permit listing (Cisco page 404), the rate-limit advice for echo, the
claim that border filters can drop 133-137 as a recommendation (the RFC says no action is needed), and the
troubleshooting and ping verify commands.
