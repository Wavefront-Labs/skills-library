---
id: computing-software.cloud-infrastructure-engineering.garage.known-issue-large-objects-and-many-objects
name: known-issue-large-objects-and-many-objects
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [known-issues, large-objects, multipart-upload, metadata-performance]
level: advanced
status: docs-checked
description: "Recognise Garage performance limits with millions of objects and very large objects, and apply the documented mitigation."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/known-issues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Architectural limits from the known-issues page:

Many objects: metadata performance can collapse with millions of objects in a bucket; the page cites reports of problems around 10 million objects.

Very big objects: each object has one metadata Version listing all its blocks. Uploading re-reads and rewrites it for every block, so cost is O(n squared) in block count. Symptoms are heavy metadata I/O, high CPU and stalled uploads. Mitigation: raise `block_size`; make multipart parts at least `block_size` and an exact multiple of it so no smaller blocks appear. A real fix needs an architectural change storing block lists in many independent entries.

Buckets are not sharded: a bucket's object index lives on `replication_factor` nodes chosen randomly at creation (spread across zones), different for each bucket. If all traffic hits one bucket, those nodes become a hotspot, and you cannot choose them.

Node count limitation: Garage uses 256 partitions, so uneven filling starts when node count exceeds 10 times `replication_factor`. Mitigation: build fewer, bigger nodes.

## Checked

2026-11-04. Read the Known issues page in full. Confirmed the many-objects reports, the Version entry and O(n^2) explanation, the mitigation, the bucket sharding hotspot and the node count limit of 10 times replication_factor with 256 partitions. Nothing removed.
Method: documentation only; no commands were run.
