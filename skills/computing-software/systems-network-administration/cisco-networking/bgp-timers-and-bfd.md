---
id: computing-software.systems-network-administration.cisco-networking.bgp-timers-and-bfd
name: bgp-timers-and-bfd
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, bgp, bgp-timers, bfd, fast-external-fallover, next-hop-tracking, convergence]
level: practitioner
status: docs-checked
description: "Speed up BGP failure detection: keepalive/hold negotiation, fast-external-fallover, BFD for eBGP sessions, and next-hop tracking, without destabilising sessions."
sources:
  - https://www.rfc-editor.org/rfc/rfc4271#section-4.2
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/command/irg-cr-book/bgp-m1.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/command/irg-cr-book/bgp-a1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP timers and BFD

Default keepalive is 60 s and hold time 180 s (Cisco `neighbor timers` reference). When a peer dies
behind a switch or provider handoff (link stays up), you blackhole for up to the hold time.

## Timers
```
router bgp 65001
 timers bgp 10 30                       ! global: keepalive hold
 neighbor 203.0.113.1 timers 10 30      ! per neighbour
```
Syntax is `neighbor [ip-address | peer-group-name] timers keepalive holdtime [min-holdtime]`. Hold
time is negotiated: each side uses the smaller of its configured value and the one received
(RFC 4271 4.2), and an accepted hold time must be zero or at least three seconds. Very low values
stress the control plane.

`show ip bgp neighbors 203.0.113.1` shows "hold time is ..., keepalive interval is ... seconds".

## Directly connected eBGP: interface-down detection
`bgp fast-external-fallover` resets the session immediately when the link to a directly connected
external peer goes down. If it is disabled, BGP waits for the hold timer to expire. It only helps
when the link actually drops.

## BFD
```
interface Gi0/1
 bfd interval 50 min_rx 50 multiplier 3
router bgp 65001
 neighbor 203.0.113.1 fall-over bfd
```
The BFD interval, min_rx and multiplier are set on the interface; `neighbor ... fall-over bfd` ties
the BGP session to BFD. Both sides must run BFD, so ask your ISP whether they support it on the
session. Multihop BFD for iBGP loopbacks needs a separate BFD template; see the Cisco BFD
configuration guide.

## Next-hop tracking (iBGP)
`bgp nexthop trigger delay seconds` (range 0 to 100, default 5) sets the delay between checks on
updated next-hop routes. Next-hop tracking is enabled by default for IPv4 and VPNv4. Cisco notes
the default of 5 s suits a fast-tuned IGP and suggests 20 s or more for a slowly converging IGP;
unstable IGP peers can introduce instability to BGP, so dampen them.

## Gotchas
- Very short hold timers plus a full table plus a CPU spike during convergence means late
  keepalives, session resets and more churn. Prefer BFD with moderate BGP timers.
- Graceful restart interacts with BFD: decide whether a control-plane restart should be hidden (GR)
  or trigger failover (BFD) and test both.

## Verify
- [ ] Simulated far-end failure (drop BFD/BGP at the far side with the link up) fails over within
  your target time.

## Checked
2026-10-31. Confirmed in the Cisco BGP command reference (`neighbor timers` defaults 60/180 and
syntax; `bgp fast-external-fallover` behaviour; `bgp nexthop trigger delay` range, default 5 and
tuning advice; `neighbor fall-over bfd` with `bfd interval 50 min_rx 50 multiplier 3`) and RFC 4271
4.2 (smaller hold time, zero or at least three seconds). Removed: one-third keepalive rule,
"3/9 on IXPs", hold time 0 disabling keepalives, the multihop BFD template and map lines, the
`show bfd neighbors` verify lines and the "about a second" failover figure, which no fetched page confirms.
Method: documentation only; no commands were run.
