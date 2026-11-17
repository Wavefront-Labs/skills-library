---
id: computing-software.cloud-infrastructure-engineering.etcd.performance-and-benchmark
name: performance-and-benchmark
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [performance, benchmark, throughput, latency, benchmark-tool, write-latency, fio, sequential-writes]
level: practitioner
status: docs-checked
description: "Measure etcd performance with the benchmark tool and fio; what throughput to expect and what limits it."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/performance/"
  - "https://etcd.io/docs/v3.5/op-guide/hardware/"
  - "https://etcd.io/docs/v3.5/faq/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The performance page gives reference numbers and a method.

Factors: disk fsync latency, network RTT between members, number of clients, key and value sizes, the number of connections, and whether requests are linearizable.

The page says a three-member cluster in common cloud environments finishes a request in under a millisecond under light load and can complete more than 30,000 requests per second under heavy load. The minimum time for a request is the network RTT between members plus the fdatasync time (about 10 ms on a spinning disk, often under 1 ms on SSD).

The benchmark setup was three Google Compute Engine machines (8 vCPUs, 16 GB, 50 GB SSD) with a 16-vCPU client, etcd 3.2.0, using the `benchmark` tool included with etcd. Sample results for 8 byte keys and 256 byte values: 1 connection and 1 client writing to the leader, 583 writes per second at 1.6 ms; 100 connections and 1000 clients, 44,341 per second (leader only) or 50,104 (all members). Reads with 100 connections and 1000 clients: 141,578 per second linearizable and 185,758 serializable. These are old figures (etcd 3.2.0); the page encourages running the benchmark in your own environment.

Typical commands:

```bash
benchmark --endpoints=$HOST_1 --target-leader --conns=1 --clients=1   put --key-size=8 --sequential-keys --total=10000 --val-size=256
benchmark --endpoints=$HOST_1,$HOST_2,$HOST_3 --conns=100 --clients=1000   put --key-size=8 --sequential-keys --total=100000 --val-size=256
benchmark --endpoints=$HOST_1,$HOST_2,$HOST_3 --conns=100 --clients=1000   range YOUR_KEY --consistency=l --total=100000
```

`--target-leader` sends to the leader only. `--consistency=l` is linearizable (goes through a quorum) and `--consistency=s` serializable (served by any single member, possibly stale).

Disk check: the hardware page recommends a benchmarking tool such as `fio`; the FAQ says p99 `wal_fsync_duration_seconds` should be under 10 ms.

## Checked

2026-11-03. Confirmed on the v3.5 performance page: the 30,000 requests per second and sub-millisecond claims, the RTT plus fdatasync minimum, benchmark hardware and etcd 3.2.0, the three write rows and four read rows, sample benchmark commands and linearizable/serializable semantics. Corrected: the reference numbers in the previous text were approximate and the setup description wrong. Fio and the 10 ms figure are on the hardware page and FAQ; the removed fio command line is not on any fetched page.

Method: documentation only; no commands were run.
