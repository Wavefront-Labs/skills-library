---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-ha-active-passive
name: pan-os-ha-active-passive
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [ha-active-passive, pan-os, high-availability, ha1, ha2, preemption, config-sync, state-sync]
level: practitioner
status: draft
description: "Build a PAN-OS active/passive HA pair with ha1/ha2 links, priorities, preemption, config and session sync, and verify failover readiness."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/high-availability/set-up-active-passive-ha"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: a pair that fails over with sessions preserved.

Prerequisites: same model, same PAN-OS and content version, same licences per device, same interface layout. Dedicated HA1 (control) and HA2 (data) links; add a backup HA1 and HA1 encryption if crossing a switch.

Primary:
```
configure
set deviceconfig high-availability enabled yes
set deviceconfig high-availability interface ha1 port ha1-a ip-address 192.0.2.201 netmask 255.255.255.252
set deviceconfig high-availability interface ha2 port ha2-a ip-address 192.0.2.205 netmask 255.255.255.252
set deviceconfig high-availability group group-id 1 mode active-passive peer-ip-address 192.0.2.202
set deviceconfig high-availability group group-id 1 election-option device-priority 90 preemptive yes
commit
```
On the peer swap the addresses and use a worse priority (higher number). Link and path monitoring are covered in the ha-path-monitoring skill.

Gotchas
- Management interface, HA settings and device-specific values are not synced; everything else is.
- Preemptive plus flapping links causes failover storms; use a hold timer.
- A suspended or non-functional peer means no failover: always check state after maintenance.
- Different content versions or licence sets raise a mismatch; fix before expecting config sync.

## Verify
```
show high-availability state
show high-availability all
request high-availability sync-to-remote running-config
request high-availability state suspend
request high-availability state functional
```
Expect local active / peer passive, running config synchronised, and a successful suspend/functional test in a window.
