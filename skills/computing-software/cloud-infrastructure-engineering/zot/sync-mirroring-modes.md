---
id: computing-software.cloud-infrastructure-engineering.zot.sync-mirroring-modes
name: sync-mirroring-modes
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, sync-extension, on-demand, poll-interval, mirror-modes, registry-migration]
level: practitioner
status: docs-checked
description: "Choose Zot sync mode from onDemand, pollInterval and content: full mirror, pull-through cache, migration settings, and the Docker Hub caution."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/mirroring.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `sync` extension (`extensions.sync`) mirrors OCI-conformant upstream registries. Three keys decide the mode: `onDemand`, `pollInterval`, `content`.

| onDemand | content | pollInterval | Result |
|---|---|---|---|
| false | none | any | sync disabled |
| false | set | > 0 | periodic for matching images |
| true | none | any | on-demand for any image |
| true | set | none | on-demand for matching images |
| true | set | > 0 | periodic and on-demand for matching images |

- Fully mirrored: periodic polling, not on-demand; Zot caches every upstream image and refreshes on change.
- Pull-through cache: `onDemand: true`; images are fetched on first request, and with `pollInterval` refreshed on change.
- Do not use polled mirroring with Docker Hub (pull rate limits, no catalog listing); use on-demand only.
- Migration or upgrade/downgrade with minimal downtime: `pollInterval: "12h"`, `onDemand: true`, and `content` with `prefix: "**"`.
- Docker-format upstreams need `http.compat: ["docker2s2"]`.

## Checked

2026-11-08. Read in full: docs/articles/mirroring.md and compared every claim above against it. Removed: the scale-out cluster compatibility bullet (not on this page).

Method: documentation only; no commands were run.
