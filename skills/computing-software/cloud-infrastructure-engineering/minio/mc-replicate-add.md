---
id: computing-software.cloud-infrastructure-engineering.minio.mc-replicate-add
name: mc-replicate-add
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, mc-replicate-add, replicate, remote-bucket, existing-objects, metadata-sync, sync-replication, bandwidth, priority, mc-replicate-update]
level: advanced
status: docs-checked
description: "Create MinIO replication rules with mc replicate add: --remote-bucket, --replicate flags, --priority, --sync, --tags and bandwidth limits."
sources: ["https://github.com/minio/docs/blob/main/source/reference/minio-mc/mc-replicate-add.rst", "https://github.com/minio/docs/blob/main/source/administration/bucket-replication/enable-server-side-one-way-bucket-replication.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mc replicate add

Creates a server-side replication rule on a bucket. The remote bucket must be a MinIO deployment on the same version. It also creates the replication target automatically, so the deprecated `mc admin bucket remote add` is not needed.

```
mc replicate add myminio/mydata \
   --remote-bucket https://user:secret@minio.mysite.tld:9001/bucket \
   --replicate "delete,delete-marker,existing-objects"
```
Since mc RELEASE.2024-03-03T00-13-08Z `--remote-bucket` can be an alias path such as `minio-target/my-bucket`.

## Flags
- `--replicate` - comma list: `delete`, `delete-marker`, `existing-objects`, `metadata-sync` (active-active only; omitting it stops metadata-only changes replicating back). If not specified, all are enabled.
- `--priority` - integer, unique per source bucket rule; higher wins; default `0`.
- `--sync` - synchronous replication for this target; default is asynchronous.
- `--tags "K=V&K2=V2"` - only objects with the tags replicate.
- `--bandwidth`, `--limit-upload`, `--limit-download` - rate caps with units such as `Ki`, `Gi`, `G`; unlimited by default.
- `--healthcheck-seconds` (default 60), `--id`, `--region`, `--storage-class`, `--path on|off|auto` (default `auto`), `--disable` (rule created disabled; existing objects must be explicitly enabled later), `--disable-proxy` (active-active proxying is on by default).

## Managing rules
- `mc replicate update --replicate` modifies a rule and enables features such as `existing-objects` on a disabled rule. You must specify all desired replication features when editing a rule.
- Replication of existing objects needs `mc` RELEASE.2021-06-13T17-48-22Z and `minio` RELEASE.2021-06-07T21-40-51Z or later.
- Lifecycle expiration deletes are not replicated; only explicit client deletes. SSE-C objects are not replicated, and both buckets need SSE-S3 enabled to replicate encrypted objects.

Enable versioning on both buckets first with `mc version enable ALIAS/PATH` (`computing-software.cloud-infrastructure-engineering.minio.bucket-replication`).

## Checked

2026-11-03. Confirmed against the MinIO docs source: mc-replicate-add page: syntax, every flag and default, the 2024-03-03 alias form, existing-objects, metadata sync, delete and encryption behaviour. Removed or fixed: the PUT-before-queue detail, `mc replicate ls/rm`, `mc stat` and `--state` advice (not on the page); fixed `--path` values and the versioning command.

Method: documentation only; no commands were run.
