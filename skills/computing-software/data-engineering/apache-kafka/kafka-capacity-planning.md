---
id: computing-software.data-engineering.apache-kafka.kafka-capacity-planning
name: kafka-capacity-planning
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-capacity-planning, sizing, partition-limits, retention-ms, network-throughput, kafka-operations]
level: advanced
status: docs-checked
description: "Size a Kafka cluster from throughput, retention and fan-out: disk, network, broker count, partition limits per broker, and headroom for failures and rebalancing."
sources:
  - https://kafka.apache.org/39/getting-started/upgrade/
  - https://docs.confluent.io/platform/current/kafka/deployment.html
  - https://www.confluent.io/blog/how-choose-number-topics-partitions-kafka-cluster/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka capacity planning

## Inputs to collect
- Peak ingress MB/s (W), average record size, growth rate.
- Replication factor (R, usually 3).
- Number of consumer groups reading each topic (fan-out C) and whether they read from the tail (page cache) or replay from disk.
- Retention per topic (time or size), compaction topics' key cardinality.
- Latency SLO and durability (`acks=all`, `min.insync.replicas`).

## Arithmetic (per cluster, at peak)
| Resource | Formula | Example W=100 MB/s, R=3, C=3 |
|---|---|---|
| Disk write | W x R | 300 MB/s |
| Network in | W x R (producer in + follower replication in) | 300 MB/s |
| Network out | W x (R-1) + W x C | 200 + 300 = 500 MB/s |
| Storage | W x R x retention_seconds x (1 + headroom) | 100 MB/s x 3 x 7 d ~ 181 TB, x1.3 ~ 235 TB |
Compression: use compressed sizes (measure the producer's `compression-rate-avg`). Divide per-broker and leave headroom in NIC and disk throughput so a broker failure (its load redistributed to N-1) and reassignment traffic still fit; pick the headroom from load tests.

## Partitions
- Each partition costs open file handles, memory and leader election time (Confluent's partition-count article). Its rule of thumb for latency-sensitive clusters is to limit partitions per broker to 100 x b x r (b brokers, r replication factor). Measure controlled shutdown time as you grow.
- Partition count per topic from target throughput: max(W_topic / per-partition producer throughput, W_topic / per-partition consumer throughput), where per-partition throughput is measured on your hardware, and from consumer parallelism needed.

## Other sizing
- **Memory**: keep the broker heap modest; the rest of RAM is page cache. Want enough page cache to hold the tail being consumed: W x (seconds consumers lag behind at most).
- **CPU**: TLS and compression (if brokers must recompress because of mismatched `compression.type`) are the CPU hogs.
- **Disk type**: consumers replaying old data hit disk, so use faster disks if replays are routine. Tiered storage (production ready since Kafka 3.9) moves old segments to remote storage and shrinks local disk to hot retention.
- **File descriptors**: raise the open-file limit with partition count: every log segment holds open file handles (Confluent's partition-count article).

## Validate
```bash
kafka-producer-perf-test.sh --topic perf --num-records 50000000 --record-size 1000 --throughput -1 --producer-props bootstrap.servers=$BS acks=all compression.type=lz4
kafka-consumer-perf-test.sh --bootstrap-server $BS --topic perf --messages 50000000
```
Run with a broker down to test degraded capacity.

## Verify
- [ ] At peak, broker NIC and disk stay inside your chosen headroom with one broker stopped.
- [ ] Projected storage at 12-month growth fits with your chosen free-space margin.

## Checked
2026-10-28. Confirmed: Confluent partition-count article (per-broker rule `100 x b x r`, open file handles grow with partitions); Kafka 3.9 upgrade notes (tiered storage production ready); `kafka-producer-perf-test.sh` flags `--num-records`, `--record-size`, `--throughput`, `--producer-props` (ProducerPerformance source 3.9) and `kafka-consumer-perf-test.sh` (ConsumerPerformance source 3.9). The throughput and storage table is arithmetic from the stated inputs. Removed: the 4000 / 200k partition figures, heap size, NIC and disk headroom percentages, the per-partition MB/s range, the page-cache and storage-class examples and the file-descriptor count (not found in the pages).
Method: documentation only; no commands were run.
