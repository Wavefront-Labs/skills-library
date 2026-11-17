---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-ha-link-and-path-monitoring
name: pan-os-ha-link-and-path-monitoring
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [ha-path-monitoring, pan-os, link-monitoring, failover-conditions, monitor-failure, hold-up-time, ha-timers]
level: practitioner
status: draft
description: "Configure PAN-OS HA link groups and path groups so failover triggers on real failures, and tune timers to avoid flapping."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/high-availability/ha-concepts/device-priority-and-preemption"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: failover when the data path is down, not just when the peer is dead.

Link monitoring watches physical interface state; path monitoring pings IPs through the data path (for example the next hop) and counts failures.

```
configure
set deviceconfig high-availability group monitoring link-monitoring enabled yes failure-condition any
set deviceconfig high-availability group monitoring link-monitoring link-group uplinks enabled yes interface [ ethernet1/1 ethernet1/2 ] failure-condition any
set deviceconfig high-availability group monitoring path-monitoring enabled yes failure-condition any
set deviceconfig high-availability group monitoring path-monitoring path-group virtual-router default destination-ip-group gw enabled yes destination-ip [ 192.0.2.1 ] ping-interval 200 ping-count 10 failure-condition any
commit
```
(Hierarchy shown as a sketch; confirm exact path in your release, or use Device > High Availability > Link and Path Monitoring.)

Timer profiles: Recommended, Aggressive or custom set promotion hold time, hello interval and heartbeat. Aggressive fails over faster but can flap.

Gotchas
- Path monitoring of a single host fails over when that host is down; monitor an upstream device that represents the real path.
- Both peers need the same monitoring config; mismatch causes odd failover decisions.
- After a monitoring-triggered failover the original unit may show `non-functional`; find the cause before enabling preempt.

## Verify
```
show high-availability state
show high-availability path-monitoring
show high-availability link-monitoring
```
Disconnect a monitored link in a test window and confirm the passive peer takes over.
