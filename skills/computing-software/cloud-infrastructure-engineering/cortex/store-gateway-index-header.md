---
id: computing-software.cloud-infrastructure-engineering.cortex.store-gateway-index-header
name: store-gateway-index-header
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [store-gateway, index-header, byte-range, local-disk, blocks]
level: advanced
status: docs-checked
description: "Explain what the store-gateway index-header is, how it is built from byte-range requests, and why a persistent disk is recommended."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/blocks-storage/binary-index-header.md
  - https://github.com/cortexproject/cortex/blob/master/docs/blocks-storage/store-gateway.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The store-gateway queries series from blocks in object storage. To do that it needs some initial data from each block's index, which it assembles into an index-header stored on local disk.

The index-header is a subset of the block index: the symbol table (to unintern string values) and the posting offset table (to look up postings). It is built by downloading just those sections from the block index using GET byte-range requests. This is cheap, so the index-header is never uploaded back to the object store, and each store-gateway builds its own.

Chunks and the full index are never fully downloaded by the store-gateway.

With the bucket index disabled (default), a starting store-gateway iterates the entire bucket, downloading `meta.json` and the index-header for each block of its shard, and the `/ready` probe fails during this first synchronisation. It rescans on `-blocks-storage.bucket-store.sync-interval`. Because the index-header is kept on local disk, running the store-gateway with a persistent disk is recommended, though not required, so restarts do not re-download them; on Kubernetes a StatefulSet with a persistent volume claim fits. Without a persistent disk, a rolling update rebuilds index-headers from the original block index.

By default each index-header is memory mapped right after download, which can mean a lot of mapped memory in a cluster with many blocks. `-blocks-storage.bucket-store.index-header-lazy-loading-enabled=true` maps an index-header only when a query needs it and releases it after `-blocks-storage.bucket-store.index-header-lazy-loading-idle-timeout` of inactivity. A store-gateway is not ready until its initial index-header download completes.

## Checked

Method: docs-checked 2026-11-09 against the Cortex binary index-header page (read in full) and the store-gateway page (raw markdown, 110 KB; read the overview, bucket sync, and index-header sections via targeted search). A claim about horizontal compaction reducing memory was dropped as unconfirmed.
