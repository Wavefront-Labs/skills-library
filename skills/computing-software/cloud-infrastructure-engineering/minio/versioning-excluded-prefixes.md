---
id: computing-software.cloud-infrastructure-engineering.minio.versioning-excluded-prefixes
name: versioning-excluded-prefixes
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, versioning-excluded-prefixes, excluded-prefixes, mc-version-info, spark, hadoop, temporary-prefixes]
level: advanced
status: docs-checked
description: "Exclude up to 10 prefixes from MinIO versioning with mc version enable --excluded-prefixes, plus replication and locking limits and reading back via mc version info."
sources: ["https://github.com/minio/docs/blob/main/source/administration/object-management/object-versioning.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Excluding prefixes from MinIO versioning

Useful for Spark, Hadoop and similar workloads that first write objects under temporary prefixes.

```
mc version enable --excluded-prefixes "prefix1, prefix2" ALIAS/BUCKET
mc version enable --excluded-prefixes "_test, _temp" local/my-bucket
```
- Matching is like `prefix*`: it hits objects containing the string in their prefix or name. To match by prefix only, use `prefix/*`.
- Up to **10 prefixes per bucket**.
- Repeating the command replaces the previous list, so include every prefix you want to keep.
- Inspect the setting with `mc version info ALIAS/BUCKET --json`; excluded prefixes appear in the `ExcludedPrefixes` property of the `versioning` object.

## Restrictions
- Versioning is required for replication, so objects in excluded prefixes are **not replicated** to any peer or remote site.
- Excluding prefixes is not supported on buckets with object locking enabled.

See `computing-software.cloud-infrastructure-engineering.minio.bucket-versioning`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Object Versioning page, Exclude a Prefix From Versioning section (object-versioning.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
