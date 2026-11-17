---
id: computing-software.cloud-infrastructure-engineering.minio.replication-sync-async
name: replication-sync-async
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, replication-sync-async, synchronous-replication, asynchronous-replication, replication-queue, mc-admin-bucket-remote-add]
level: practitioner
status: docs-checked
description: "Pick synchronous or asynchronous MinIO replication, understand client PUT semantics for each, and where the sync option is set on the remote target."
sources: ["https://github.com/minio/docs/blob/main/source/administration/bucket-replication.rst", "https://github.com/minio/docs/blob/main/source/includes/common-replication.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO synchronous vs asynchronous replication

MinIO lets you choose per remote target.

- **Asynchronous (default).** MinIO completes the originating `PUT` *before* placing the object in the replication queue. The client may see success before replication has happened, so the remote can briefly be stale or missing objects. The benefit is that slow or loaded replication does not slow writes.
- **Synchronous.** MinIO attempts to replicate *before* completing the `PUT`, but still returns success whether or not that attempt succeeded. The docs list reduced risk of slow writes at a possible cost of stale or missing objects as the trade-off.

## How to enable
Synchronous replication must be enabled explicitly when defining the remote target. `mc replicate add --sync` does it for a new rule; the older `mc admin bucket remote add` command exposes a sync flag as well (that command is deprecated in favour of `mc replicate add`).

See `computing-software.cloud-infrastructure-engineering.minio.mc-replicate-add`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: mc replicate add reference (--sync), Bucket Replication page and the replication include. Removed: the claim that mc stat shows the replication stage (not on these pages).
Method: documentation only; no commands were run.
