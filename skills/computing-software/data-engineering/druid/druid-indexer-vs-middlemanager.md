---
id: computing-software.data-engineering.druid.druid-indexer-vs-middlemanager
name: druid-indexer-vs-middlemanager
category: computing-software
field: data-engineering
product: druid
tags: [indexer, middle-manager, peon, task-execution, jvm]
level: practitioner
status: docs-checked
description: "Compare the experimental Indexer service with the Middle Manager plus Peon task execution system."
sources:
  - https://github.com/apache/druid/blob/master/docs/design/indexer.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Indexer is an alternative to the Middle Manager plus Peon system. Instead of forking a separate JVM per task, the Indexer runs tasks as separate threads inside a single JVM process. It is designed to be easier to configure and deploy than Middle Manager plus Peon, and to share resources better across tasks.

The docs mark the Indexer as optional and experimental. Their guidance is that if you mainly do batch ingestion, use either the Middle Manager and Peon system or Kubernetes-based Middle Manager-less ingestion; for mainly streaming ingestion you may want to try the Indexer.

The Indexer shares the same HTTP endpoints as the Middle Manager, so tooling that talks to a Middle Manager keeps working. Its configuration is described in the Indexer section of the configuration reference. Start it with:

```
org.apache.druid.cli.Main server indexer
```

Because all tasks live in one JVM, these are shared across tasks:
- Query processing threads and buffers, served from a single endpoint; the query cache too if query caching is enabled.
- Server HTTP threads: two equally sized pools of `druid.server.http.numThreads` each, one only for Overlord task control messages (chat handler threads) and one for all other requests, plus two threads for lookup handling.
- Heap: `druid.worker.globalIngestionHeapLimitBytes`, by default 1/6 of the JVM heap, is divided evenly across the `druid.worker.capacity` task slots. The Indexer overrides each task's `maxBytesInMemory` with that per-task limit and sets `maxRowsInMemory` to an essentially unlimited value, because it does not support row limits. Peak in-heap row data can reach roughly `maxBytesInMemory * (2 + maxPendingPersists)`; `maxPendingPersists` defaults to 0.
- Concurrent segment persist/merge operations are limited to `druid.worker.capacity / 2`, rounded down, configurable with `druid.worker.numConcurrentMerges`.

Current limitations: separate task logs are not supported, so all task log messages go to the Indexer service log, and every task gets an identical memory limit.

## Checked

2026-11-08. Read design/indexer.md in full. Added shared resources, heap limit default (1/6 of JVM heap), HTTP thread pools, merge limits and current limitations.

Method: documentation only; no commands were run.
