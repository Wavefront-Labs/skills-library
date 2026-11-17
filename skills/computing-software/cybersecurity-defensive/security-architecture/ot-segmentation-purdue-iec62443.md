---
id: computing-software.cybersecurity-defensive.security-architecture.ot-segmentation-purdue-iec62443
name: ot-segmentation-purdue-iec62443
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [network-segmentation, purdue-model, iec-62443, ot-security, zones-and-conduits, industrial-dmz, ics-security]
level: advanced
status: draft
description: "Segment OT networks using the Purdue model and IEC 62443 zones and conduits: asset zoning, industrial DMZ, conduit rules, remote access paths and monitoring."
sources: ["https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards", "https://csrc.nist.gov/pubs/sp/800/82/r3/final", "https://www.cisa.gov/topics/industrial-control-systems"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OT segmentation (Purdue / IEC 62443)

**Goal:** contain IT-borne threats (ransomware, phishing footholds) away from industrial
control systems, and limit spread inside OT, without breaking deterministic process control.

## Reference models
- **Purdue model levels:** L0 physical process (sensors, actuators), L1 basic control
  (PLCs, RTUs), L2 supervisory (HMI, SCADA), L3 site operations (historians, engineering
  workstations, OT AD), L3.5 **industrial DMZ**, L4/5 enterprise IT and internet.
- **IEC 62443-3-2 zones and conduits:** group assets with common security requirements
  into zones; every communication between zones goes through a defined conduit with
  controls. Assign a target security level (SL 1-4) per zone from risk assessment.

## Design steps
1. Inventory OT assets and flows (passive monitoring: Claroty, Nozomi, Dragos, Defender for
   IoT; vendor documentation). No active scanning on live control networks without vendor approval.
2. Define zones: per production line/cell, safety instrumented systems (SIS) in their own
   zone, supervisory, site operations, IDMZ.
3. **IDMZ:** no direct traffic from IT to L3 or below. Patterns: historian replica in IDMZ
   (OT pushes, IT reads), patch/AV staging server, remote access jump host, file transfer
   with scanning. Rule of thumb: traffic terminates in the IDMZ; nothing traverses it end to end.
4. Conduits: firewalls (OT-aware with protocol inspection for Modbus/DNP3/S7/CIP where
   needed) with explicit allow rules; unidirectional gateways (data diodes) for high-SL zones.
5. Remote access: vendor and engineer access via IDMZ jump host with MFA, session recording,
   time-bound approval; no always-on vendor VPNs into L2.

## Monitoring
OT network detection at zone boundaries and inside (SPAN/TAP), alerts on new flows, PLC
program changes/mode changes, engineering protocol use from non-engineering hosts.

## Gotchas
- Flat L2 networks with shared VLANs across lines: segment gradually during planned outages.
- Dual-homed hosts (engineering laptops, historians with two NICs) bridge zones; remove.
- Firewall changes on control networks need OT change control and testing; latency-sensitive
  traffic may break.
- Safety systems must stay independent from basic control.

## Verify
Conduit rule review against the documented flow matrix; from an IT host, attempts to reach
L2/L1 addresses fail; passive monitoring shows no unexpected cross-zone flows.
