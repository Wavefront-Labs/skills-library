---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-ha-fgcp-active-passive-cluster
name: fortigate-ha-fgcp-active-passive-cluster
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [fgcp-ha, fortios, high-availability, ha-heartbeat, session-pickup, virtual-mac, ha-override]
level: practitioner
status: draft
description: "Build a FortiGate FGCP active-passive HA cluster with heartbeat interfaces, priority, monitored ports and session pickup."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: two identical units failing over with sessions intact.

Both units, same model and firmware:
```
config system ha
    set group-name "fgt-cluster"
    set mode a-p
    set password <HA-PASSWORD>
    set hbdev "port3" 50 "port4" 100
    set session-pickup enable
    set priority 200
    set override disable
    set monitor "port1" "port2"
end
```
Use a lower priority (for example 100) on the peer. Cabled heartbeat links on dedicated ports. Config sync is automatic from the primary; `execute ha manage <index> <admin>` logs into the secondary.

Key behaviour
- Primary election: highest uptime (older releases) or priority per `override`; confirm in your release. With `override enable` the highest priority always becomes primary.
- Virtual MAC addresses (00:09:0f:09:xx:xx) move with the primary, so ARP changes minimal.
- Hostnames differ per unit (not synced).

Gotchas
- Mismatched licences, firmware or hardware prevent sync.
- Heartbeat over a shared production switch is fragile; use direct cables.
- Upgrade the cluster as a whole, one unit at a time (see firmware skill).
- Management interface reservation (`set ha-mgmt-status enable`) gives a unique management IP per unit.

## Verify
```
get system ha status
diagnose sys ha status
diagnose sys ha checksum cluster
```
Both members show in sync and the checksums match.
