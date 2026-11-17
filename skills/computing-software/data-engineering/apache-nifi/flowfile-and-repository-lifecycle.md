---
id: computing-software.data-engineering.apache-nifi.flowfile-and-repository-lifecycle
name: flowfile-and-repository-lifecycle
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, flowfile, write-ahead-log, lifecycle, swapping, checkpoint]
level: advanced
status: docs-checked
description: "How a FlowFile lives in NiFi: attributes plus content pointer, write-ahead log with snapshots and deltas, swap files of 10,000, and the ingress to cleanup lifecycle."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/nifi-in-depth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FlowFile and repository lifecycle

- A FlowFile is a content pointer plus key/value attributes and links to provenance events.
- The FlowFile repository logs changes ahead of time as deltas on a snapshot; recovery loads the snapshot and replays deltas. The new snapshot is written to a `.partial` file, then renamed.
- The checkpoint period is set in nifi.properties; this document states a two-minute default, so check the administration guide for your version.
- Past `nifi.queue.swap.threshold`, lowest-priority FlowFiles are swapped to disk in batches of 10,000.
- Lifecycle: ingress creates a FlowFile (CREATE or RECEIVE); processing logs deltas; egress DROPs it; after a checkpoint content claims are released; unreferenced resource claims are deleted or archived.
- Queues pass references (Claim Check pattern); routing clones share one content pointer (CLONE and ROUTE events).

Verify: after a crash test, queued FlowFiles are recovered from the snapshot.

## Checked

Confirmed against the NiFi In Depth guide: FlowFile as content pointer plus attributes, write-ahead log of deltas over a snapshot, `.partial` file renamed to snapshot, swapping past `nifi.queue.swap.threshold` in batches of 10,000, CREATE/RECEIVE ingress, DROP egress, content-claim release after checkpoint, Claim Check style references, CLONE and ROUTE events. Removed the 20-second checkpoint figure and the property name that the cited page does not give.

Method: docs-only read of cited pages, 2026-11-08
