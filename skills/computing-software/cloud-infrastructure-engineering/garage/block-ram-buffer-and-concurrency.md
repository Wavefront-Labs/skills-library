---
id: computing-software.cloud-infrastructure-engineering.garage.block-ram-buffer-and-concurrency
name: block-ram-buffer-and-concurrency
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [block-ram-buffer-max, block-max-concurrent-reads, block-max-concurrent-writes-per-request, backpressure]
level: advanced
status: docs-checked
description: "Bound RAM and disk concurrency with block_ram_buffer_max and the concurrent read and write limits."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three settings control backpressure.

`block_ram_buffer_max` (since v0.9.4, default 256MiB) limits the total size of data blocks held in RAM by S3 API nodes while they wait to be sent asynchronously to storage nodes. Writes use quorum: with three replicas, success returns after two, so the third write finishes asynchronously. If a slow third node never catches up, buffers pile up. When the limit is reached, backpressure goes back to the S3 client. It is not a hard RAM cap, since other buffers are not counted and RAM still grows with the number of concurrent large requests.

`block_max_concurrent_reads` (since v1.3.0 and v2.1.0) caps how many block files are open for reading at once, protecting HDD read speed. A request waits for a slot, reads the whole block into RAM, then frees the slot before network transfer. If no slot is free within 15 seconds it fails with a timeout. The metric `block_read_semaphore_timeouts` counts these; a non-zero value indicates an HDD read bottleneck.

`block_max_concurrent_writes_per_request` (since v1.3.1 and v2.2.0) limits parallel block writes per PUT. The default is 3, with 10 to 30 recommended for NVMe and 3 to 10 for spinning disks. Higher values may increase throughput and memory use.

## Checked

2026-11-04. Read the Configuration file format page in full. Confirmed all three options, their since-versions, the 256MiB and 3 defaults, the 15 second slot timeout, the block_read_semaphore_timeouts metric and the recommended ranges. Nothing removed.
Method: documentation only; no commands were run.
