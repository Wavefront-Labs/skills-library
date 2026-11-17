---
id: computing-software.cloud-infrastructure-engineering.zot.storage-subpaths
name: storage-subpaths
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, subpaths, multiple-storage, per-path-config, remote-subpaths]
level: advanced
status: docs-checked
description: "Serve several filesystems or backends from one Zot using storage.subPaths, with per-subpath settings, separate drivers, and cautions for retention and CVE."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/storage.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/cve-scanning.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/retention.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`storage.subPaths` maps path keys (for example `/a`, `/b`) to separate filesystems or backends, all appearing as one registry over HTTP with no client difference.

```json
"storage": {
  "rootDirectory": "/tmp/zot",
  "subPaths": { "/infra": { "rootDirectory": "/tmp/zot1" }, "/apps": { "rootDirectory": "/tmp/zot2" } }
}
```

- Each entry can set its own `rootDirectory`, `dedupe`, `gc`, `storageDriver`, `redirectBlobURL`, `hydrateBlobOnRead` and so on. Different storage drivers per subpath are supported.
- `maxRepoBytes` on a subpath does not inherit the top-level value.
- A subpath can carry its own retention config; its `gcDelay` defaults to 1h in the docs example.
- With CVE scanning, each storage path gets its own `_trivy` directory and database.
- Use cases: serve existing OCI images from different backends, or expand storage with separate backing stores.

Warning: `subPaths` is a separate feature and should not be used just to configure retention.

The docs spell it `subpaths` in one place and `subPaths` in examples; use `subPaths`.

## Checked

2026-11-04. Read against the zot storage planning article (subpaths), CVE scanning and retention articles; every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
