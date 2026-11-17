---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.snmp-and-remote-syslog
name: snmp-and-remote-syslog
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, snmp, remote-syslog, ntp-dns]
level: practitioner
status: draft
description: "Configure SNMP v2c/v3 access, trap destinations and remote syslog on BIG-IP, and keep NTP and DNS correct."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-system-initial-configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SNMP and remote syslog configuration

```
tmsh modify sys snmp allowed-addresses add { 10.9.9.0/24 }
tmsh modify sys snmp communities add { monitor { community-name 'ro-comm' source 10.9.9.0/24 access ro } }
tmsh modify sys snmp traps add { t1 { host 10.9.9.50 community ro-comm version 2c port 162 } }
tmsh modify sys syslog remote-servers add { siem { host 10.9.9.60 remote-port 514 } }
tmsh modify sys ntp servers add { 0.pool.ntp.org 1.pool.ntp.org }
tmsh modify sys dns name-servers add { 10.1.1.2 } search add { example.com }
tmsh save sys config
```
- By default SNMP only answers from 127.0.0.0/8, so add `allowed-addresses`. SNMP listens on management and self IPs only if their port lockdown permits UDP 161 (`allow-service add { udp:161 }`).
- Prefer SNMPv3 users: `tmsh modify sys snmp users add { u { auth-protocol sha auth-password-encrypted ... } }` (confirm syntax).
- `remote-servers` ships all syslog levels; filter noisy ones with `sys syslog include`. Use TCP/TLS through a log forwarder if loss is unacceptable, as plain UDP drops.
- Certificates and logins break when time drifts: confirm `tmsh show sys ntp` reaches stratum under 16.
- Gotcha: changing hostname and SNMP `sys-contact` triggers no restart, but trap targets on data VLANs need a self IP route.

Verify: `snmpwalk -v2c -c ro-comm <bigip> sysProductVersion` from the allowed host, and `logger -p local0.info testmsg` (or `tmsh show sys log ltm`) arriving at the SIEM.
