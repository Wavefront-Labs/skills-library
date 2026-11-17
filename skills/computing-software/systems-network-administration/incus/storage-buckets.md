---
id: computing-software.systems-network-administration.incus.storage-buckets
name: storage-buckets
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, storage-bucket, s3, object-storage, access-key, cephobject, bucket-keys]
level: practitioner
status: docs-checked
description: "Provide S3 object storage with Incus buckets: core.storage_buckets_address, create/set/delete, size quota, cluster behaviour and access keys with admin or read-only roles."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/storage_buckets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage buckets

Local pools (`dir`, `btrfs`, `lvm`, `zfs`) need an S3 address: `incus config set core.storage_buckets_address=:8555`.

```
incus storage bucket create <pool> <bucket> [--target=<member>] [options]
incus storage bucket set <pool> <bucket> size=<new_size>
incus storage bucket list|show <pool> [<bucket>]
incus storage bucket delete <pool> <bucket>
incus storage bucket key create <pool> <bucket> <key> [--role=admin]
incus storage bucket key list|show|edit|delete <pool> <bucket> [<key>]
```

- No quota by default; a bucket cannot shrink below its used size.
- Deleting a bucket deletes its keys.
- Keys: a generated access key and secret key. Role `admin` has full access; `read-only` (default) lists and gets only.
- Cluster: on local pools a bucket lives on one member, unreplicated, and S3 works only via that member; names must be unique or use `--target`. For HA use `cephobject` pools.

## Checked

2026-11-04: confirmed against the Incus storage buckets how-to (S3 address, create/set/delete/list/show, size quota and shrink limit, cluster behaviour, key roles and default). Nothing removed.

Method: documentation only; no commands were run.
