---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.remote-cache-uncache-gateway
name: remote-cache-uncache-gateway
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [remote-cache, remote-gateway, createbucketat, uncache, warm-up]
level: advanced
status: docs-checked
description: "Warm or free local copies of remote objects with remote.cache/remote.uncache, and mirror whole buckets with weed filer.remote.gateway."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Cache-Remote-Storage
  - https://github.com/seaweedfs/seaweedfs/wiki/Gateway-to-Remote-Object-Storage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# remote cache uncache gateway

After a remote is mounted you can already read and write files in the mounted directory (content is cached lazily). To warm or free content explicitly, in `weed shell`:
```
remote.cache -dir=/xxx/sub -include=*.pdf
remote.cache -maxSize=1024000 -maxAge=3600
remote.uncache -dir=/xxx -minSize=1024000 -minAge=3600
```
`remote.cache` copies content in parallel through volume servers and skips files already in sync; `remote.uncache` keeps metadata, drops local content, and skips files not synced to the remote (no data loss). Both are meant to run from cron.

Gateway mode mirrors the `/buckets` tree to a remote store:
```
> remote.mount.buckets -remote=cloud1 -apply       # optional: import existing remote buckets
$ weed filer.remote.gateway -createBucketAt=cloud1
$ weed filer.remote.gateway -createBucketAt=cloud1 -createBucketWithRandomSuffix
```
New local buckets are created in the remote, deleted ones are deleted there, and local changes under mounted buckets upload. It can be paused and resumed; changing `-createBucketAt` affects only new buckets. Use `-createBucketWithRandomSuffix` (name-xxxx) where bucket names must be globally unique.

Verify: create a bucket via S3 and confirm it appears in the remote.

## Checked
Checked 2026-11-09: the remote.cache and remote.uncache examples and skip behaviour, the gateway command and its three mirroring rules, optional remote.mount.buckets, pause and resume, `-createBucketAt` effect and the random suffix option match both pages. Reworded the lazy-read sentence to what the page says.
Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Cache-Remote-Storage and Gateway-to-Remote-Object-Storage, both read in full from a local clone of the wiki.
