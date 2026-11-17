---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.weed-mini-quickstart
name: weed-mini-quickstart
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [s3, dev, weed-mini, all-in-one, quick-start]
level: intro
status: docs-checked
description: "Start a single-process SeaweedFS with weed mini: master, volume, filer, S3, WebDAV and Admin UI, with seeded credentials and a pre-created bucket."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Quick-Start-with-weed-mini
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# weed mini quickstart

Goal: a working S3 endpoint in one command.

```bash
AWS_ACCESS_KEY_ID=admin AWS_SECRET_ACCESS_KEY=secret S3_BUCKET=my-bucket weed mini -dir=/path/to/data
aws --endpoint-url http://localhost:8333 s3 ls s3://my-bucket/
```

`-dir` is required. The credentials seed the `mini` user; omit them and S3 starts in unauthenticated "Allow All" mode (development only). `S3_BUCKET` (or `-bucket`) pre-creates buckets, comma-separated, idempotent. `S3_TABLE_BUCKET` / `-tableBucket` does the same for table buckets.

Default endpoints: S3 8333, master UI 9333, volume 9340, filer 8888, WebDAV 7333, Admin UI 12535, Iceberg REST catalog 8181.

Change ports with `-master.port=9444 -s3.port=8334`. Behind a reverse proxy add `-s3.externalUrl=https://s3.example.com` so signatures verify.

Versus `weed server -filer -s3`: mini runs a single master only (no Raft peers), auto-tunes volume size (64-1024 MB), and bundles the Admin UI and maintenance worker. Use the multi-component setup for HA masters or separate hosts. Defaults may change between releases, so pin the version or pass flags explicitly.

Verify: the aws `ls` returns without error and http://localhost:9333 shows the cluster.

## Checked
Checked 2026-11-09: every default port, the seeded `mini` user, bucket and table-bucket variables, `-s3.externalUrl`, the single-master and 64-1024 MB auto-tuning claims and the comparison with `weed server -filer -s3` all match the page. Dropped the Getting-Started source (not read).
Method: docs-checked 2026-11-09 against the SeaweedFS wiki page Quick-Start-with-weed-mini, read in full from a local clone of the wiki.
