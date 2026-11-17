---
id: computing-software.systems-network-administration.cisco-networking.conditional-debugging-safely
name: conditional-debugging-safely
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, debug, ios-troubleshooting, conditional-debug, debug-condition, debug-ip-packet, undebug-all, logging-buffered, radioactive-tracing, show-debugging]
level: practitioner
status: draft
description: "Run IOS debugs without taking down the box: buffer-only logging, debug conditions by interface/IP/MAC, ACL-limited debug ip packet, timed undebug, and IOS XE radioactive tracing."
sources:
  - https://www.cisco.com/c/en/us/support/docs/dial-access/integrated-services-digital-networks-isdn-channel-associated-signaling-cas/10374-debug.html
  - https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-xe-16/218226-collect-radioactive-traces-on-cisco-ios.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conditional debugging, safely

Debugs run at high priority in the CPU. On a busy router, `debug ip packet` without limits can
hang the device. Prepare, limit, time-box.

## 1. Prepare output handling
```
logging buffered 2000000 debugging    ! big buffer, catches level 7
no logging console                    ! console at 9600 baud is the usual cause of hangs
logging monitor informational         ! keep debugs off the VTY too, read from buffer
service timestamps debug datetime msec localtime
```
Open a **second** SSH session first so you can `undebug all` if the first one is swamped.

## 2. Limit scope
```
debug condition interface GigabitEthernet0/0/1    ! many debugs honour it (PPP, crypto, some IP)
debug condition ip 10.20.30.40
debug condition mac-address 0011.2233.4455        ! wireless / 802.1X
show debug condition
!
ip access-list extended DBG
 permit icmp host 10.20.30.40 host 10.0.0.1
 permit icmp host 10.0.0.1 host 10.20.30.40
debug ip packet DBG detail                         ! only matching packets
```
`debug ip packet` only sees **process-switched** (punted) traffic, not CEF-switched transit
traffic. For transit packets use Embedded Packet Capture instead.

## 3. Time-box
```
reload in 15        ! extreme cases on remote boxes; or:
debug ip ospf adj
! ... reproduce ...
undebug all         ! u all
show debugging      ! confirm nothing left on
show logging | b OSPF
```
IOS XE: `debug ... ` plus `request platform software trace ...` for platform components.

## IOS XE radioactive tracing (no CPU risk)
Traces are always collected at low cost; RA tracing raises verbosity for one MAC/IP only:
```
debug wireless mac 0011.2233.4455            ! 9800 17.x: starts RA tracing for one client/AP
no debug wireless mac 0011.2233.4455         ! stops it and writes ra_trace_MAC_... to bootflash:
show logging profile wireless filter mac 0011.2233.4455 to-file bootflash:ra.txt   ! decode always-on traces
```
On the 9800 GUI: Troubleshooting > Radioactive Trace, add MAC, start, reproduce, generate.

## Gotchas
- `debug all` = outage. Never.
- Some debugs ignore conditions; read the command reference or test on a lab box.
- Clear conditions when done: `undebug condition all` or `no debug condition all`.

## Verify
- [ ] `show debugging` empty and `show debug condition` cleared at the end.
- [ ] CPU (`show processes cpu history`) showed no spike during the session.
