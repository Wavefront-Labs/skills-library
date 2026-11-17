---
id: computing-software.cloud-infrastructure-engineering.zot.storage-failure-status-codes
name: storage-failure-status-codes
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, storage-errors, status-503, status-500, status-404, fail-closed]
level: advanced
status: docs-checked
description: "Interpret Zot storage failure responses since v2.1.22: 404 missing, 503 transient (retry), 500 permanent (check logs), and fail-closed background jobs."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/storage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
From v2.1.22 Zot distinguishes storage outcomes:

| Code | Meaning | What to do |
|---|---|---|
| `404` | Content is missing | Treat as absent |
| `503` | Transient backend failure | Clients should retry |
| `500` | Permanent backend failure | Check logs before retrying |

Background operations (garbage collection, dedupe, scrub, storage walks) fail closed. They do not treat an unknown result as missing content, so a flaky backend will not cause deletions.

Related behaviour:
- A listing or existence-check failure aborts that GC pass.
- Quota accounting returns `503` if accounting is unavailable and `500` for invalid stored size metadata.
- Over-limit pushes return `413`.

Triage tip: a burst of `503` from an S3 or GCS-backed registry points at the backend or network; `500` that persists means read the Zot logs rather than retrying blindly.

## Checked

2026-11-04. Read against the zot storage planning article (Storage failure handling); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
