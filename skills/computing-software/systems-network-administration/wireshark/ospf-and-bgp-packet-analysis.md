---
id: computing-software.systems-network-administration.wireshark.ospf-and-bgp-packet-analysis
name: ospf-and-bgp-packet-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, ospf-analysis, bgp-analysis, routing-protocols, protocol-analysis]
level: practitioner
status: verified
description: "Read OSPF and BGP in Wireshark: hello parameter mismatches, adjacency states, LSA flooding, BGP OPEN capabilities, NOTIFICATION codes and UPDATE contents."
sources:
  - https://www.rfc-editor.org/rfc/rfc2328
  - https://www.rfc-editor.org/rfc/rfc4271
  - https://www.wireshark.org/docs/dfref/o/ospf.html
  - https://www.wireshark.org/docs/dfref/b/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPF and BGP packet analysis

## OSPF (IP protocol 89)
```
ospf
ospf.msg == 1                # Hello; 2 DBD; 3 LSR; 4 LSU; 5 LSAck
ospf.hello.hello_interval
ospf.hello.router_dead_interval
ospf.area_id
```
Adjacency won't form? Compare two Hellos side by side; RFC 2328 drops a Hello whose network mask, HelloInterval or
RouterDeadInterval differs (the mask is not compared on point-to-point or virtual links), and area ID, authentication
and the E bit (`ospf.v2.options.e`, stub area capability) must also match. MTU is carried in DBD
(`ospf.db.interface_mtu`): a DBD advertising an MTU larger than the receiver can accept is rejected, so the
adjacency stalls in ExStart/Exchange.
Repeated LSUs for the same LSA with rising sequence numbers are worth correlating with link state.

## BGP (TCP 179)
```
bgp
bgp.type == 1                # OPEN; 2 UPDATE; 3 NOTIFICATION; 4 KEEPALIVE; 5 ROUTE-REFRESH
bgp.notify.major_error
bgp.update.path_attribute.as_path_segment.as4   # as2 for 2-byte AS_PATH; there is no plain `.as` field
```
- OPEN: My AS, hold time, BGP identifier, capabilities (4-byte AS, multiprotocol AFI/SAFI, route
  refresh, add-path, graceful restart). A required capability the peer lacks = NOTIFICATION 2/7 (Unsupported Capability, RFC 5492; a capability a speaker does not
  recognise must just be ignored).
- NOTIFICATION codes: 2/2 bad peer AS, 4/0 hold timer expired, 6/x cease (6/2 admin shutdown,
  6/4 admin reset, 6/1 maximum prefixes reached).
- UPDATE: withdrawn routes, path attributes (ORIGIN, AS_PATH, NEXT_HOP, MED, LOCAL_PREF,
  COMMUNITIES) and NLRI.

## Tips
- TCP MD5 (`tcp.options.md5`, RFC 2385): a failed digest check drops the segment and must produce no response, so a
  wrong key looks like SYNs ignored with no RST. TCP-AO is the successor (RFC 5925).
- Use Decode As if BGP runs on another port (route servers, test labs).

## Verify
- [ ] Hello parameters match on both sides and BGP reaches steady KEEPALIVEs (RFC 4271: a reasonable maximum is one third of the hold time).

## Checked
Run with TShark 4.4.1 on generated OSPF Hello packets (hello 10 s/dead 40 s in area 0.0.0.0 versus 30/120 in
0.0.0.1) and a DBD with MTU 1400, and on a BGP session carrying OPEN (AS 65001, hold 90), UPDATE (AS_PATH 65001 65002)
and NOTIFICATION 6/2: `ospf`, `ospf.msg == 1`, `ospf.area_id`, the interval and MTU fields, `bgp`, `bgp.type`,
`bgp.notify.major_error` all matched; `bgp.update.path_attribute.as_path_segment.as` does not exist (as2/as4 do).
BGP and OSPF message-type and notification names read from `tshark -G values` (Cease subcodes 1, 2, 4; OPEN subcodes 2
and 7); RFC 4271, 4486, 5492, 2385 and 2328 text fetched for the keepalive third, cease subcodes, capability
subcode, MD5 behaviour, Hello checks, E bit and MTU rejection. Convergence and flap interpretations were removed or reduced to pointers.
