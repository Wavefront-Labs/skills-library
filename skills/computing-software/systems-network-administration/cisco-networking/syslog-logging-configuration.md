---
id: computing-software.systems-network-administration.cisco-networking.syslog-logging-configuration
name: syslog-logging-configuration
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, syslog, logging, syslog-severity, logging-trap, logging-buffered, logging-console, terminal-monitor, logging-host, logging-source-interface, logging-facility, logging-rate-limit, show-logging]
level: practitioner
status: draft
description: "Configure IOS logging: severity levels 0-7, buffered vs console vs monitor, remote syslog hosts with source interface/VRF/TCP, rate limiting and reading the buffer."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/esm/configuration/xe-16/esm-xe-16-book/esm-sys-msg-log.html
  - https://datatracker.ietf.org/doc/html/rfc5424
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Syslog and logging configuration on IOS

## Severity levels
| Level | Keyword | Example |
|---|---|---|
| 0 | emergencies | system unusable |
| 1 | alerts | temperature critical |
| 2 | critical | hardware failure |
| 3 | errors | interface errors, `%LINK-3-UPDOWN` |
| 4 | warnings | `%SPANTREE-4`, config warnings |
| 5 | notifications | `%LINEPROTO-5-UPDOWN`, `%SYS-5-CONFIG_I` |
| 6 | informational | ACL log hits, `%SEC-6` |
| 7 | debugging | debug output |
Setting a level sends that level **and everything more severe** (lower number). Mnemonic:
"Every Awesome Cisco Engineer Will Need Ice-cream Daily".

## Destinations
```
no logging console                    ! or 'logging console critical': console logging at 9600 baud can stall the CPU
logging buffered 64000 informational  ! local RAM buffer, size in bytes
logging monitor informational         ! VTY sessions that run 'terminal monitor'
logging trap informational            ! remote hosts
logging source-interface Loopback0
logging host 10.0.0.40
logging host 10.0.0.41 transport tcp port 601    ! reliable delivery where the collector supports it
logging host 10.0.0.42 vrf Mgmt-vrf
logging facility local6               ! lets the collector route network logs
logging rate-limit 100 except errors  ! cap messages/s, but never drop errors and worse
```
Add timestamps and sequence numbers (see clock-timezone-and-log-timestamps).

## Viewing
```
show logging                          ! status per destination + buffer contents
show logging | i %LINK|%LINEPROTO
terminal monitor                      ! see logs live in an SSH session; 'terminal no monitor' to stop
clear logging
```
On IOS XE, `show logging onboard` and `show logging process` / btrace logs hold platform
detail beyond syslog.

## Gotchas
- Debug output goes to every destination at level 7: before `debug` set `logging buffered 7`
  and keep console/monitor/trap at 6 or lower, or you can flood the collector and CPU.
- UDP syslog is lossy and unauthenticated; for compliance use TCP or TLS (`logging host ...
  transport tls profile` on IOS XE) and sequence numbers.
- Logs from the wrong source IP get dropped by collector allow-lists: always set
  `logging source-interface`.
- `logging discriminator` can filter specific noisy messages (e.g. per-port LINK on access ports).

## Verify
- [ ] `show logging` shows the trap level and hosts with increasing "messages logged" counters.
- [ ] `send log 6 "syslog test"` arrives at the collector from the loopback IP.
- [ ] Console logging is off or at critical.
