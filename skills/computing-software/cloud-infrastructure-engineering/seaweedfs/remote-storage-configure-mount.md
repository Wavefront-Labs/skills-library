---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.remote-storage-configure-mount
name: remote-storage-configure-mount
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [remote-configure, remote-mount, lazy-metadata, cloud-drive]
level: advanced
status: docs-checked
description: "Attach S3, GCS, Azure or compatible remote storage with remote.configure, then remote.mount it eagerly or lazily with listing cache, plus write-back sync."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Configure-Remote-Storage
  - https://github.com/seaweedfs/seaweedfs/wiki/Mount-Remote-Storage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# remote storage configure mount

Configure a named remote in `weed shell` (types include s3, gcs, azure, b2, wasabi, storj, filebase, aliyun, tencent, baidu):
```
remote.configure -name=cloud1 -type=s3 -s3.access_key=xxx -s3.secret_key=yyy -s3.storage_class="STANDARD"
remote.configure -name=cloud2 -type=gcs -gcs.appCredentialsFile=/path/to/service-account.json
remote.configure -name=cloud3 -type=azure -azure.account_name=xxx -azure.account_key=yyy
remote.configure -name=other -type=s3 -s3.endpoint=zzz -s3.force_path_style=true -s3.v4_signature=false
```
The default S3 storage class is `STANDARD_IA`.

Mount a bucket or a subdirectory:
```
remote.mount -dir=/xxx -remote=cloud1/bucket/dir1
remote.mount -dir=/xxx -remote=cloud1/bucket -metadataStrategy=lazy -listingCacheTTL=300
```
`-metadataStrategy` is `eager` (default, pull all metadata now) or `lazy` (fetch on first access). `-listingCacheTTL` of 0 disables on-demand listing; greater than 0 lists from the remote and caches that many seconds. `-nonempty` allows mounting over a non-empty directory.

Push local writes back to the remote with a separate long-running process:
```bash
weed filer.remote.sync -filer=localhost:8888 -dir=/xxx
```
Gotcha: files are stored as-is in the bucket, so no filer encryption applies.

Verify: `ls` on the filer path shows remote objects; write a file and see it in the bucket after sync.

## Checked
Checked 2026-11-09: the vendor type list, all four remote.configure examples, the STANDARD_IA default, remote.mount flags and defaults, eager versus lazy and listingCacheTTL semantics, and the separate filer.remote.sync write-back process match the pages. The no-encryption gotcha is supported by the Cloud Drive note on the Cloud-Tier page.
Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Configure-Remote-Storage and Mount-Remote-Storage (read in full) and the Cloud-Tier page, from a local clone of the wiki.
