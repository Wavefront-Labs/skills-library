---
id: computing-software.cybersecurity-defensive.system-hardening.snmpv3-configuration
name: snmpv3-configuration
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [snmpv3, usm, authpriv, net-snmp, network-hardening, monitoring-security]
level: practitioner
status: docs-checked
description: "Move monitoring to SNMPv3 authPriv: remove v1/v2c communities, create net-snmp users, understand USM keys and engine IDs, and validate that v2c polling fails."
sources: ["https://www.rfc-editor.org/rfc/rfc3414.html", "https://www.net-snmp.org/docs/man/snmpcmd.html", "https://www.net-snmp.org/docs/man/net-snmp-create-v3-user.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNMPv3 configuration

**Goal:** monitoring works over authenticated, encrypted SNMPv3 only; community strings are gone.

## Concepts
- SNMPv3 uses the User-based Security Model (RFC 3414). The RFC defines HMAC-MD5-96 (must be supported) and HMAC-SHA-96 (should be supported) authentication, and CBC-DES privacy as the first privacy protocol.
- Security levels are `noAuthNoPriv`, `authNoPriv` and `authPriv`. Use `authPriv` (authentication plus encryption).
- User keys are localised: the user's key is combined with the authoritative engine's snmpEngineID, so the secret shared with each engine differs. A device whose engine ID changes cannot validate keys localised to the old ID; plan to re-create the user after replacement.

## Linux net-snmp agent
`net-snmp-create-v3-user -ro -a <authpass> -x <privpass> -X <DES|AES> nmsuser` creates a read-only user in the net-snmp configuration file (the page gives `/var/net-snmp/snmpd.conf` as the default). Remove v1/v2c community lines from `snmpd.conf` and restrict who can poll with your agent's access settings; check the net-snmp documentation for the exact directives.

## Network devices
Follow each vendor's SNMPv3 configuration guide: define a restricted read-only view and group, create the user with authentication and privacy, restrict polling sources with an ACL, then delete the v1/v2c communities. Prefer read-only access.

## Test
```
snmpwalk -v3 -l authPriv -u nmsuser -a SHA -A <authpass> -x AES -X <privpass> <device> system
snmpwalk -v2c -c <old-community> <device> system     # must now fail
```
net-snmp options (snmpcmd): `-v 1|2c|3`, `-l` security level, `-u` security name, `-a` authentication protocol (MD5 or SHA), `-A` authentication pass phrase, `-x` privacy protocol (DES or AES, only if built with OpenSSL), `-X` privacy pass phrase, `-c` community. The page warns that pass phrases on the command line are insecure; prefer a configuration file.

## Rollout
Update the monitoring system first, add v3 on devices, confirm polling, then remove communities.

## Verify
- [ ] Monitoring shows all devices polling via v3.
- [ ] A v2c poll with the old community fails from the monitoring host and from another host.

## Checked
2026-11-01. Confirmed: USM authentication and privacy protocols and engine-ID key localisation (RFC 3414, first 100,000 characters); snmpwalk-style options and security levels (net-snmp snmpcmd); `net-snmp-create-v3-user` options `-ro`, `-a`, `-x`, `-X` and default config file path.
Removed: Cisco IOS XE configuration (page not readable), SHA-2 and AES-256 options, claims that MD5 and DES are weak, `snmp-server` commands, nmap SNMP script check, trap/inform and NMS product notes, default-community template note.
Method: documentation only; no commands were run.
