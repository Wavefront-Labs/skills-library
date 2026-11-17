---
id: computing-software.messaging-and-integration.apache-zookeeper.performance-and-reliability-expectations
name: performance-and-reliability-expectations
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, performance, benchmarks, read-write-ratio, leader-election-time, reliability]
level: intro
status: docs-checked
description: "Published ZooKeeper performance expectations: read-heavy 10:1 ratio, benchmark setup, 3.2 speedup and leader election under 200 ms in the seven-machine test."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperOver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Performance and reliability expectations

- Optimised for read-dominated workloads; the overview cites about 10:1 read-to-write.
- Release 3.2 improved read/write performance by roughly 2x over 3.1.
- Benchmark setup: 1K reads and writes, dual 2 GHz Xeon servers with SATA drives, about 30 other servers simulating clients.
- Reliability test: 7 machines, 30% writes; throughput stayed high when followers failed and recovered once they resumed.
- Leader election took under 200 ms in that test.
- Treat these as reference points on old hardware, not a sizing guarantee; benchmark your own hardware (see YCSB tooling).

Verify: run your own load test at your real read-to-write ratio and compare the result with these figures only as a rough reference.

## Checked

Method: docs-checked 2026-11-09 against zookeeperOver.html (full page read)
