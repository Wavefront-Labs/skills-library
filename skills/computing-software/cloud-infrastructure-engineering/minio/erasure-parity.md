---
id: computing-software.cloud-infrastructure-engineering.minio.erasure-parity
name: erasure-parity
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, erasure-parity, ec-4, storage-efficiency, parity-tradeoff, usable-capacity, erasure-code-calculator]
level: practitioner
status: docs-checked
description: "Choose MinIO erasure parity by weighing usable capacity against drive failure tolerance, using the documented EC 4, EC 6 and EC 8 outcomes on a 16 drive node."
sources: ["https://github.com/minio/docs/blob/main/source/operations/concepts/erasure-coding.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO erasure parity and storage efficiency

Parity is a balance: higher parity tolerates more drive or node failures but reduces usable storage, while lower parity maximises capacity with less failure tolerance. The default is `EC:4`.

Docs example, one node with 16 x 1 TB drives:

| Parity | Usable storage | Ratio | Min drives to read | Min drives to write |
|---|---|---|---|---|
| EC:4 (default) | 12 TiB | 0.750 | 12 | 12 |
| EC:6 | 10 TiB | 0.625 | 10 | 10 |
| EC:8 | 8 TiB | 0.500 | 8 | 9 |

Note the write column at `EC:8`: parity equal to half the set raises write quorum by one (`K+1`) to avoid split-brain.

## How to decide
- Use the MinIO erasure code calculator with your planned node and drive counts before committing, because the erasure set layout is fixed when a pool is created.
- Parity can be set between `EC:0` and half the erasure set size.
- Objects keep the parity they were written with; a later change only affects new writes.
- When an erasure set is degraded, MinIO writes new objects with upgraded parity (the availability page shows `EC:6` replacing `EC:4` with two failed drives), which is a safeguard and not a substitute for replacing the drives.

Related: `computing-software.cloud-infrastructure-engineering.minio.erasure-coding`, `computing-software.cloud-infrastructure-engineering.minio.availability-resiliency`.

## Checked

2026-11-03. Confirmed against the MinIO docs source: erasure-coding page: the 16 x 1 TB parity table (12, 10 and 8 TiB), K+1 write quorum at half parity, EC:0 to half-set range, parity not rewritten for old objects. Removed or fixed: nothing.

Method: documentation only; no commands were run.
