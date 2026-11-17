---
id: computing-software.systems-network-administration.cisco-networking.eigrp-stub-and-stuck-in-active
name: eigrp-stub-and-stuck-in-active
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, eigrp, eigrp-stub, stuck-in-active, sia, query-scoping, active-timer, hub-and-spoke, dual]
level: advanced
status: docs-checked
description: "Keep EIGRP queries bounded: stub routing on spokes, what the stub keywords advertise, and diagnosing DUAL-3-SIA neighbour resets."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/13676-18.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_eigrp/configuration/xe-16/ire-xe-16-book/ire-eigrp-stub-rtg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EIGRP stub routing and stuck-in-active

## Why SIA happens
A route is stuck in active (SIA) when an EIGRP router has not received a reply to a query from one or more neighbours
within the time allotted (approximately 3 minutes; the SIA timer is a little over 3 minutes by default). EIGRP then
clears the neighbours that did not reply and logs a `%DUAL-3-SIA` error for the route that went active. Routing to
other destinations is not affected while the route is active. Typical causes named by Cisco: a flapping interface, a
configuration change, dialup clients, an unresponsive router, a routing loop of queries, or a neighbour that never
answers (for example hellos from a subnet the peer does not recognise).

## Stub routing (spokes)
```
router eigrp 1
 network 10.0.0.0
 eigrp stub connected static
```
Syntax: `eigrp stub [receive-only] [leak-map name] [connected] [static] [summary] [redistributed]`; the same command
is used under the address family in named mode.
- By default a stub shares connected and summary routes with its neighbours. `connected static` advertises
  connected and static routes only (summary routes are not sent); `receive-only` sends no connected, summary or static
  routes; `redistributed` advertises routes from other protocols and autonomous systems; `leak-map name` references a
  leak map for routes that would otherwise be suppressed.
- Configure only the remote (spoke) device as the stub, not the distribution device.
- The stub sends a special peer information packet reporting its stub status. A neighbour that receives it does not
  query the stub for any routes, and the stub answers any query it does get with "inaccessible". The distribution
  device answers queries on behalf of the stub.
- Without stub routing, a lost route can make the distribution device query the remote device even if routes are
  summarised, and a WAN problem between them can cause SIA and instability elsewhere.
- Use stub only on devices through which core transit traffic should not flow. A stub should have no EIGRP neighbours
  other than distribution devices; ignoring this causes undesirable behaviour.
- On multiaccess interfaces (ATM, Gigabit Ethernet, Frame Relay, ISDN PRI, X.25) stub is supported only when all
  devices on the interface except the hub are stubs.

## Diagnose an SIA
```
show ip eigrp neighbors        ! from both ends
show log | in DUAL
show ip eigrp topology active
```
- `show ip eigrp topology active` lists routes in the active state; it is normal for some to appear, so look at routes
  active for longer than one minute. The `r` code is "Reply status".
- Because the timer is a little over 3 minutes, track the unanswered query hop by hop to the router that is not
  replying, while the route is still active.
- `DUAL-5-NBRCHANGE` messages appear only when `eigrp log-neighbor-changes` is configured under the EIGRP process;
  Cisco recommends it on all EIGRP routers when troubleshooting SIA.

## Verify
- [ ] `show ip eigrp neighbors detail` on the distribution device shows the stub status of the spoke on its last line.
- [ ] No `%DUAL-3-SIA` messages appear in `show log | in DUAL`.

## Checked
Date: 2026-11-07. Both pages were read in full: the DUAL-3-SIA troubleshooting page 13676-18 (about 16k characters)
and the IOS XE EIGRP Stub Routing chapter (about 25k).
Confirmed: SIA definition, 3-minute timing, neighbour clearing, the diagnostic commands and `log-neighbor-changes`
note, stub purpose, query behaviour, `eigrp stub` syntax and keyword descriptions, the default of connected and
summary, the stub-only-on-stubs caution, the multiaccess note, `show ip eigrp neighbors detail` for stub status.
Removed (not on the pages): the SIA-query/SIA-reply mechanism at half the active timer, the named-mode `af-interface`
and `summary-address` summarisation recipe, "Q Cnt" and retransmit checks, the
"Stub Peer Advertising" wording, the one-week log check and the claim that stub is the single biggest stability win.
Method: documentation only; no commands were run.
