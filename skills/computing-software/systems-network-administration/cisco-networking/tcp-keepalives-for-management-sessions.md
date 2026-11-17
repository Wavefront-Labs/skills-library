---
id: computing-software.systems-network-administration.cisco-networking.tcp-keepalives-for-management-sessions
name: tcp-keepalives-for-management-sessions
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, tcp-keepalives, service-tcp-keepalives-in, vty-hung-sessions, device-hardening, ssh-sessions]
level: practitioner
status: draft
description: "Clear hung VTY sessions with service tcp-keepalives-in/out, combine with exec-timeout and SSH timeouts, and identify stuck lines."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fundamentals/command/fundamentals-cr-book/fundamentals-s1.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TCP keepalives for management sessions

## Problem
A management session whose client vanished (laptop sleep, network cut, NAT timeout) can leave the
VTY line and TCP connection open. With 5-16 VTYs, a handful of orphans locks admins out, and the
orphaned session may hold a config lock or an authenticated shell.

## Fix
```
service tcp-keepalives-in      ! keepalives on incoming TCP sessions (SSH/telnet to the device)
service tcp-keepalives-out     ! for sessions the device initiates
line vty 0 15
 exec-timeout 10 0
ip ssh time-out 60             ! SSH negotiation timeout
```
IOS sends a keepalive after the session is idle (about 60 s), retries a few times, and closes the
TCP connection if the peer does not respond, freeing the line. exec-timeout handles idle but
alive sessions; keepalives handle dead peers.

## Find stuck sessions
```
show users                     ! line, user, idle time, location
show tcp brief                 ! TCB, local/remote address, state
show ssh
clear line vty 3               ! kill a specific line
clear tcp tcb 0x7F1234567890   ! kill a TCP connection by TCB
```

## Also
- Reserve one VTY for a management station: `line vty 15` with a tighter `access-class` so admins
  can always get in.
- Automation tools that open many sessions should close them; check `show users` after jobs.
- `ip tcp synwait-time 10` shortens half-open connection waits for outgoing sessions.

## Verify
- [ ] `show running-config | include keepalives` shows both services.
- [ ] Kill a client mid-session: line frees within a few minutes (`show users`).
