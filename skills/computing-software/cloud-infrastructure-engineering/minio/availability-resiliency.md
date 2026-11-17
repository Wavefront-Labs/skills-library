---
id: computing-software.cloud-infrastructure-engineering.minio.availability-resiliency
name: availability-resiliency
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, availability-resiliency, erasure-set-selection, degraded-set, drive-striping, node-failure, read-only-mode, split-brain]
level: advanced
status: docs-checked
description: "How a distributed MinIO deployment tolerates drive and node loss via deterministic erasure set selection, parity upgrade on degraded sets and striping across nodes."
sources: ["https://github.com/minio/docs/blob/main/source/operations/concepts/availability-and-resiliency.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO availability and resiliency

Per the docs, distributed MinIO builds availability on erasure coding. Key behaviours:

- **Deterministic placement.** For each object namespace `BUCKET/PREFIX/.../OBJECT`, MinIO always selects the same erasure set, including all versions of that object.
- **Reads** continue while the set has not lost more drives than parity; with default `EC:4` four drives per set can fail. Lost data shards are replaced automatically from parity and the reconstructed object is served.
- **Writes to degraded sets.** If parity is under half the set size, write quorum behaves like read quorum, and MinIO raises the parity of objects written to a degraded set so they meet the same SLA as objects in healthy sets. The page shows two failed drives leading to an `EC:6` write.
- **Half parity.** When parity equals half the set size, write quorum is parity + 1. If half the drives are isolated, writes are rejected but existing objects remain readable.
- **Data loss** happens only when an erasure set permanently loses more drives than parity. For the maximum set size 16 and maximum parity 8, that takes 9 lost drives. Transient controller or connectivity failures may recover.
- **Striping.** MinIO sizes sets automatically (maximum 16 drives), taking one drive per node across the pool and wrapping around when the set is larger than the node count. Losing one node (or its storage controller) costs each set at most the drives it had there. Example: 16 nodes x 8 drives gives 8 sets of 16 drives, one drive per node per set.

The page is a best-effort design guide, not a support substitute. Related: `computing-software.cloud-infrastructure-engineering.minio.erasure-coding`.

## Checked

2026-11-03. Confirmed against the MinIO docs source: availability-and-resiliency page: set placement, EC:6 upgrade example, half parity quorum, data loss threshold of 9 drives, maximum set size 16, striping example. Removed or fixed: nothing.

Method: documentation only; no commands were run.
