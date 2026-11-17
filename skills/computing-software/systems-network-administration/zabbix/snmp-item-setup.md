---
id: computing-software.systems-network-administration.zabbix.snmp-item-setup
name: snmp-item-setup
category: computing-software
field: systems-network-administration
product: zabbix
tags: [snmp, snmpv3, oid, net-snmp, snmpwalk]
level: practitioner
status: docs-checked
description: "Set up SNMP monitoring: find the OID, add an SNMP interface, choose the version and understand retries and combined requests."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/snmp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SNMP checks need a server built with --with-net-snmp and run over UDP only. Install MIB files so values display correctly; without them formatting issues such as HEX instead of UTF-8 can appear.

Setup:
1. Find the OID. Run snmpwalk -v 2c -c public <host IP> . then use snmpget -On <host IP> IF-MIB::ifHCInOctets.3 to get the numeric OID, here .1.3.6.1.2.1.31.1.1.1.6.3. The last number is the port index.
2. Create the host with an SNMP interface: address, port and version. SNMPv1 and v2 need a community, usually public. SNMPv3 needs context name, security name, security level (noAuthNoPriv, AuthNoPriv, authPriv) and the matching authentication and privacy settings; user macros resolve in these fields.
3. Set the max repetition value (default 10), used for native bulk requests by discovery[] and walk[] in v2 and v3. Too high a value can time out the check.
4. Tick Use combined requests to batch legacy single-OID checks.

Retries: the server retries up to 5 times for walk and get items, but not on DNS failures.

SNMPv3 caveats: msgAuthoritativeEngineID must be unique per device. Some devices do not persist engineBoots, so after a reboot their messages are discarded as outdated; clear the cache with -R snmp_cache_reload or restart the server or proxy.

If a device returns wrong or short answers, turn off combined requests for that interface and look for the log line "does not contain all of the requested variable bindings".

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/items/itemtypes/snmp): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
