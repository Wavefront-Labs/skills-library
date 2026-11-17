---
id: computing-software.systems-network-administration.cisco-networking.snmpv3-and-v2c-configuration
name: snmpv3-and-v2c-configuration
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, snmp, snmpv3, authpriv, snmpv2c, snmp-community, snmp-view, snmp-group, snmp-user, snmp-acl, snmp-server, usm, engine-id, engineid, ifindex-persist]
level: practitioner
status: draft
description: "Configure SNMP on IOS safely: SNMPv3 authPriv groups, users and views, read-only v2c communities locked by ACL when v3 is impossible, and testing with snmpwalk."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/snmp/configuration/xe-16/snmp-xe-16-book/nm-snmp-snmpv3.html
  - https://datatracker.ietf.org/doc/html/rfc3414
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNMPv3 and v2c configuration on IOS

SNMPv1/v2c send the community string in cleartext; v3 adds authentication (SHA) and
encryption (AES) per user. Use v3 everywhere your NMS supports it; v2c read-only, ACL-bound,
only as a fallback.

## SNMPv3 authPriv
```
ip access-list standard NMS
 permit 10.0.0.30
 permit 10.0.0.31
snmp-server view NMS-VIEW iso included
snmp-server group NMS-RO v3 priv read NMS-VIEW access NMS
snmp-server user nmsuser NMS-RO v3 auth sha <AUTH_PASS> priv aes 128 <PRIV_PASS> access NMS
snmp-server location DC1 Row4 Rack12
snmp-server contact noc@example.org
snmp-server ifindex persist          ! stable ifIndex across reloads for graphs
```
Security levels: `noauth` (noAuthNoPriv), `auth` (authNoPriv), `priv` (authPriv). Use `priv`.
Newer IOS XE supports `auth sha-2 256` and `priv aes 256`; match what the NMS supports.

- `snmp-server user` lines do **not** appear in `show running-config` (keys are localised to
  the engine ID). Check with `show snmp user`. Record credentials in your vault.
- Changing `snmp-server engineID local` invalidates all v3 users; re-create them.

## SNMPv2c fallback
```
snmp-server community <RANDOM_LONG_STRING> RO NMS
```
Never use `public`/`private`, never `RW` unless a specific tool requires it (and then with a
restricted view and ACL).

## Test from the NMS
```
snmpwalk -v3 -l authPriv -u nmsuser -a SHA -A '<AUTH_PASS>' -x AES -X '<PRIV_PASS>' <DEVICE> 1.3.6.1.2.1.1
snmpget -v2c -c '<COMMUNITY>' <DEVICE> sysUpTime.0
```
Errors: `Unknown user name` (user/engine mismatch), `Authentication failure` (wrong pass or
algorithm), `Decryption error` (priv pass/algorithm), timeout (ACL, CoPP, wrong VRF, UDP 161 blocked).

## Check on the device
```
show snmp user
show snmp group
show snmp engineID
show snmp | i packets|Unknown|Illegal
```

## Verify
- [ ] `snmpwalk` with authPriv works from the NMS, fails from other hosts.
- [ ] No `community` lines other than the intended RO one (`show run | i snmp-server community`).
- [ ] ifIndex persistence enabled so graphs do not jump after reload.
