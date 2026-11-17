---
id: computing-software.messaging-and-integration.apache-zookeeper.thread-pool-tuning
name: thread-pool-tuning
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, performance-tuning, nio, commitprocessor, worker-threads, netty]
level: sme
status: docs-checked
description: "Server threading properties: NIO selector and worker threads, CommitProcessor worker and batch sizes, learner async sending and Netty handshake limits."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread and processing tuning

- `zookeeper.nio.numSelectorThreads`: default sqrt(cores / 2), at least 1.
- `zookeeper.nio.numWorkerThreads`: default 2 x cores; 0 makes selectors do I/O.
- `zookeeper.commitProcessor.numWorkerThreads`: default number of cores; 0 uses the main thread.
- `zookeeper.commitProcessor.maxReadBatchSize`: default less than 0.
- `zookeeper.commitProcessor.maxCommitBatchSize`: default 1.
- `learner.asyncSending`: default false; `learner.closeSocketAsync` and `leader.closeSocketAsync` default false.
- `forward_learner_requests_to_commit_processor_disabled`: default false.
- `zookeeper.netty.server.outstandingHandshake.limit`: example value 250; `earlyDropSecureConnectionHandshakes` disabled by default since 3.7.1/3.8.0.
- `messageTracker.Enabled` default false, `messageTracker.BufferSize` default 10.

Change one property at a time and compare latency before and after.

Verify: `mntr` average latency and outstanding requests improve (or at least do not regress) under the same load.

## Checked

Read the relevant entries of the ZooKeeper Administrator's Guide. Confirmed the NIO selector and worker thread defaults, the commitProcessor worker, read-batch and commit-batch settings and defaults, learner.asyncSending, the closeSocketAsync options, forward_learner_requests_to_commit_processor_disabled, Netty outstandingHandshake.limit (example 250), earlyDropSecureConnectionHandshakes default since 3.7.1 and 3.8.0, and the messageTracker properties. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
