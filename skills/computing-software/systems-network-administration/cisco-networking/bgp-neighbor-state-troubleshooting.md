---
id: computing-software.systems-network-administration.cisco-networking.bgp-neighbor-state-troubleshooting
name: bgp-neighbor-state-troubleshooting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, bgp, bgp-neighbor, bgp-states, idle, active, opensent, established, ebgp-multihop, update-source]
level: practitioner
status: draft
description: "Bring up a BGP session on IOS and diagnose it by state (Idle, Connect, Active, OpenSent, OpenConfirm): TCP 179, update-source, multihop, ASN and auth mismatches."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/22166-bgp-trouble-main.html
  - https://www.rfc-editor.org/rfc/rfc4271
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BGP neighbour states and troubleshooting

BGP rides TCP 179. `show ip bgp summary` shows the state in the `State/PfxRcd` column; a
number there means Established.

| State stuck in | Meaning | Usual cause |
|---|---|---|
| Idle | not trying | no route to the peer, `shutdown`, or Idle (Admin)/(PfxCt) after max-prefix |
| Connect / Active | TCP not completing | ACL/firewall on 179, wrong neighbor IP, peering from wrong source |
| OpenSent / OpenConfirm | TCP up, OPEN rejected | wrong remote-as, bad router-id/duplicate, hold time, capability mismatch |
| flapping Established | session resets | MD5 password mismatch, MTU (large UPDATEs dropped), hold timer expiry |

## iBGP over loopbacks
```
router bgp 64512
 neighbor 10.255.0.2 remote-as 64512
 neighbor 10.255.0.2 update-source Loopback0     ! source must match peer's neighbor IP
```
Peer must have a route to your loopback (IGP); without `update-source` the TCP SYN comes from
the egress interface IP and the peer refuses it (stays Active).

## eBGP not directly connected
```
 neighbor 192.0.2.9 ebgp-multihop 2      ! default TTL 1 for eBGP
 neighbor 192.0.2.9 update-source Loopback0
 ! or: neighbor 192.0.2.9 disable-connected-check (same-link loopbacks)
```

## Diagnose
```
show ip bgp summary
show ip bgp neighbors 203.0.113.1 | include state|Last reset|hold|Local host|Foreign host
show tcp brief | include 179
debug ip bgp 203.0.113.1 events        ! briefly, with logging buffered
```
`Last reset` text tells you directly: "Peer closed the session", "BGP Notification sent,
hold time expired", "bad AS". `%TCP-6-BADAUTH` in the log = MD5 mismatch or missing.
Telnet test: `telnet 203.0.113.1 179 /source-interface Lo0` proves the TCP path.

## Verify
- [ ] Established with expected PfxRcd; `Last reset` older than the change window.
- [ ] Session survives a 3x hold-time interval without resets.
