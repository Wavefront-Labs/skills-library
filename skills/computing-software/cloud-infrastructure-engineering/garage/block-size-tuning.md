---
id: computing-software.cloud-infrastructure-engineering.garage.block-size-tuning
name: block-size-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [block-size, chunk-size, large-objects, deduplication]
level: advanced
status: docs-checked
description: "Tune block_size, the chunk size objects are split into, and understand its effect on existing data and large uploads."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/known-issues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Garage splits each object into consecutive chunks of `block_size`, except that the last chunk may be smaller. The default is 1MiB and suits most cases. The page suggests raising it to around 10MiB when you store large files and have fast links between all nodes, such as 1 Gbps.

Changing `block_size` on a running installation only affects newly uploaded files. Existing files stay readable. However, chunks of older files will not be deduplicated against chunks of newer uploads, so you may use more storage than optimal.

The known-issues page explains why large block counts hurt: each object has a single metadata entry (a Version) listing all its blocks, and during an upload this entry is read, deserialised, reserialised and written for every block, so upload cost grows as O(n squared) in the number of blocks. This shows up as heavy metadata I/O, high CPU and stalled uploads on very big objects.

Documented mitigation: raise `block_size` to reduce the number of blocks, and make multipart uploads use parts at least `block_size` large and an exact multiple of `block_size`, so no smaller blocks are created.

## Checked

2026-11-04. Read the Configuration file format and Known issues pages in full. Confirmed the 1MiB default, the 10MiB and 1 gbps suggestion, the new-uploads-only and deduplication caveat, the Version entry and O(n^2) explanation and the multipart mitigation. Nothing removed.
Method: documentation only; no commands were run.
