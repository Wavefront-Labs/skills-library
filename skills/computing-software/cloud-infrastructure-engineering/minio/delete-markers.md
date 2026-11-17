---
id: computing-software.cloud-infrastructure-engineering.minio.delete-markers
name: delete-markers
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, delete-markers, deletemarker, idempotent-delete, version-delete, permanent-delete, mc-ls-versions]
level: practitioner
status: docs-checked
description: "Understand MinIO versioned deletes, 0-byte DeleteMarkers, idempotent delete markers since 2022-08-22, and permanent deletion of a specific version with its version ID."
sources: ["https://github.com/minio/docs/blob/main/source/administration/object-management/object-versioning.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO delete markers in versioned buckets

A `DELETE` without a version ID on a versioned object creates a 0-byte `DeleteMarker` as the latest version. Unversioned `GET`, `HEAD` and `LIST` skip delete markers by default, so the object looks deleted; to reach a prior version clients must pass version flags or IDs.

- **Idempotent markers.** Since RELEASE.2022-08-22T23-53-06Z, a delete with no version ID creates at most one delete marker. Standard S3 may stack multiple sequential markers; MinIO deliberately does not.
- **Deleting a specific version** (supplying its version ID) is permanent and does not create a marker.
- **Permanent cleanup.** Use lifecycle expiration rules, or manual deletes of non-current versions and markers.

## Commands
- `mc ls --versions` lists all versions including delete markers.
- `mc cp --version-id=UUID ...` retrieves the version of the "deleted" object.
- `mc rm --version-id=UUID ...` deletes that version.
- `mc rm --versions` deletes all versions of an object.

## With object locking
Delete markers are not eligible for WORM protection. An unversioned delete of a locked object succeeds and adds a marker, while explicitly deleting a locked version fails with a "WORM protected" error (`computing-software.cloud-infrastructure-engineering.minio.object-locking`).

Background: `computing-software.cloud-infrastructure-engineering.minio.bucket-versioning`.

## Checked

2026-11-03. Confirmed against the MinIO docs source: object-versioning and object-retention pages: delete marker behaviour, idempotent markers, version commands, WORM interaction. Removed or fixed: nothing.

Method: documentation only; no commands were run.
