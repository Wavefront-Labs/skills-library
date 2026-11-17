---
id: computing-software.systems-network-administration.backup-and-recovery.source-vs-target-dedupe-appliances
name: source-vs-target-dedupe-appliances
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [dedupe-appliance, data-domain, source-side-deduplication, target-side-deduplication, dd-boost, storeonce]
level: advanced
status: draft
description: "Choose and integrate deduplication appliances: source vs target dedupe, Data Domain DD Boost and StoreOnce Catalyst, restore speed limits, and immutability features."
sources:
  - https://www.dell.com/support/kbdoc/en-us/000017262
  - https://www.hpe.com/us/en/storage/storeonce.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Source vs target dedupe appliances

## Concepts
- **Target-side dedupe**: backup software sends full data, the appliance dedupes on ingest. Simple, but network carries everything.
- **Source-side (client) dedupe**: the backup server or agent asks the appliance which segments exist and sends only new ones (DD Boost, StoreOnce Catalyst). Cuts network 80-95% and enables fast synthetic fulls via virtual synthetics.
- Global dedupe ratios of 10-50x are typical for repetitive full backups; incremental-forever chains show lower ratios.

## Integrating with backup software
- Use the vendor protocol (DD Boost, Catalyst) not CIFS/NFS: faster, supports synthetic operations on the appliance, and avoids share-level ransomware exposure.
- Send uncompressed, unencrypted data (decompress on the repository); encrypt with the appliance's at-rest encryption instead, as backup-side encryption kills dedupe.
- Per Veeam guidance: use the appliance for longer retention, and a fast disk repository for the most recent points and instant recovery.

## Restore and instant recovery limits
Dedupe appliances rehydrate on read: random I/O for instant VM recovery is slow. Plan RTO on primary disk landing zones, not on the appliance.

## Immutability
- Data Domain **Retention Lock** (Governance or Compliance mode) and DD Cyber Recovery vault.
- StoreOnce **Catalyst immutability** / Dual Authorization.
- Enable dual authorisation for deletes and protect the appliance admin interface with separate credentials and MFA.

## Gotchas
- Capacity planning is on post-dedupe size; a ratio drop (encrypted source data, compressed media) consumes space fast.
- Garbage collection/cleaning schedules must run to reclaim space after expiry.

## Verify
Ingest rate and dedupe ratio within expectations for a month; a test restore of a large VM meets RTO.
