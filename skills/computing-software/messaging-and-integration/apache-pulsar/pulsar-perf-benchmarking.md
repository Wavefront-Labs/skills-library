---
id: computing-software.messaging-and-integration.apache-pulsar.pulsar-perf-benchmarking
name: pulsar-perf-benchmarking
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [pulsar-perf, benchmarking, throughput, latency, performance-testing, transaction-benchmark]
level: practitioner
status: docs-checked
description: "Benchmark Pulsar with bin/pulsar-perf: produce and consume tests, reading throughput and latency percentiles, transaction flags and the Latest subscription gotcha."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/performance-pulsar-perf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: measure write and read throughput and latency against a topic.

`pulsar-perf` is a built-in performance test tool. Full flag lists are in the pulsar-perf reference; this page shows the common runs.

Produce with defaults:
```shell
bin/pulsar-perf produce my-topic
```
It prints a line about every 10 seconds, such as `Throughput produced: 100.0 msg/s --- 0.8 Mbit/s --- failure 0.0 msg/s --- Latency: mean ... med ... 95pct ... 99pct ... 99.9pct ...`. Stop it with Ctrl+C; aggregated throughput and latency statistics are printed at stop.

Produce with transactions: `bin/pulsar-perf produce my-topic -r 10 -m 100 -txn` (flag meanings are in the pulsar-perf reference). The log then also reports transactions ended successfully or failed and Txn/s.

Consume with defaults:
```shell
bin/pulsar-perf consume my-topic
```
Consume with transactions and explicit subscription: `bin/pulsar-perf consume my-topic -r 10 -txn -ss mysubName -st Exclusive -sp Earliest -ntxn 10`.

Transaction workload: `bin/pulsar-perf transaction --topics-c myConsumerTopic --topics-p MyproduceTopic -threads 1 -ntxn 50 -ss testSub -nmp 1 -nmc 1`.

Gotchas:
- Run a producer while measuring consumption, or prepare a retained backlog. A new subscription starts at `Latest` by default, so use `--subscription-position Earliest` to read retained messages.
- Automatic topic creation depends on the broker and namespace configuration and does not create test data.
- A warning about the Circe JNI library falling back to Java CRC32c is informational.

## Checked

2026-11-03. Confirmed against the pulsar-site page performance-pulsar-perf: the produce, consume and transaction commands as printed, the 10-second output lines, Ctrl+C aggregated stats, the Latest-subscription note and the Circe warning. Removed the flag glosses the page does not state and the invented Verify step.

Method: documentation only; no commands were run.
