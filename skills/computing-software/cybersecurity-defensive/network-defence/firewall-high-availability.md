---
id: computing-software.cybersecurity-defensive.network-defence.firewall-high-availability
name: firewall-high-availability
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [firewall-high-availability, ha-cluster, active-passive, state-synchronisation, failover-testing, pan-os-ha, fortigate-ha]
level: practitioner
status: draft
description: "Design and test firewall HA: active/passive vs active/active, session sync, HA links and monitoring, split-brain avoidance, upgrades without outages and failover drills."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/high-availability", "https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/62403/high-availability", "https://csrc.nist.gov/pubs/sp/800/41/r1/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Firewall high availability

## Modes
| Mode | Use | Caveat |
|---|---|---|
| Active/passive | Default choice; simple, predictable | Passive capacity idle |
| Active/active | Asymmetric routing designs, more throughput | Complex session ownership; each unit must handle full load on failure anyway |
| Cloud | Usually no L2 HA; use load-balancer sandwich or Gateway Load Balancer with autoscaling | Session state not synced in many designs |

## Configuration essentials
- Identical model, licences, software version.
- Dedicated HA links: control (heartbeat/config) and data (session sync); use two heartbeat paths (HA1 + HA1 backup / multiple heartbeat interfaces) to avoid split-brain.
- **Link and path monitoring:** fail over when an upstream interface or next-hop IP is lost, not just when the unit dies.
- Preemption off for active/passive unless there is a reason (avoids flapping).
- Session synchronisation on so established flows survive failover.

## Upgrades
Suspend/upgrade the passive peer, fail over, upgrade the other, fail back if needed. Check compatibility
of sync between versions; PAN-OS supports upgrades across HA peers with the same major/minor feature rules.

## Testing
Quarterly: pull the active unit's power or suspend it (`request high-availability state suspend` on
PAN-OS; `execute ha failover set 1` on FortiOS 7.x), and fail a monitored link. Measure packet loss and
check long-lived sessions (SSH, database) survive.

## Gotchas
- Split-brain with both active causes duplicate IP/MAC and outages; out-of-band heartbeat path prevents it.
- Config sync does not include everything (management IPs, HA settings themselves); verify after changes.
- Cloud "HA" templates may fail over by API route-table change taking 30-60 s.

## Verify
- [ ] HA status healthy, config synced (`show high-availability state` / `get system ha status`).
- [ ] Last failover drill within 3 months with measured impact.
