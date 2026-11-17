---
id: computing-software.cloud-infrastructure-engineering.minio.replication-resync
name: replication-resync
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, replication-resync, mc-replicate-resync, disaster-recovery, resynchronize, existing-object-replication, remote-bucket-arn, tiered-objects]
level: advanced
status: docs-checked
description: "Rebuild a damaged MinIO bucket from a healthy replica with mc replicate resync start and status: per-bucket scope, load warnings, one job per bucket, tiering side effect."
sources: ["https://github.com/minio/docs/blob/main/source/administration/bucket-replication/server-side-replication-resynchronize-remote.rst", "https://github.com/minio/docs/blob/main/source/administration/bucket-replication.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO replication resynchronization

Resync uses a healthy replica to rebuild a deployment after partial or total data loss.

## Requirements
- Source and target both online and able to read and write, with full connectivity.
- The healthy source must already have a replication config for the damaged bucket, created with the `existing-objects` feature.
- Matching encryption, MinIO-to-MinIO same version, versioning, and (if used) object locking configured on the target bucket beforehand.
- Per-bucket: repeat for every bucket that lost data. Only one resync job per bucket at a time. There is no prefix-level granularity.

## Procedure
1. Direct load balancers to the healthy cluster only until resync finishes.
2. `mc replicate ls SOURCE/BUCKET` to find the remote target ARN.
3. Start: `mc replicate resync start --remote-bucket "arn:minio:replication::UUID:BUCKET" SOURCE/BUCKET`. It returns a job ID.
4. Track with `mc replicate resync status ALIAS/BUCKET`; Status becomes `Completed`.

## Behaviour
Every source object matching a rule with existing-object replication is queued regardless of its current replication status, but objects whose remote copy already matches exactly (including metadata) are skipped. A large bucket can cause a significant jump in replication load and traffic, so use it only when necessary.

## Tiering warning
For buckets with tiering, resync restores objects in a non-transitioned state with no transition metadata, so data previously on the remote tier becomes permanently disconnected. If the tier used an explicit readable prefix, that prefix can be purged to avoid paying for orphaned data.

See `computing-software.cloud-infrastructure-engineering.minio.tiering`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Resynchronize Bucket from Remote Replica page and Bucket Replication page resynchronization section. Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
