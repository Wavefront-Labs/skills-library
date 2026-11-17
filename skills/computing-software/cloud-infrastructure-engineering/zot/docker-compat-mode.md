---
id: computing-software.cloud-infrastructure-engineering.zot.docker-compat-mode
name: docker-compat-mode
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, docker-compat, docker2s2, preserve-digest, docker-schema2]
level: practitioner
status: docs-checked
description: "Enable Docker schema 2 manifest support in Zot with http.compat docker2s2, when it is required, and what changed for sync and preserveDigest."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/admin-guide/admin-configuration.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/mirroring.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Zot accepts OCI format only; Docker schema 2 manifests are rejected on push. Enable compat in the `http` block:

```json
"http": { "address": "127.0.0.1", "port": "8080", "compat": ["docker2s2"] }
```

The array must contain the exact string `docker2s2`; aliases are not accepted.

Enable it when:
- clients push Docker schema 2 manifests,
- you mirror Docker-format images (for example Docker Hub),
- mirrored images carry cosign or notation signatures tied to Docker manifest digests.

Since v2.1.22:
- Sync preserves upstream media types and digests and rejects Docker schema 2 content unless `http.compat` is set.
- The sync `preserveDigest` setting is deprecated and ignored; remove it from new configs. Digests are always preserved.

A Docker-compatible pull-through cache combines `http.compat` with sync `onDemand: true` (see the `config-docker-compat-sync.json` example in the Zot repository). Omit compat only when all synced content is OCI-formatted.

## Checked

2026-11-04. Read against the zot admin configuration (compatibility section) and mirroring article; every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
