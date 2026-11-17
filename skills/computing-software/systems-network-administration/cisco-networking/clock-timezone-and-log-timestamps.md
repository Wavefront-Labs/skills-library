---
id: computing-software.systems-network-administration.cisco-networking.clock-timezone-and-log-timestamps
name: clock-timezone-and-log-timestamps
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ntp, clock-timezone, clock-summer-time, service-timestamps, log-timestamps, msec, localtime, show-timezone, utc, syslog, sequence-numbers]
level: practitioner
status: draft
description: "Make IOS timestamps usable for incident timelines: UTC vs local timezone, summer-time rules, service timestamps with msec and timezone, and pitfalls when correlating logs."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/bsm/configuration/xe-16/bsm-xe-16-book/bsm-time-calendar-set.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/esm/configuration/xe-16/esm-xe-16-book/esm-sys-msg-log.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clock timezone and log timestamps

## Decide: UTC everywhere (recommended)
Network devices in several countries, cloud logs and SIEM all correlate easiest in UTC. Leave
`clock timezone` unset (UTC) and let the SIEM display local time. If the organisation insists
on local time, configure it identically on every device.

## Local timezone (if required)
```
clock timezone AEST 10 0
clock summer-time AEDT recurring 1 Sun Oct 2:00 1 Sun Apr 3:00
! UK example
clock timezone GMT 0 0
clock summer-time BST recurring last Sun Mar 1:00 last Sun Oct 2:00
```
`recurring` without arguments uses US rules: always give the explicit dates outside the US.

## Timestamps on logs and debugs
```
service timestamps log datetime msec localtime show-timezone year
service timestamps debug datetime msec localtime show-timezone year
service sequence-numbers
```
- Default is `uptime` (e.g. `2w3d:`), useless for correlation: always change it.
- `localtime` uses the configured timezone (omit for UTC); `show-timezone` prints the zone so a
  reader cannot misinterpret; `msec` resolves events in the same second.
- `service sequence-numbers` numbers each message so gaps (dropped UDP syslog) are visible.

Example result:
```
000123: Oct 16 2026 09:14:03.512 AEDT: %LINEPROTO-5-UPDOWN: Line protocol on Interface Gi1/0/3, changed state to down
```
An asterisk before the time (`*Oct 16 ...`) means the clock is **not synchronised** (no NTP).
A dot (`.Oct 16`) means it was synchronised but lost sync.

## Check
```
show clock detail        ! source: NTP / user configuration / hardware calendar
show run | i timezone|summer-time|timestamps
```

## Gotchas
- Syslog servers add their own receive timestamp; if device and server zones differ you get
  double offsets in the SIEM. Parse the device timestamp, or use RFC 5424 with
  `logging host ... transport ... session-id`/`logging rfc5424` on newer IOS XE.
- Mixed `summer-time` rules across sites cause one-hour discrepancies twice a year.

## Verify
- [ ] Log lines show year, msec and timezone; no leading `*`.
- [ ] `show clock detail` source is NTP.
- [ ] A test log (`send log "test"`) appears in the SIEM with the correct time.
