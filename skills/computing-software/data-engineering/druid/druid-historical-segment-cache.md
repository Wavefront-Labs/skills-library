---
id: computing-software.data-engineering.druid.druid-historical-segment-cache
name: druid-historical-segment-cache
category: computing-software
field: data-engineering
product: druid
tags: [historical, segment-cache, deep-storage, load-segments, memory-mapping]
level: practitioner
status: docs-checked
description: "Explain how a Historical pulls segments from deep storage into its local segment cache and advertises them."
sources:
  - https://github.com/apache/druid/blob/master/docs/design/historical.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Historical stores and queries historical data. It caches data segments on local disk and serves queries from that cache as well as from an in-memory cache.

Each Historical copies or pulls segment files from deep storage into an area called the segment cache. Configure the size and location of that cache with `druid.segmentCache.locations`. The Coordinator controls which segments go to which Historical and how they are balanced; Historicals do not communicate directly with each other. The Coordinator sends segment load and drop requests over HTTP, and each Historical exposes an HTTP endpoint the Coordinator polls for the state of its segment assignments.

When a load request arrives, the Historical first checks its own segment cache. If nothing is there it uses the segment metadata in the request, which includes where the segment sits in deep storage and how to decompress and process it, to pull the segment down. Once the segment is pulled and processed, Druid advertises it as available for queries. The Historical exposes its served segments through `/druid-internal/v1/segments`, which the Broker polls to learn what data each Historical holds. On startup a Historical searches its local segment cache and advertises the segments found there, so data is queryable as soon as possible.

The segment cache uses memory mapping, so the operating system page cache holds parts of segment files in memory. If the needed part is in the page cache the Historical reads it from memory; otherwise it reads from disk, and new data may flush other segment data out of memory. The more free operating system memory relative to `druid.server.maxSize`, the more likely segment data is in memory and the faster queries run. Free memory is affected by the JVM heap, direct memory buffers and other services on the host. This page cache is in addition to the query-level caches.

## Checked

2026-11-08. Read design/historical.md in full. Added startup advertisement and the memory-mapped page cache behaviour.

Method: documentation only; no commands were run.
