---
id: computing-software.cloud-infrastructure-engineering.zot.repository-quotas
name: repository-quotas
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, max-repo-bytes, repository-quota, max-repos, status-413, metadb]
level: advanced
status: docs-checked
description: "Limit repository size in Zot (v2.1.23+) with storage.maxRepoBytes, how bytes are counted, the 413 DENIED response, and subPaths interaction."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/storage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`storage.maxRepoBytes` (v2.1.23+) caps logical bytes per repository, not registry-wide. Zero or omission disables it. The docs example uses 10 GiB.

Accounting:
- Counts unique manifest, index, config and layer digests reachable from tags.
- Untagged content, referrers and signatures are excluded.
- Checked on manifest push. An over-limit push returns `413` with `DENIED`; the detail includes `current`, `projected` and `limit`.

Rules:
- Lowering the limit does not block pushes that do not increase size, and does not reclaim physical space.
- A matching `subPaths` entry uses its own value (including zero) and does not inherit the top-level one.
- Changes require a restart.
- Accounting uses MetaDB, initialised when quotas are enabled; the search extension is not required.
- Multiple writers need single-writer cluster routing.
- `503` means accounting is unavailable; `500` means invalid stored size metadata.

Separate setting: `storage.maxRepos` returns `413` for a push that would create a new repository past the limit.

## Checked

2026-11-04. Read against the zot storage planning article (Repository quotas); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
