---
id: computing-software.systems-network-administration.backup-and-recovery.tape-library-partitioning
name: tape-library-partitioning
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [library-partitioning, tape-library, logical-library, tape, control-path, medium-changer]
level: advanced
status: draft
description: "Partition a physical tape library into logical libraries: assign drives, slots and I/E stations, control path drives, barcode policies, FC zoning, and backup app configuration."
sources:
  - https://www.ibm.com/docs/en/ts4500-tape-library?topic=library-logical-libraries
  - https://support.hpe.com/hpesc/public/docDisplay?docId=c03541579
  - https://www.quantum.com/en/products/tape-storage/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tape library partitioning

**Goal:** one physical library shared by several backup applications, tenants or sites, each seeing its own independent library.

## Concepts
- A **logical library (partition)** has its own drives, storage slots, (optionally) I/E slots, and a medium changer device presented to hosts.
- The changer is presented through a **control path drive** (one or two drives per partition carry the changer LUN) or a dedicated robotic control path in some models.
- Each backup app sees only its partition; robots are shared transparently.

## Setup steps (similar on IBM TS4300/TS4500, HPE MSL/StoreEver, Quantum Scalar)
1. Plan: drives and slots per partition from each app's needs (concurrent jobs, retention capacity); leave spare slots.
2. Library web UI: create partitions, assign drives, assign slot ranges or let the library allocate by barcode (some models assign by barcode prefix/range).
3. Enable control path on at least one drive per partition (two for failover where supported).
4. I/E slots: assign to a partition or set as shared (operator chooses at import).
5. Cleaning: auto-clean managed by the library or by the application; choose one, not both.
6. FC/SAS zoning: zone each partition's drives only to its backup servers.
7. On each backup server: rescan (`lsscsi -g`, Windows Device Manager), configure the new changer and drives in the app (`proxmox-tape changer create`, Veeam tape server rescan, Bacula Autochanger resource).

## Gotchas
- Moving a tape between partitions requires export/import or a library admin move; apps will not see each other's media.
- Firmware upgrades affect all partitions at once; coordinate downtime.
- Drive serials map changer drive numbers; verify the drive order in each app against the library (`mtx -f /dev/sgX status` plus drive serials).

## Verify
Each app inventories only its slots and loads tapes into its own drives; a load from one app never appears in another's drives.
