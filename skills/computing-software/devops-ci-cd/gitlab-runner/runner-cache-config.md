---
id: computing-software.devops-ci-cd.gitlab-runner.runner-cache-config
name: runner-cache-config
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [cache, runners-cache, s3, gcs, azure]
level: practitioner
status: docs-checked
description: "Configure the distributed cache in [runners.cache] for S3, GCS or Azure."
sources: ["https://docs.gitlab.com/runner/configuration/advanced-configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Distributed cache configuration

`[runners.cache]` sets the cache backend:
- `Type`: `s3`, `gcs` or `azure`.
- `Path` is prepended to the cache URL; `Shared` enables cache sharing between runners (default `false`).

For S3, `[runners.cache.s3]` takes the server address, credentials, bucket name, region, and optional `RoleARN`. `AssumeRoleMaxConcurrency` is also available there.

GCS and Azure have their own `[runners.cache.gcs]` and `[runners.cache.azure]` sections.

Choose the archive format with the `CACHE_COMPRESSION_FORMAT` variable: `zip`, `tarzstd` or `zipzstd`.

## Checked

2026-11-03. Confirmed against Type, Path, Shared, S3 options and CACHE_COMPRESSION_FORMAT on Advanced configuration. Removed: the unconfirmed AssumeRoleMaxConcurrency default and the generic closing sentence.

Method: documentation only; no commands were run.
