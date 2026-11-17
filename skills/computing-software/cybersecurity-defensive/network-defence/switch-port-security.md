---
id: computing-software.cybersecurity-defensive.network-defence.switch-port-security
name: switch-port-security
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [network-access-control, port-security, sticky-mac, err-disable, bpdu-guard, storm-control, unused-ports-shutdown, layer-2-security]
level: practitioner
status: draft
description: "Apply switch port security and layer-2 hygiene: MAC limits, sticky MACs, BPDU guard, storm control, shutting unused ports and handling err-disabled ports."
sources: ["CompTIA Security+ SY0-701 objective 3.2 (port security)", "Cisco Catalyst Security Configuration Guide (port security, BPDU guard, storm control)", "NSA Network Infrastructure Security Guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Switch port security

**Goal:** access ports accept only expected devices and cannot be used to disrupt the
layer-2 network, where full NAC is not available.

## Baseline for access ports (Cisco example)
```
interface range GigabitEthernet1/0/1 - 48
 switchport mode access
 switchport nonegotiate                       ! no DTP trunk negotiation
 switchport access vlan 100
 switchport port-security
 switchport port-security maximum 2           ! PC + IP phone
 switchport port-security mac-address sticky
 switchport port-security violation restrict  ! drop and log; 'shutdown' is stricter
 spanning-tree portfast
 spanning-tree bpduguard enable
 storm-control broadcast level 5.00
 storm-control action trap
```
Unused ports:
```
interface range GigabitEthernet1/0/40 - 48
 switchport access vlan 999                   ! parking VLAN, not routed
 shutdown
```
Also: change the native VLAN on trunks to an unused VLAN, prune trunk allowed VLANs, and do
not use VLAN 1 for user traffic.

## Violation modes
- `protect`: drop silently (no logs) - avoid.
- `restrict`: drop and log/SNMP trap - good default.
- `shutdown`: err-disable the port - strongest, causes helpdesk calls.
Recovery: `errdisable recovery cause psecure-violation` with an interval, or manual `shutdown`/`no shutdown`.

## Monitoring
`show port-security`, `show port-security address`, syslog `%PORT_SECURITY-2-PSECURE_VIOLATION`
to the SIEM. Alert on BPDU guard err-disables (someone plugged in a switch).

## Gotchas
- Sticky MACs are saved only after `write memory`; otherwise lost on reboot.
- Virtualised desktops and docking stations change MAC counts; size `maximum` accordingly.
- Port security does not stop MAC spoofing of an allowed device: it is a hygiene control, not authentication.

## Verify
- [ ] Config audit shows all access ports with port security, BPDU guard and nonegotiate.
- [ ] Plugging a small switch into a test port triggers BPDU guard and an alert.
