---
id: computing-software.systems-network-administration.cisco-networking.snmp-hardening
name: snmp-hardening
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, snmp, snmp-hardening, snmpv3, community-string, read-only, acl, security-audit]
level: practitioner
status: draft
description: "Lock down SNMP on network devices: remove default and RW communities, move to SNMPv3 authPriv, restrict by ACL and view, and audit the estate for weak settings."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/simple-network-management-protocol-snmp/20370-snmpsecurity-20370.html
  - https://www.cisa.gov/news-events/alerts/2017/06/05/reducing-risk-snmp-abuse
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SNMP hardening

SNMP with a guessable community and RW access lets anyone reachable download or rewrite the
configuration. It is one of the most common findings in network audits.

## Baseline
```
no snmp-server community public
no snmp-server community private
! any remaining RW communities: remove unless a tool truly needs write access
ip access-list standard SNMP-MGRS
 permit 10.0.0.60
 permit 10.0.0.61
 deny any log
snmp-server view LIMITED iso included
snmp-server view LIMITED 1.3.6.1.6.3.15 excluded      ! hide USM user table
snmp-server group MON v3 priv read LIMITED access SNMP-MGRS
snmp-server user monitor MON v3 auth sha <authpass> priv aes 128 <privpass>
snmp-server location DC1-RowB-R12
snmp-server contact noc@example.net
```
Prefer `auth sha-2 256`/`aes 256` where the release and the NMS support them.

## If v2c must stay (old tools)
```
snmp-server community L0ng-R4nd0m-String RO SNMP-MGRS
```
RO only, long random string, ACL, and plan the v3 migration.

## Control-plane protection
- CoPP class limiting SNMP to the manager addresses.
- Management VRF so SNMP is not reachable from user subnets at all.
- `no snmp-server system-shutdown` and avoid `snmp-server enable traps` with community strings
  sent to unknown hosts.

## Disable entirely where unused
`no snmp-server` removes all SNMP configuration (check what else depends on it first).

## Audit
```
show running-config | include snmp-server community|snmp-server user|snmp-server host
show snmp community
show snmp group
show snmp user
```
Estate-wide: run a config grep in your backup system (Oxidized/RANCID) for `community public`,
`RW`, and communities without an ACL. From a scanner host, `onesixtyone -c dict.txt -i hosts.txt`
finds devices answering common strings (with authorisation).

## Gotchas
- Community strings are cleartext on the wire in v1/v2c; v3 authPriv encrypts.
- Deleting the community the NMS uses breaks monitoring; add v3 first, switch the NMS, then remove.
- `snmp-server user` passwords are not shown in running-config; keep them in your secrets vault.

## Verify
- [ ] `snmpwalk -v2c -c public <device>` times out from any host.
- [ ] `snmpwalk -v3 -l authPriv ...` from the NMS works; from another host it is refused.
