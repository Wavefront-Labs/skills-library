---
id: computing-software.cloud-infrastructure-engineering.minio.bucket-versioning
name: bucket-versioning
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, bucket-versioning, mc-version-enable, version-id, null-version, versioned-objects, storage-capacity, mc-rm-versions]
level: practitioner
status: docs-checked
description: "Enable and reason about MinIO versioning with mc version enable: per-namespace uniqueness, UUID version IDs, the null version, storage growth and cleanup."
sources: ["https://github.com/minio/docs/blob/main/source/administration/object-management/object-versioning.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO bucket versioning

Versioning keeps multiple versions of an object. A write that would overwrite instead creates a new version with a unique version ID; the newest is the "latest" returned by default, and clients may list, read or delete a specific version. It is a prerequisite for object locking and for replication.

```
mc version enable ALIAS/BUCKET
```
Objects written before versioning was enabled (or while disabled or suspended) have the version ID `null`, which you can pass in S3 operations.

## Behaviour
- Uniqueness is per full namespace (bucket plus path): `databucket/object.blob` and `blobbucket/object.blob` are distinct.
- Version IDs are server-generated, immutable 128-bit UUIDv4 values; clients cannot choose them.
- Since RELEASE.2023-05-04T21-44-30Z, MinIO does not version explicit directory objects (prefixes); objects inside them still version normally.
- Storage: no incremental versioning. The docs' example: a 1 GB log with 100 MB appended daily for 10 days holds more than 14 GB. Since RELEASE.2024-04-18T19-09-19Z MinIO warns when the cumulative size of versions of one object exceeds 1 TiB.

## Cleanup
- Lifecycle expiration, for example expiring non-current versions 90 days after they become non-current.
- Manually: `mc rm --versions` removes all versions of an object; adding `--older-than` restricts by age. `mc ls --versions` shows versions and delete markers; `mc cp --version-id=UUID` fetches one; `mc rm --version-id=UUID` deletes one.

See `computing-software.cloud-infrastructure-engineering.minio.delete-markers` and `computing-software.cloud-infrastructure-engineering.minio.versioning-excluded-prefixes`.

## Checked

2026-11-03. Confirmed against the MinIO docs source: object-versioning page: version ID rules, null version, directory objects, storage example, 1 TiB warning, cleanup commands. Removed or fixed: nothing.

Method: documentation only; no commands were run.
