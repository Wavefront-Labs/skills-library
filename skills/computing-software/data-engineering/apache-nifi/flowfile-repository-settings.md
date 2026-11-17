---
id: computing-software.data-engineering.apache-nifi.flowfile-repository-settings
name: flowfile-repository-settings
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, flowfile-repository, write-ahead-log, checkpoint, nifi-properties]
level: practitioner
status: docs-checked
description: "FlowFile repository keys in nifi.properties: WriteAheadFlowFileRepository, SequentialAccessWriteAheadLog, directory, checkpoint interval 20 secs, always.sync, swap threshold."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FlowFile repository

- `nifi.flowfile.repository.implementation`: `org.apache.nifi.controller.repository.WriteAheadFlowFileRepository`
- `nifi.flowfile.repository.wal.implementation`: `org.apache.nifi.wali.SequentialAccessWriteAheadLog`
- `nifi.flowfile.repository.directory`: `./flowfile_repository`
- `nifi.flowfile.repository.checkpoint.interval`: 20 secs
- `nifi.flowfile.repository.always.sync`: false (default)
- `nifi.swap.manager.implementation`: `org.apache.nifi.controller.FileSystemSwapManager`
- `nifi.queue.swap.threshold`: 20000

Values above are the defaults the administration guide lists. The repository keeps the attributes and current state of each FlowFile; the guide advises configuring it on a separate drive if available. With `always.sync` true every change is synchronised to disk, which the guide calls very expensive and able to reduce NiFi performance significantly; with false there is potential data loss on sudden power loss or an OS crash. Other implementations are `VolatileFlowFileRepository` and `RocksDBFlowFileRepository`; switch only on an instance with zero queued FlowFiles. `SequentialAccessWriteAheadLog` was added in NiFi 1.6.0 to fix incorrect FlowFile recovery after power loss in the older `org.wali.MinimalLockingWriteAheadLog`.

Verify: with the node stopped cleanly and restarted, queued FlowFile counts match what they were before.

## Checked

Confirmed against the NiFi administration guide (FlowFile Repository, Write Ahead FlowFile Repository, Swap Management). Removed the advice to separate it from the content repository specifically (the guide only says a separate drive is advisable).

Method: docs-only read of cited pages, 2026-11-08
