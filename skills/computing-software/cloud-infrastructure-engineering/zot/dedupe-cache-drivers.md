---
id: computing-software.cloud-infrastructure-engineering.zot.dedupe-cache-drivers
name: dedupe-cache-drivers
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, cache-driver, boltdb, dynamodb, remote-cache, dedupe]
level: advanced
status: docs-checked
description: "Choose a Zot cache driver for dedupe tracking: default BoltDB, or DynamoDB with its required table names for multi-instance and search deployments."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/storage.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/scaleout.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cache drivers track duplicate blobs when `dedupe` is enabled.

BoltDB (default): used when no cache driver is set; stored as `cache.db` in the root directory or subpath root. It does not support concurrent writes, so multiple Zot instances or replicas are not supported.

DynamoDB: set `dedupe`, `remoteCache: true` and a `cacheDriver`:

```json
"cacheDriver": { "name": "dynamodb", "endpoint": "...", "region": "...", "cacheTablename": "..." }
```

- The AWS SDK loads extra config and credentials from the environment and shared AWS files.
- With the search extension enabled, these table names are also required: `userDataTablename`, `apiKeyTablename`, `repoMetaTablename`, `imageMetaTablename`, `repoBlobsInfoTablename`, `versionTablename`.
- Required actions cover table management, scan, batch get, get, update and delete. `DeleteTable` is only needed for tests.

Scale-out cluster samples use `dedupe: false`, `remoteCache: true`, an S3 `storageDriver` and either this DynamoDB driver or the Redis driver (see the Redis skill).

## Checked

2026-11-04. Read against the zot storage planning article and scale-out article; every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
