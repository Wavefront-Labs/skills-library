---
id: computing-software.cloud-infrastructure-engineering.minio.erasure-coding
name: erasure-coding
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, erasure-coding, erasure-set, reed-solomon, quorum, read-quorum, write-quorum, parity, shards, highwayhash]
level: practitioner
status: docs-checked
description: "Explain MinIO erasure sets, data and parity shards, Reed-Solomon coding, read and write quorum with the K+1 rule at half parity, and why set layout is fixed at pool creation."
sources: ["https://github.com/minio/docs/blob/main/source/operations/concepts/erasure-coding.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO erasure coding

MinIO uses Reed-Solomon erasure coding as its core redundancy mechanism. Drives in each server pool are grouped into one or more **erasure sets** of equal size. MinIO picks the number and size of sets when the pool is initialised and the docs say you cannot change them afterwards.

## Shards and parity
For each write the object is split into data and parity shards: `N (erasure set size) = K (data) + M (parity)`. Parity can range from `EC:0` up to half the set size (a 16 drive set supports up to `EC:8`). Changing the parity setting later does not rewrite objects already stored with the old parity.

## Quorum
- Read quorum: at least `K` shards of any type must be available. Below that the object cannot be reconstructed; the docs point to replication resynchronisation as a recovery route.
- Write quorum: at least `K` drives online. If parity is exactly half the set size, write quorum is `K+1`. This prevents a split-brain where a network fault isolates exactly half of the drives and the same object is written to each half.
- With read quorum intact, any data or parity shard can be used to heal damaged shards.

Worked example from the page: 4 nodes x 4 drives form one 16 drive set; with `EC:4` and one node offline, 12 healthy drives still meet `K=12`.

## Bit rot
MinIO uses its HighwayHash implementation to detect and heal corrupted objects on the fly, hashing on read and verifying on write end to end.

## Planning tips
Prefer an even number of nodes and drives per node. The vendor's erasure code calculator helps explore set sizes. See `computing-software.cloud-infrastructure-engineering.minio.erasure-parity` for the storage trade-off and `computing-software.cloud-infrastructure-engineering.minio.healing` for repair.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Erasure Coding page (erasure-coding.rst). Removed: the 'exclusive access to drives' planning tip (not on this page).
Method: documentation only; no commands were run.
