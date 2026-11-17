---
id: computing-software.cloud-infrastructure-engineering.thanos.objstore-configuration
name: objstore-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-objstore, objstore-config, bucket-config, supported-providers]
level: intro
status: docs-checked
description: "Pass one object storage config to every Thanos component and pick a supported provider."
sources: ["https://thanos.io/tip/thanos/storage.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Object storage configuration

Each Thanos component reads exactly one bucket from `--objstore.config-file` or `--objstore.config` (inline YAML, preferred by the docs because it gives an explicit static view per component). There is no way to configure multiple buckets in one component.

Supported clients: Google Cloud Storage and AWS S3 and S3-compatible stores such as MinIO (stable, production), Azure (stable), OpenStack Swift (beta), Tencent COS, AliYun OSS, Baidu BOS, Oracle Cloud Infrastructure Object Storage, and a local filesystem client.

```yaml
type: GCS
config:
  bucket: "my-thanos-bucket"
prefix: ""
```

`prefix` lets you separate blocks from different sources under path prefixes, so the origin is visible without Thanos tooling.

The filesystem type (`type: FILESYSTEM`, `config.directory`) is experimental, can be inefficient, and is not advised as the main production store.

Swift has a default 5 GiB maximum file size.

**Verify.** `thanos tools bucket ls --objstore.config-file bucket.yml` lists blocks without error.

## Checked

2026-11-08. Read the raw Thanos docs page behind the cited URL (docs/storage.md): the single-bucket note, the supported-clients table and maturity levels, the S3, OpenStack Swift (5 GiB limit) and Filesystem (experimental) sections, and the prefix field. Partial read: the GCS, Azure, COS, OSS, BOS and OCI config sections were not read in full; no claims here depend on them beyond their being listed. Nothing removed.

Method: documentation only; no commands were run.
