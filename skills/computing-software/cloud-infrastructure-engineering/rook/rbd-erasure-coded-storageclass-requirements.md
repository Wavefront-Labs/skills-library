---
id: computing-software.cloud-infrastructure-engineering.rook.rbd-erasure-coded-storageclass-requirements
name: rbd-erasure-coded-storageclass-requirements
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [erasure-coded, datapool, bluestore, storageclass-ec, kernel-4-11]
level: advanced
status: docs-checked
description: "Prerequisites and layout for erasure-coded RBD storage: bluestore OSDs, kernel 4.11 or newer, one replicated and one EC pool, and the dataPool parameter."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Block-Storage-RBD/block-storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Erasure coded RBD has specific requirements stated on the Block Storage page:
- OSDs must use `bluestore` as their `storeType`.
- Nodes that mount the erasure coded RBD volumes need Linux kernel 4.11 or newer.
- You create two pools: one erasure coded and one replicated. RBD metadata lives in the replicated pool, while the EC pool holds the image data.

The docs example needs at least three bluestore OSDs, each on a different node. With `failureDomain: host` and chunk settings of 2 `dataChunks` plus 1 `codingChunks`, three distinct OSDs are required. (Production EC pools should use at least 2 coding chunks, as noted in the CephBlockPool CRD page.)

In the CSI configuration, the erasure coded pool is named in the `dataPool` parameter of `storageclass-ec.yaml`, and that pool is used for the data of the RBD images. The class's `pool` parameter refers to the replicated pool.

Create the pools from the example `CephBlockPool` definitions, then create the storage class, then use PVCs as for ordinary RBD.

## Checked

2026-11-03. Confirmed against the Block Storage page and CephBlockPool CRD page: bluestore storeType, kernel 4.11, the replicated plus EC pool pair, the dataPool parameter and the three-OSD 2+1 example; the two-coding-chunk production advice is from the CephBlockPool CRD page. Removed: the self-check paragraph, which the page does not state.

Method: documentation only; no commands were run.
