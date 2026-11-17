---
id: computing-software.cloud-infrastructure-engineering.garage.zstd-compression-level
name: zstd-compression-level
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [compression-level, zstd, block-compression, bandwidth]
level: practitioner
status: docs-checked
description: "Set the zstd compression_level used for stored blocks, from none to ultra levels."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`compression_level` chooses the zstd level for stored data blocks. Standard levels run from 1 (faster compression) to 19 (smaller files). Levels 20 to 22 are "ultra" and use a lot of memory, so use them carefully. A value of 0 lets zstd pick its default, currently 3. Negative values from -1 down to -99 select zstd's fast modes, with -99 the fastest.

If you do not specify the entry, Garage sets it to 1. That level uses little CPU, should run faster than line speed in most situations, and saves some space and intra-cluster bandwidth.

To disable zstd entirely, set the special value `'none'`; no zstd code runs and chunks are written to disk unprocessed.

Compression happens synchronously, so a very high level adds latency to write requests. The value may differ between nodes: the node that receives the API call does the compressing, so the setting is effectively per receiving node.

The page's full example uses `compression_level = 1`.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Configuration file format. Confirmed on the configuration page: levels 1 to 19, ultra 20 to 22, 0 meaning zstd default (currently 3), negative levels down to -99, default 1 when unset, the `'none'` value, synchronous compression, and per-node values. No changes needed.

Method: documentation only; no commands were run.
