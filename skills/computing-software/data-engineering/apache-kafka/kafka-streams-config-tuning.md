---
id: computing-software.data-engineering.apache-kafka.kafka-streams-config-tuning
name: kafka-streams-config-tuning
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-streams, commit-interval-ms, statestore-cache-max-bytes, num-stream-threads, rocksdb-config-setter, streams-config]
level: advanced
status: docs-checked
description: "Tune Kafka Streams: commit.interval.ms, record cache size, num.stream.threads, standby replicas, RocksDB memory bounding and producer/consumer overrides."
sources:
  - https://kafka.apache.org/39/streams/developer-guide/config-streams/
  - https://kafka.apache.org/39/streams/developer-guide/memory-mgmt/
  - https://kafka.apache.org/40/configuration/kafka-streams-configs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka Streams configuration tuning

```properties
application.id=billing-aggregator
num.stream.threads=4                       # threads per instance; total threads <= total input partitions (tasks)
commit.interval.ms=30000                   # default 30000 (100 under exactly_once_v2)
statestore.cache.max.bytes=104857600       # record cache across all threads (was cache.max.bytes.buffering)
num.standby.replicas=1                     # warm copies of state on other instances
processing.guarantee=at_least_once         # or exactly_once_v2
max.task.idle.ms=0                         # wait for data on all inputs before processing joins (set >0 for better join ordering)
state.dir=/var/lib/kafka-streams           # persistent volume, not /tmp
consumer.max.poll.records=500
producer.linger.ms=50
producer.compression.type=lz4
```

## Commit interval and cache work together
- Aggregation results are held in the record cache and flushed downstream (and to changelog) on commit or when the cache is full. Bigger cache + longer commit interval = fewer, deduplicated updates downstream and less changelog traffic; smaller = lower latency, more update records.
- `statestore.cache.max.bytes=0` disables caching: every update forwarded (useful in tests, expensive in production).
- With EOS, the commit interval also bounds read_committed latency for downstream consumers.

## Threads and scaling
- Parallelism unit is the task (one per input partition per sub-topology). Threads beyond tasks sit idle.
- `acceptable.recovery.lag` (default 10000 offsets) and `probing.rebalance.interval.ms` let new instances catch up before taking over active tasks.

## Bound RocksDB memory
Each RocksDB store has its own block cache and memtables by default, and the number of stores multiplies this off-heap memory. Streams lets you tune RocksDB through a class implementing `org.apache.kafka.streams.state.RocksDBConfigSetter`, registered with `rocksdb.config.setter` (the Streams docs show `setCacheIndexAndFilterBlocks(true)` so index and filter blocks do not grow unbounded). Follow the bounded-memory example on the Streams memory management page to share one cache across stores. Container memory = JVM heap + RocksDB memory + overhead.

## Overrides
Prefix with `consumer.`, `producer.`, `admin.`, `main.consumer.`, `restore.consumer.`, `global.consumer.`, or `topic.` (internal topic configs like `topic.min.insync.replicas=2`). Set `replication.factor` for internal topics explicitly if needed (default -1 = use the broker default, which requires brokers 2.4 or newer).

## Verify
- [ ] Streams and RocksDB metrics (see the Streams monitoring documentation) within targets.
- [ ] Container memory steady over 24 h (no RocksDB growth).

## Checked
2026-10-28. Confirmed in the Kafka 3.9 Streams config guide and the 4.0 Streams configs page: defaults `num.stream.threads` 1, `commit.interval.ms` 30000 (100 ms under exactly-once), `statestore.cache.max.bytes` 10485760 (the 100 MiB value above is an example), `num.standby.replicas` 0, `acceptable.recovery.lag` 10000, `replication.factor` -1 (brokers 2.4+), `state.dir` under the temp dir, `rocksdb.config.setter` and `RocksDBConfigSetter`, `cache.max.bytes.buffering` deprecated in favour of `statestore.cache.max.bytes`, client prefixes (`consumer.`, `main.consumer.`, `restore.consumer.`, `global.consumer.`, `topic.`), `processing.guarantee` values. Removed: `addStreamThread` version gate, the RocksDB code sample (not matched to the docs), metric names not found in the pages. `max.task.idle.ms` is described in the guide as controlling in-order join/merge processing.
Method: documentation only; no commands were run.
