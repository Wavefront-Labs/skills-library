---
id: computing-software.systems-network-administration.patch-management.ot-ics-patching-groups
name: ot-ics-patching-groups
category: computing-software
field: systems-network-administration
product: patch-management
tags: [ot-patching, ics-patching, maintenance-groups, compensating-controls, nist-800-82, iec-62443]
level: advanced
status: draft
description: "Patch OT/ICS environments: vendor-qualified patches only, maintenance windows tied to process outages, staged testing, compensating controls when patching is impossible."
sources:
  - https://csrc.nist.gov/pubs/sp/800/82/r3/final
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://www.cisa.gov/topics/industrial-control-systems
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OT and ICS patching

OT priorities are safety and availability first, then integrity, then confidentiality.
IT-style monthly forced patching breaks plants. NIST SP 800-82r3 and IEC 62443-2-3 describe
a different cadence.

## Groups and cadence
| Group | Examples | Approach |
|---|---|---|
| Level 3/3.5 (site ops, DMZ) | historians, jump hosts, patch/AV servers | near-IT cadence (monthly), vendor-qualified |
| Level 2 (supervisory) | HMI, engineering workstations, SCADA servers | quarterly or at planned outages, vendor-qualified list only |
| Level 0/1 (controllers, field devices) | PLCs, RTUs, drives, safety systems | firmware at turnaround/outage, after vendor advisory and site testing |
| Unpatchable legacy | XP HMIs, unsupported controllers | compensating controls, replacement plan |

## Process
1. **Vendor qualification**: automation vendors (Siemens, Rockwell, ABB, Emerson, Honeywell, ...)
   publish lists of Microsoft and third-party patches tested with their product versions.
   Install only what's qualified for your exact release.
2. **Test**: on a staging/FAT system or a redundant node first (e.g. standby SCADA server),
   with the process engineer present.
3. **Window**: tie to production schedule; switch redundant pairs (patch standby, fail over,
   patch the other).
4. **Backup first**: images of HMIs/servers and controller program backups.
5. **Change record** includes process risk assessment and rollback.

## When you can't patch
Compensating controls (document in the risk register with review dates):
- Network segmentation per zones/conduits, allow-list firewalls between levels, no direct
  internet, remote access via brokered jump host with MFA.
- Application allow-listing on HMIs/EWS, USB control, disable unused services.
- Monitoring: passive OT IDS (asset and anomaly detection).
- CISA ICS advisories (ICSA-) mapped to your inventory.

## Gotchas
- Automatic updates on OT Windows hosts must be **disabled**; patch distribution via an
  OT WSUS in the DMZ, not internet.
- Reboots can stop a process: confirm with operations even for "rebootless" updates.
- Antivirus definition updates also need vendor qualification on some systems.

## Verify
Inventory by level shows patch state vs vendor-qualified baseline; every unpatched known
vulnerability has a documented compensating control and owner.
