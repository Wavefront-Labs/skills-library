---
id: computing-software.systems-network-administration.keepalived.snmp-mib-oids
name: snmp-mib-oids
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, snmp, mib, oid, snmpwalk, keepalived-mib, monitoring]
level: practitioner
status: docs-checked
description: "Query Keepalived over SNMP: the KEEPALIVED-MIB sections, base OID .1.3.6.1.4.1.9586.100.5, snmpwalk examples and where to install the MIB file."
sources:
  - https://keepalived.readthedocs.io/en/latest/snmp_support.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KEEPALIVED-MIB and OIDs

The MIB file `KEEPALIVED-MIB` is in the project's doc directory. To use names rather than numbers, copy it to /usr/share/snmp/mibs (global) or ~/.snmp/mibs (per user); snmpd checks both.

Sections:
- **global:** version, router ID, administrative email addresses.
- **vrrp:** each instance's name, current state and virtual IP addresses.
- **check:** virtual and real server tables, algorithm, method, protocol, status and connection statistics.
- **conformance:** not yet documented.

Base OID: `.1.3.6.1.4.1.9586.100.5` (in the IANA-assigned Debian OID space). The version string is `.1.3.6.1.4.1.9586.100.5.1.1.0`.

```
snmpwalk -v2c -c public localhost .1.3.6.1.4.1.9586.100.5.1.1.0
snmpwalk -v2c -c public localhost KEEPALIVED-MIB::version
```
The docs recommend a MIB browser such as mbrowse for browsing objects and monitoring LVS health.

Verify: the version query returns the running Keepalived version string.

## Checked

2026-11-04. Confirmed the base OID, the version OID, both snmpwalk examples, the MIB directories, the four MIB sections, the conformance todo and the mbrowse note on the Configuring SNMP Support page. Nothing removed.

Method: documentation only; no commands were run.
