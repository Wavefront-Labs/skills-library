---
id: computing-software.cloud-infrastructure-engineering.zot.sync-background-and-streaming
name: sync-background-and-streaming
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, on-demand-in-background, streaming-sync, max-concurrent-streams, download-dir, sync-staging]
level: advanced
status: docs-checked
description: "Use Zot sync onDemandInBackground (404 then background fetch) and streaming on-demand sync (v2.1.23+) with its incompatibilities and staging space."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/mirroring.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Background on-demand: set `onDemand: true` with `onDemandInBackground: true`. The first manifest request gets a real `404` and queues a background sync; later requests succeed. Blob misses alone do not trigger it. Do not use it if Zot is the client's only registry, and do not combine it with `manifestCheckInterval`.

Streaming on-demand (v2.1.23+):
- Keys: `stream` (default disabled) and `maxConcurrentStreams` (default `32`, shared across streaming registries; every streaming entry must use the same value).
- Requires `onDemand: true`, explicit HTTPS URLs and TLS verification enabled.
- Incompatible with `tlsVerify: false`, `onDemandInBackground`, `maxRetries` and `retryDelay`; Zot rejects these combinations. If another matching rule enables `onDemandInBackground`, that takes precedence for new syncs.
- Zot returns the upstream manifest before the cache fill completes; the download is pinned to that manifest's digest. Clients may receive bytes before digest verification finishes, so use a trusted upstream.
- Existing local blobs use no stream slots. On failure or when the cap is reached, the request falls back to regular on-demand sync.
- Staging: local storage uses its root directory; S3, GCS and Azure need `extensions.sync.downloadDir`. Plan roughly the total size of concurrently syncing images. Orphaned `_stream/` files are removed at startup; never delete active ones.

## Checked

2026-11-08. Read in full: docs/articles/mirroring.md and compared every claim above against it.

Method: documentation only; no commands were run.
