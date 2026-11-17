---
id: computing-software.database-administration.oracle-database.ocr-and-voting-disk-management
name: ocr-and-voting-disk-management
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, rac, real-application-clusters, ocr-backup, voting-disk, ocrconfig, crsctl, grid-infrastructure]
level: advanced
status: docs-checked
description: "Protect Oracle Clusterware's OCR and voting files: check integrity, manual and automatic OCR backups, mirroring, moving to a new ASM disk group, and restoring OCR."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/cwadd/managing-oracle-cluster-registry-and-voting-files.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCR and voting disk management

- **OCR** (Oracle Cluster Registry): cluster configuration: resources, databases, services,
  VIPs, node apps. Stored in ASM (19c), with automatic backups.
- **Voting files**: heartbeat/membership arbitration. Count depends on ASM disk group
  redundancy: 1 (external), 3 (normal), 5 (high). Majority must be accessible or the node is evicted.

## Health
```bash
ocrcheck                          # integrity, location, space (run as root for full check)
ocrcheck -config
crsctl query css votedisk         # voting file locations and state
olsnodes -n -s -t
```

## OCR backups
Clusterware keeps automatic backups every 4 hours, daily and weekly on one node (in
`<GRID_HOME>/cdata/<cluster>/` or in a disk group if configured).
```bash
ocrconfig -showbackup                     # list automatic and manual backups
ocrconfig -manualbackup                   # before any cluster change (as root)
ocrconfig -backuploc +OCRVOTE             # change the OCR backup location
```
Copy the backup files off the cluster nodes as part of your backup routine.

## Mirroring / moving
```bash
ocrconfig -add +DATA2              # add an OCR location (up to 5)
ocrconfig -delete +OLDDG
crsctl replace votedisk +NEWDG     # moves all voting files to another disk group (as grid owner/root)
```
Moving OCR/voting files to a new disk group: create the disk group with the right redundancy,
then `ocrconfig -add`, `ocrconfig -delete`, `crsctl replace votedisk`. Do it after a manual
OCR backup.

## Restoring OCR (all copies lost or corrupt)
Outline (as root, follow the docs for your version exactly):
```bash
crsctl stop crs -f                         # on all nodes
crsctl start crs -excl -nocrs              # on one node: exclusive mode, ASM only
# recreate/mount the disk group if needed
ocrconfig -restore <GRID_HOME>/cdata/<cluster>/backup00.ocr
crsctl replace votedisk +OCRVOTE           # if voting files were lost too
crsctl stop crs -f
crsctl start crs                           # then on other nodes
cluvfy comp ocr -n all -verbose
```

## Gotchas
- Never manipulate OCR with direct file tools; use ocrconfig/srvctl.
- Voting file count is tied to disk group redundancy; an external-redundancy disk group gives
  a single voting file: a single point of failure unless storage-level protection is trusted.
- After restoring OCR, resources registered after that backup (new services, databases) must
  be re-added with srvctl.

## Verify
`ocrcheck` reports success for its integrity checks; `crsctl query css votedisk` shows the expected number of ONLINE voting files;
`ocrconfig -showbackup` lists a recent backup copied off-cluster.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: automatic OCR backups every four hours, ocrconfig -manualbackup / -backuploc / -showbackup / -add (up to five locations), crsctl replace votedisk, crsctl start crs -excl -nocrs (Clusterware Administration and Deployment Guide).

Removed or corrected: ocrconfig -export, the 12.2+ remark, failure-group requirements and the exact ocrcheck success strings (not found in the cited pages).

Method: documentation only; no commands were run.
