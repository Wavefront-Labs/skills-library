---
id: computing-software.systems-network-administration.cisco-networking.bgp-communities
name: bgp-communities
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, bgp, bgp-community, no-export, no-advertise, large-community, blackhole, community-list, send-community]
level: practitioner
status: docs-checked
description: "Tag and act on BGP communities on IOS: send-community, new-format, well-known no-export/no-advertise, and the RFC 7999 blackhole community."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/28784-bgp-community.html
  - https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/26634-bgp-toc.html
  - https://www.rfc-editor.org/rfc/rfc1997
  - https://www.rfc-editor.org/rfc/rfc7999
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP communities

The community attribute is a transitive, optional attribute used to group destinations and apply routing
decisions (accept, prefer, redistribute) to the group without matching prefixes.

## Enable
```
ip bgp-community new-format
router bgp 64512
 neighbor 10.255.0.2 send-community both
```
- By default IOS shows a community as a decimal number (for example `6553620`); `ip bgp-community new-format`
  displays and configures `AA:NN` (for example `100:20`).
- Setting a community does not send it: a neighbor receives it only if `neighbor ... send-community` is configured.
  The command reference syntax is `neighbor {ip-address | ipv6-address | peer-group-name} send-community
  [both | standard | extended]`.

## Set and match
```
route-map FROM-ISP-A permit 10
 set community 64512:100 additive
ip community-list 1 permit 64512:100
route-map TO-ISP-B deny 10
 match community 1
route-map TO-ISP-B permit 20
```
- `set community community-number [additive] [well-known-community]`: without `additive` the new value replaces any
  existing community, with it the value is added.
- `match community` in a route map tests against an `ip community-list`; the Cisco examples use numbered lists such
  as `ip community-list 1 permit 100:300`.

## Well-known
| Community | Effect |
|---|---|
| no-export (65535:65281, 0xFFFFFF01) | do not advertise outside the AS (or confederation boundary); IOS: do not advertise to eBGP peers |
| no-advertise (65535:65282, 0xFFFFFF02) | do not advertise to any peer, internal or external |
| local-as | used in confederation scenarios to stop advertisement outside the local AS |
| internet | advertise to the Internet community; every router belongs to it |
| BLACKHOLE (65535:666, 0xFFFF029A, RFC 7999) | request that traffic to the prefix be discarded (the low-order 666 is a commonly used value) |

Provider-specific action communities (prepend, local preference, remotely triggered blackhole) are defined in each
provider's own documentation; do not assume a value.

## Verify
```
show ip bgp 10.6.0.0
show ip bgp community 100:20
```
- [ ] The `Community:` line appears on the receiving router (send-community needed at every hop that must pass it on).
- [ ] After `ip bgp-community new-format`, values display as `AA:NN`.

## Checked
Date: 2026-11-07. Cisco documents 28784 (BGP community lab, about 24k characters) was read for its configurations and
outputs; 26634 (BGP case studies, about 127k, added as a source) was read in the Community Attribute section and the
no-export/additive examples (lines 868-930 and 1097-1126), not cover to cover. RFC 1997 (well-known values) and
RFC 7999 (BLACKHOLE value) were searched for the values. The BGP command reference pages were searched for the
`send-community` syntax and `show ip bgp community`.
Confirmed: new-format behaviour, decimal default, send-community requirement and its keywords, `set community ...
[additive] [well-known]`, numbered community-list and `match community`, well-known meanings and values, `Community:` display.
Removed: `ip community-list standard NAME` (page uses numbered lists), the ISP action community and RTBH static-route
and route-map recipe (not on the pages), `show ip bgp neighbors ... advertised-routes` Verify line, and the
`address-family ipv4 unicast` wrapper.
Method: documentation only; no commands were run.
