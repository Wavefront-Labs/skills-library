---
id: computing-software.systems-network-administration.cisco-networking.snmptrapd-trap-receiver
name: snmptrapd-trap-receiver
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [snmp, snmptrapd, net-snmp, snmpv3-traps, trap-receiver, mib, linkdown, monitoring]
level: practitioner
status: draft
description: "Receive SNMP traps and informs with Net-SNMP snmptrapd: v2c communities and v3 USM users with engine IDs, MIB loading for readable output, forwarding to logs, and testing."
sources:
  - http://www.net-snmp.org/docs/man/snmptrapd.html
  - http://www.net-snmp.org/docs/man/snmptrapd.conf.html
  - https://www.rfc-editor.org/rfc/rfc3414
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Receiving traps with snmptrapd

## v2c
`/etc/snmp/snmptrapd.conf`:
```
authCommunity log,execute,net TrapC0mm
format2 %V\n%B [%a]: %W\n%v\n
```
`log` writes to syslog/stdout, `execute` allows traphandle scripts, `net` allows forwarding.

## v3 traps (USM)
Traps are sent with the sender's engine ID, so the receiver needs a user per sending engine ID:
```
createUser -e 0x800000090300AABBCCDDEEFF trapuser SHA "AuthPass123" AES "PrivPass123"
authUser log,execute trapuser priv
```
Get the device engine ID with `show snmp engineID` on IOS. Informs are different: the receiver's
engine ID is used, so one `createUser trapuser ...` (no `-e`) works for all senders.

Device side (IOS):
```
snmp-server group TRAPGRP v3 priv
snmp-server user trapuser TRAPGRP v3 auth sha AuthPass123 priv aes 128 PrivPass123
snmp-server host 10.0.0.70 informs version 3 priv trapuser
snmp-server enable traps snmp linkdown linkup coldstart
snmp-server enable traps config
```

## Run and read
```
snmptrapd -f -Lo -m ALL -M /usr/share/snmp/mibs:/opt/mibs/cisco    # foreground, log to stdout
systemctl enable --now snmptrapd
```
Without MIBs you see numeric OIDs like `.1.3.6.1.6.3.1.1.5.3`; with them `IF-MIB::linkDown`.
Download Cisco MIBs (CISCO-SMI, CISCO-CONFIG-MAN-MIB, etc.) into a local MIB dir.

## Hand off
```
traphandle IF-MIB::linkDown /usr/local/bin/notify-linkdown.sh
traphandle default /usr/bin/logger -t snmptrap
```
Or forward everything to the monitoring system: `forward default udp:monitor.example.net:162`.

## Test
```
snmptrap -v 2c -c TrapC0mm 10.0.0.70 '' IF-MIB::linkDown ifIndex.3 i 3
snmpinform -v 3 -u trapuser -l authPriv -a SHA -A AuthPass123 -x AES -X PrivPass123 10.0.0.70 '' coldStart
```

## Gotchas
- UDP 162 is privileged; run as root or grant the capability. Firewalls must allow it inbound.
- Wrong engine ID for v3 traps fails silently (`Unknown engine ID` with `-Dusm`).
- Traps are UDP, fire-and-forget; use informs for anything you must not miss.

## Verify
- [ ] Shutting a test interface produces a readable linkDown line within seconds.
