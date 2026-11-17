---
id: computing-software.data-engineering.apache-spark.shuffle-tuning-and-push-based-shuffle
name: shuffle-tuning-and-push-based-shuffle
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, push-based-shuffle, shuffle-tuning, shuffle-compression, magnet, external-shuffle-service, spark-performance]
level: advanced
status: docs-checked
description: "Tune the Spark shuffle: file buffers, compression codecs, fetch concurrency, external shuffle service, and push-based shuffle (Magnet) on YARN to cut fetch failures."
sources:
  - https://spark.apache.org/docs/latest/configuration.html#shuffle-behavior
  - https://spark.apache.org/docs/latest/configuration.html#push-based-shuffle-configuration
  - https://issues.apache.org/jira/browse/SPARK-30602
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shuffle tuning and push-based shuffle

## Baseline knobs (map side and reduce side)
```properties
spark.shuffle.compress=true                    # default; map outputs compressed
spark.io.compression.codec=lz4                 # alternative: zstd (level via spark.io.compression.zstd.level)
spark.io.compression.zstd.level=1
spark.shuffle.file.buffer=1m                   # default 32k; fewer disk syscalls when writing map output
spark.shuffle.localDisk.file.output.buffer=1m   # replaces spark.shuffle.unsafe.file.output.buffer, deprecated since Spark 4.0
spark.reducer.maxSizeInFlight=96m              # default 48m; more parallel fetch per reducer
spark.shuffle.io.maxRetries=10                 # default 3; ride out GC pauses / busy shuffle servers
spark.shuffle.io.retryWait=15s
spark.shuffle.service.enabled=true             # external shuffle service: shuffle files survive executor loss
```
Partition count (`spark.sql.shuffle.partitions` / AQE coalescing) and skew handling matter more than these; tune those first.

## Push-based shuffle (Magnet)
Classic shuffle: each reducer fetches tiny blocks from every mapper (M x R random reads). With push-based shuffle, mappers push blocks to remote shuffle services, which **merge** them per reduce partition; reducers read a few large sequential files.
```properties
# application
spark.shuffle.push.enabled=true
spark.shuffle.service.enabled=true
# YARN NodeManager (yarn-site/shuffle server config)
spark.shuffle.push.server.mergedShuffleFileManagerImpl=org.apache.spark.network.shuffle.RemoteBlockPushResolver
```
- Needs the server-side merge manager enabled on the shuffle service; see the push-based shuffle section of the configuration page.
- Merging is best-effort; unmerged blocks fall back to normal fetch.
- Benefits show when blocks are small. Compare shuffle read metrics in the Stages tab before and after.

## Kubernetes alternatives
Enable decommissioning (`spark.decommission.enabled`, `spark.storage.decommission.shuffleBlocks.enabled`) so shuffle blocks migrate off executors that are shutting down.

## Verify
- [ ] Shuffle read time and FetchFailed counts drop on the heavy stage.
- [ ] Executor disk not filling (`spark.local.dir` on fast disks).

## Checked

2026-10-28. Confirmed in the Spark configuration page (shuffle behaviour and push-based shuffle sections): `spark.shuffle.file.buffer` default 32k, `spark.reducer.maxSizeInFlight` default 48m, `spark.shuffle.io.maxRetries` default 3, `spark.shuffle.io.retryWait`, `spark.io.compression.zstd.level`, `spark.shuffle.push.enabled`, `spark.shuffle.push.server.mergedShuffleFileManagerImpl`, `spark.decommission.enabled`, `spark.storage.decommission.shuffleBlocks.enabled`. Fixed: `spark.shuffle.unsafe.file.output.buffer` is deprecated since 4.0 in favour of `spark.shuffle.localDisk.file.output.buffer`. Removed: the zstd percentage, the version and cluster-manager limits, named remote shuffle services, and UI metric names not found in the pages.
Method: documentation only; no commands were run.
