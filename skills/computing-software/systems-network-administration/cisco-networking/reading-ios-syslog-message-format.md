---
id: computing-software.systems-network-administration.cisco-networking.reading-ios-syslog-message-format
name: reading-ios-syslog-message-format
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, syslog, syslog-message-format, facility-severity-mnemonic, log-parsing, severity-levels, service-timestamps]
level: practitioner
status: draft
description: "Read IOS syslog lines (%FACILITY-SEVERITY-MNEMONIC), map severities 0-7, add timestamps and sequence numbers, and parse them reliably at the collector."
sources:
  - https://www.cisco.com/c/en/us/td/docs/routers/access/wireless/software/guide/SysMsgLogging.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/esm/configuration/xe-16/esm-xe-16-book/esm-sys-msg-log.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading FACILITY-SEVERITY-MNEMONIC messages

## Anatomy
```
000123: *Oct 18 09:14:07.412 UTC: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet1/0/3, changed state to down
^seq    ^timestamp (* = clock not authoritative)  ^facility ^sev ^mnemonic  ^description
```
- **Facility**: the IOS component (LINK, LINEPROTO, OSPF, SYS, SEC_LOGIN, DUAL, BGP, PLATFORM...).
  This is not the syslog RFC facility (local7 by default, set with `logging facility`).
- **Severity**: 0-7.
- **Mnemonic**: event name, stable across releases; use it as the parsing key.

| Level | Keyword | Example |
|---|---|---|
| 0 | emergencies | system unusable |
| 1 | alerts | `%PLATFORM_ENV-1-FAN` |
| 2 | critical | `%SYS-2-MALLOCFAIL` |
| 3 | errors | `%LINK-3-UPDOWN` |
| 4 | warnings | `%SW_MATM-4-MACFLAP_NOTIF` |
| 5 | notifications | `%SYS-5-CONFIG_I`, `%OSPF-5-ADJCHG` |
| 6 | informational | `%SEC-6-IPACCESSLOGP` |
| 7 | debugging | debug output |

`logging trap notifications` sends levels 0-5 to the server.

## Make lines useful
```
service timestamps log datetime msec localtime show-timezone year
service sequence-numbers
logging origin-id hostname
logging source-interface Loopback0
```
A leading `*` means the clock is not NTP-synced; `.` means it was synced but lost sync.

## Parsing
Regex for the core:
`%(?P<facility>[A-Z0-9_]+)-(?P<severity>[0-7])-(?P<mnemonic>[A-Z0-9_]+):\s(?P<msg>.*)`
IOS XE on some platforms adds a prefix (`%... : SW1 R0/0:`) for the process; allow optional text before `%`.

## Look up a message
Cisco's System Message Guide / error message decoder explains each FACILITY-SEV-MNEMONIC with recommended action.

## Verify
- [ ] Collector extracts facility/severity/mnemonic fields for 100% of a sample.
- [ ] All devices log with year, msec, timezone and sequence numbers.
