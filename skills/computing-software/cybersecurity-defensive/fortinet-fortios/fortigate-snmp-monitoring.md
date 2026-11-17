---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-snmp-monitoring
name: fortigate-snmp-monitoring
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [snmp-agent, fortios, snmpv3, snmp-community, mib, oid, monitoring]
level: practitioner
status: draft
description: "Enable SNMPv3 on FortiGate with auth and privacy, restrict hosts, and poll standard and Fortinet OIDs."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: secure polling by the monitoring system.

```
config system snmp sysinfo
    set status enable
    set description "edge firewall"
    set location "dc1"
end
config system snmp user
    edit "monitor"
        set security-level auth-priv
        set auth-proto sha256
        set auth-pwd <AUTH-PASSWORD>
        set priv-proto aes256
        set priv-pwd <PRIV-PASSWORD>
        set notify-hosts 192.0.2.50
    next
end
config system interface
    edit "port2"
        append allowaccess snmp
    next
end
```
Fortinet enterprise OIDs are under 1.3.6.1.4.1.12356 (FORTINET-FORTIGATE-MIB: CPU, memory, sessions, HA, VPN tunnels). Download MIB files from the support portal (FORTINET-CORE-MIB and FORTINET-FORTIGATE-MIB).

Poll test from a monitoring host:
```
snmpwalk -v3 -l authPriv -u monitor -a SHA-256 -A '<AUTH-PASSWORD>' -x AES-256 -X '<PRIV-PASSWORD>' 192.0.2.2 1.3.6.1.4.1.12356.101.4.1
```
(Use `SHA`/`AES` if your tool lacks the longer variants; confirm supported protocols.)

Gotchas
- Allow SNMP only on trusted interfaces; use a local-in policy to limit source IPs.
- `append allowaccess snmp` keeps existing services; `set allowaccess snmp` replaces them and can lock you out.
- Community strings (v1/v2c) are cleartext; avoid.

## Verify
`snmpwalk` returns sysDescr and Fortinet values; `diagnose sys snmp` style debugging lists requests (confirm).
