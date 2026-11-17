---
id: computing-software.cloud-infrastructure-engineering.minio.replication-deletes
name: replication-deletes
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, replication-deletes, delete-marker-replication, pending-delete, lifecycle-expiry-not-replicated, prefix-trimming, xminio-replication-status]
level: advanced
status: docs-checked
description: "How MinIO replicates versioned deletes and delete markers, the PENDING state, duplicate markers in active-active, and why lifecycle expiry and prefix trimming need matching setup."
sources: ["https://github.com/minio/docs/blob/main/source/administration/bucket-replication.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO replication of deletes

Delete replication must be enabled explicitly: `--replicate delete,delete-marker` (either or both) on `mc replicate add` or `update`.

- **Delete markers.** Replication starts after a delete creates the marker; status is tracked in `X-Minio-Replication-DeleteMarker-Status`. In active-active setups both clusters may create duplicate markers if they delete concurrently or if one was down before the event synced.
- **Specific version deletes.** The version is marked `PENDING` until the remote has deleted it, and only then deleted on the source. This keeps versions near-synchronised but a listing may still show the version after the initial delete. Status field: `X-Minio-Replication-Delete-Status`.
- **Only explicit client deletes replicate.** Objects removed by lifecycle expiration rules are not replicated; in active-active, put the same expiration rules on *all* replicated buckets.
- **Prefix trimming.** When deleting the last object in a prefix, MinIO removes empty implicit prefixes up to the bucket root (not prefixes created explicitly, e.g. with `mc mb`). With delete replication on, the destination applies the same trimming. Example: removing the only objects under `photos/2021/january` and `/february` trims those and `/2021`, while an explicitly created `photos/NYE21` stays.

Related: `computing-software.cloud-infrastructure-engineering.minio.delete-markers`, `computing-software.cloud-infrastructure-engineering.minio.mc-replicate-add`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Bucket Replication page, Replication of Delete Operations and prefix trimming sections (bucket-replication.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
