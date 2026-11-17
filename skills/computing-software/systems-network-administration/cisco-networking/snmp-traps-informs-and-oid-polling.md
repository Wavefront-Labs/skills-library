---
id: computing-software.systems-network-administration.cisco-networking.snmp-traps-informs-and-oid-polling
name: snmp-traps-informs-and-oid-polling
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, snmp, snmp-traps, snmp-informs, snmp-server-host, snmp-server-enable-traps, oid, mib, if-mib, ifhcinoctets, trap-source, linkdown]
level: practitioner
status: docs-checked
description: "Send SNMP notifications from IOS and poll the right IF-MIB objects: traps vs informs, enabling trap types, trap source, and why 64-bit HC counters matter on fast links."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/snmp/configuration/xe-16/snmp-xe-16-book/nm-snmp-cfg-snmp-support.html
  - https://datatracker.ietf.org/doc/html/rfc2863
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNMP traps, informs and OID polling

## Traps vs informs
| | Trap | Inform |
|---|---|---|
| Delivery | no acknowledgment; sender cannot know it arrived | manager acknowledges with a response PDU; sender may retransmit |
| Cost | discarded once sent, sent only once | held in memory until answered or timed out; retries add traffic |
| Use | best effort | events where loss matters |

The agent uses the reserved UDP ports 161 and 162 when the SNMP process comes up; `show snmp host` on the Cisco page
shows hosts with `udp-port: 162`.

## Configure notifications
```
snmp-server trap-source <interface>
snmp-server enable traps snmp linkup linkdown warmstart coldstart
snmp-server enable traps bgp
snmp-server enable traps entity
snmp-server host <host> informs version 3 priv <user> <notification-type>
```
Host syntax on the page: `snmp-server host host-id [traps | informs] [version {1 | 2c | 3 [auth | noauth | priv]}]
community-string [udp-port port] [notification-type]`.
- No `snmp-server host` command means no notifications are sent. A host command without type keywords enables all
  trap types for that host.
- `snmp-server host` works with `snmp-server enable`: for most notifications you need at least one `enable` command
  and the host command. Repeating `snmp-server host` for the same host and notification kind overwrites the earlier
  line; use separate commands for separate hosts.
- `snmp-server enable traps snmp` with no keywords turns on authenticationFailure, linkUp, linkDown, warmStart and
  coldStart; with keywords, only those.
- linkUp/linkDown generation is controlled per interface by `snmp trap link-status`, and the page notes these
  notifications are enabled on interfaces by default but are not sent unless enabled globally.
- Which notification types exist depends on the platform and features; use `?` at the end of `snmp-server host` to
  see them.
- Check with `show snmp host` and `show snmp`.

## IF-MIB objects (RFC 2863)
Paths below are relative to mib-2.
| What | Object | Path |
|---|---|---|
| Interface name | ifName | 31.1.1.1.1 |
| Description alias | ifAlias | 31.1.1.1.18 |
| Traffic in/out, 64-bit | ifHCInOctets, ifHCOutOctets | 31.1.1.1.6, 31.1.1.1.10 |
| Operational status | ifOperStatus | 2.2.1.8 |
| Input errors | ifInErrors | 2.2.1.14 |
| Output discards | ifOutDiscards | 2.2.1.19 |

Use the HC (64-bit) counters on fast links. RFC 2863 gives the minimum wrap time of the 32-bit ifInOctets as
just over 57 minutes at 10 Mb/s, 5.7 minutes at 100 Mb/s and 34 seconds at 1 Gb/s, so polling every few minutes
misses wraps on gigabit links.

## Verify
- [ ] The NMS receives a linkDown when a test port is shut (with `snmp trap link-status` active on it).
- [ ] Graphs use HC counters.
- [ ] `show snmp host` lists the intended hosts and notification kind (trap or inform).

## Checked
Date: 2026-11-08. Read in the relevant sections: Cisco "Configuring SNMP Support" (IOS XE 16 book) and RFC 2863
(object definitions and the counter-wrap discussion).
Confirmed: items above, including each OID position from the RFC's `::=` assignments.
Removed: sysUpTime/sysName OIDs, Cisco CPU and memory-pool OIDs, the `config`, `envmon`, `ospf` and `cpu` trap lines,
the claim that `snmp-server enable traps` with no keyword is noisy with MAC notifications, `no snmp trap link-status`
as a recommendation, the snmpwalk/snmptranslate/snmptrapd tool section and `~/.snmp/mibs` advice, and the
`show run | i` check (none supported by the cited pages).
Method: documentation only; no commands were run.
