---
id: computing-software.systems-network-administration.cisco-networking.radius-server-groups-and-dead-criteria
name: radius-server-groups-and-dead-criteria
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, aaa, radius, aaa-server-group, radius-dead-criteria, radius-deadtime, load-balancing, automate-tester]
level: practitioner
status: draft
description: "Build IOS XE RADIUS server groups with dead criteria, deadtime and automate-tester so failover to the next ISE node is fast and recovery is detected."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_usr_rad/configuration/xe-16/sec-usr-rad-xe-16-book/sec-rad-ov-ietf-attr.html
  - https://www.cisco.com/c/en/us/support/docs/security/identity-services-engine/213906-configure-radius-server-group-and-dead-c.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RADIUS server groups and dead criteria

## Config
```
radius server ISE-1
 address ipv4 10.0.0.31 auth-port 1812 acct-port 1813
 key <SECRET>
 automate-tester username probe-user probe-on      ! probes even when idle, detects recovery
radius server ISE-2
 address ipv4 10.0.0.32 auth-port 1812 acct-port 1813
 key <SECRET>
 automate-tester username probe-user probe-on
aaa group server radius ISE
 server name ISE-1
 server name ISE-2
 ip radius source-interface Vlan900
 deadtime 15                                       ! minutes a dead server is skipped
radius-server dead-criteria time 5 tries 3
radius-server timeout 5
radius-server retransmit 2
radius-server load-balance method least-outstanding  ! optional
aaa authentication dot1x default group ISE
aaa authorization network default group ISE
aaa accounting dot1x default start-stop group ISE
```

## How dead detection works
A server is marked dead when **both** criteria are met: no response for `time` seconds and
`tries` consecutive retransmissions failed. Then:
- With `deadtime`, the switch skips it for that many minutes and goes straight to the next server.
- Without deadtime, every new request still tries the dead server first (slow authentication for every user).
- automate-tester sends periodic dummy Access-Requests; an Access-Reject still proves the server
  is alive. `probe-on` marks it alive as soon as a probe succeeds.

## Timing math
Worst-case delay before failover per request = timeout x (retransmit + 1). 5 s x 3 = 15 s,
longer than many 802.1X supplicant timeouts. Keep timeout x attempts under ~10 s.

## Gotchas
- `ip radius source-interface` must be the address ISE has as a network device; else `Unknown NAD`.
- All servers dead: critical authentication (see dot1x-critical-auth) or local fallback for device admin.
- Mixed IOS/IOS XE syntax: legacy `radius-server host x key y` still works but use the `radius server` blocks.

## Verify
```
show aaa servers                        ! State: current UP/DEAD, dead time, platform state
show aaa dead-criteria radius 10.0.0.31
test aaa group ISE probe-user <PW> new-code
```
- [ ] Shut ISE-1: authentications succeed via ISE-2 within seconds; ISE-1 returns to UP when restored.
