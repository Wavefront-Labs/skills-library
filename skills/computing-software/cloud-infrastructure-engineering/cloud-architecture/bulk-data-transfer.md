---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.bulk-data-transfer
name: bulk-data-transfer
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, storage-selection, bulk-data-transfer, snowball, data-box, transfer-appliance, datasync]
level: practitioner
status: draft
description: "Move bulk data to cloud: online (DataSync, AzCopy, Storage Transfer Service) vs offline appliances, transfer-time maths, verification, cutover delta and chain of custody."
sources: ["https://docs.aws.amazon.com/snowball/latest/developer-guide/whatisedge.html", "https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html", "https://learn.microsoft.com/azure/databox/data-box-overview", "https://cloud.google.com/transfer-appliance/docs/4.0/overview", "https://cloud.google.com/storage-transfer-service"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bulk data transfer (appliances / online transfer)

## Steps
1. **Do the maths**: time = data / effective bandwidth. 100 TB over a 1 Gbps link at 80%
   utilisation is about 12-13 days; 1 PB over 10 Gbps is a similar order. If that exceeds the
   window or saturates business traffic, consider appliances.
2. **Online tools**: AWS DataSync (agents, NFS/SMB/HDFS/object, verification, scheduling),
   AzCopy / Azure Storage Mover, Google Storage Transfer Service (agents for on-prem), rclone
   for cross-cloud. Throttle during business hours.
3. **Offline**: AWS Snowball Edge (check current device availability per region), Azure Data
   Box / Data Box Heavy, Google Transfer Appliance. Factor shipping and ingest time (often a
   week or two end to end).
4. **Verification**: checksums at source and destination (tools verify on copy; spot-check
   with your own hashes), object counts and byte totals.
5. **Delta and cutover**: seed with bulk copy or appliance, then online incremental syncs
   until a final short cutover sync.
6. **Security and custody**: encryption keys you hold, chain-of-custody records, device wipe
   certificates.

## Gotchas
- Millions of small files are bound by per-file overhead, not bandwidth; package or parallelise.
- Forgetting permissions/metadata (ACLs, timestamps) breaks apps after the move.

## Verify
- [ ] Checksums and counts reconciled.
- [ ] Final delta sync completed within the cutover window.
