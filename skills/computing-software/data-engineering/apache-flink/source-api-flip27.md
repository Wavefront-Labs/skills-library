---
id: computing-software.data-engineering.apache-flink.source-api-flip27
name: source-api-flip27
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-source-api, flip-27, split-enumerator, source-reader, custom-source, datastream-api]
level: advanced
status: docs-checked
description: "Build or use Flink FLIP-27 sources: SplitEnumerator, SourceReader and splits, bounded vs unbounded, checkpointed split state, and per-split watermarks."
sources:
  - https://raw.githubusercontent.com/apache/flink/release-2.4/docs/content/docs/internals/sources.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Source API (FLIP-27) and building sources

The Data Source API (FLIP-27) has three core components: splits, the SplitEnumerator and the SourceReader. The `Source` class is the entry point tying them together.

## Using one
```java
DataStream<Integer> stream = env.fromSource(
        mySource,
        WatermarkStrategy.noWatermarks(),
        "MySourceName");
```
`fromSource` takes the `WatermarkStrategy`, which creates the `TimestampAssigner` and `WatermarkGenerator`; they run inside the reader output, so source implementors write no timestamp or watermark code. Generators run per split, so event-time progress is tracked per split and idle partitions need not hold back the whole job. They are active only in streaming execution; in batch they are no-ops.

## Components
| Piece | Runs on | Job |
|---|---|---|
| `Source` | factory | creates the enumerator, reader, split serializer and enumerator checkpoint serializer; declares `Boundedness`; must be serializable |
| `SplitEnumerator` | JobManager, single instance | "brain": registers readers, discovers splits, assigns them (reactively, or proactively e.g. via `SplitEnumeratorContext.callAsync()` for periodic discovery), handles `SourceEvent`s |
| Split | data | a portion of data such as a file or log partition; the unit of work distribution and parallelism |
| `SourceReader` | TaskManagers, in parallel | requests and reads splits, produces records |

- `SourceReader` is pull-based: the task loops on `pollNext(ReaderOutput)`, which returns `MORE_AVAILABLE`, `NOTHING_AVAILABLE` or `END_OF_INPUT`. The task thread is an event loop and cannot block, so avoid emitting many records per call unless necessary (e.g. block-granular systems that can only checkpoint at block boundaries).
- `SplitEnumerator.addSplitsBack()` is invoked when a reader fails: take back assignments the failed reader had not acknowledged.
- All `SourceReader` state should live in the `SourceSplit`s returned from `snapshotState()`, so splits can be reassigned to other readers.
- For blocking systems (Kafka consumer, file I/O) implement the high-level `SplitReader` (blocking fetch, non-blocking split-change handling, non-blocking wake-up) and extend `SourceReaderBase`. The page highly recommends this over writing a `SourceReader` from scratch: it manages fetcher threads, hand-over, per-split watermarks for alignment, split state for checkpoints and optional rate limiting (`RateLimiterStrategy`, off by default). Threading is set by a `SplitFetcherManager`.

## Behaviour
- Bounded vs unbounded: bounded means a fixed set of finite splits; unbounded means splits are not finite or the enumerator keeps generating them (a streaming file source never answers `NoMoreSplits`). `Boundedness` lets Flink pick the execution mode.
- Normally assigned splits are not reassigned. After failure, splits from saved state are added back to the readers; a source implementing `SupportsSplitReassignmentOnRecovery` instead returns all splits to the enumerator, which redistributes them in a balanced way.
- Event timestamps are assigned in two steps: the reader may attach a source record timestamp (`SourceOutput.collect(event, timestamp)`; Kafka, Kinesis, Pulsar, Pravega), then the application's `TimestampAssigner` sets the final timestamp. Using the source record timestamp with a source lacking one (files) gives `Long.MIN_VALUE`.

## Checked
Method: 2026-11-08 read the Flink release-2.4 Data Sources page (internals/sources) in full; the old dev/datastream/sources URL there is only a redirect to it. Removed unsupported claims: SourceFunction deprecation/removal, the Kafka builder example, exactly-once reasoning, idleness/withIdleness and pauseOrResumeSplits notes, connector test-utils advice and the verify steps. The FLIP-27 wiki page was not read, so it is no longer cited. Description changed to drop "replacing legacy SourceFunction".
