---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-interfaces-roles-and-zones
name: fortigate-interfaces-roles-and-zones
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [fortigate-interfaces, fortios, interface-role, allowaccess, zone, ha-mgmt, system-interface]
level: practitioner
status: draft
description: "Configure FortiGate interfaces with IP, role, allowed admin access and group them into zones to simplify policy."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: interfaces that are addressed, labelled and only expose needed services.

```
config system interface
    edit "port1"
        set alias "WAN"
        set role wan
        set mode static
        set ip 192.0.2.2 255.255.255.0
        set allowaccess ping
        set estimated-upstream-bandwidth 100000
        set estimated-downstream-bandwidth 100000
    next
    edit "port2"
        set alias "LAN"
        set role lan
        set ip 10.1.0.1 255.255.255.0
        set allowaccess ping https ssh
    next
end
config system zone
    edit "INTERNAL"
        set interface "port2" "port3"
        set intrazone deny
    next
end
```
Roles (wan, lan, dmz, undefined) affect GUI defaults and which interface offers features such as DHCP; `allowaccess` governs access to the FortiGate itself (https, ssh, snmp, ping, fgfm, radius-acct, capwap, ftm).

Gotchas
- Members of a zone cannot be referenced individually in policies. Remove the interface from policies first.
- `set intrazone deny` blocks traffic between zone members unless a policy allows it; `allow` lets them talk freely.
- Do not leave `https ssh` on WAN interfaces; use local-in policies (`config firewall local-in-policy`) when management over WAN is unavoidable.

## Verify
```
get system interface physical
get system interface
diagnose ip address list
```
Interfaces up with correct IP; test reachability with `execute ping-options source 10.1.0.1` then `execute ping 10.1.0.5`.
