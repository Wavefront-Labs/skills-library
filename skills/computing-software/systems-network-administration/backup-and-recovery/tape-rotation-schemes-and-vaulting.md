---
id: computing-software.systems-network-administration.backup-and-recovery.tape-rotation-schemes-and-vaulting
name: tape-rotation-schemes-and-vaulting
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [tape-rotation, tape-vaulting, gfs, tower-of-hanoi, offsite-storage, chain-of-custody, tape]
level: practitioner
status: draft
description: "Design tape rotation and vaulting: GFS and other schemes, cartridge counts, off-site vault schedules, chain-of-custody records, recall times and encryption for transit."
sources:
  - https://www.bacula.org/15.0.x-manuals/en/main/Automated_Disk_Backup.html
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tape rotation schemes and vaulting

**Goal:** enough tapes, cycling predictably, with the right ones off-site and retrievable within the RTO.

## Schemes
| Scheme | Pattern | Use |
|---|---|---|
| GFS (grandfather-father-son) | Daily (son) sets reused weekly; weekly (father) reused monthly; monthly (grandfather) kept for months/years | Most common; maps to retention policy |
| Tower of Hanoi | Sets used at doubling intervals (A every 2 days, B every 4, C every 8...) | Long history with few tapes; harder to manage |
| Simple weekly rotation | N weekly sets cycling | Small sites |

## Cartridge count (GFS example)
Daily: 6 sets; weekly: 4 sets; monthly: 12 sets; yearly: 7 sets. Multiply each set by tapes per full/incremental (data size / native capacity / fill efficiency) and add 20% spare. Tape software (Veeam GFS media pools, Bacula pools) enforces the overwrite rules.

## Vaulting
- Weekly and monthly sets go off-site promptly (e.g. next business day) via a vaulting provider or a second site.
- Track every cartridge: barcode, set, date written, location, expiry. Tape software vault features or a vault register.
- Return schedule: expired tapes come back for reuse; recall SLA for emergencies (e.g. 4 hours) written into the contract and tested.
- **Chain of custody**: signed handover at pickup and delivery, sealed transit cases, discrepancies investigated.

## Security
Encrypt all tapes leaving the site (LTO hardware encryption managed by the backup software); keys escrowed separately from tapes.

## Gotchas
- Vault inventory drifts from software inventory; reconcile monthly.
- Recalling the wrong set during an incident wastes hours; label sets clearly and practise recalls.

## Verify
Monthly reconciliation of vault provider inventory with backup software matches 100%, and an annual recall test meets the SLA.
