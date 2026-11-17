---
id: computing-software.messaging-and-integration.redpanda.sizing-cores-memory-and-network
name: sizing-cores-memory-and-network
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [sizing, capacity, network, memory-per-core, throughput, nvme]
level: intro
status: docs-checked
description: "Size a Redpanda cluster from network bandwidth, 2 GB memory per core, 2 MB per partition replica and a 100 MB/sec per core rule of thumb."
sources:
  - https://docs.redpanda.com/streaming/current/deploy/redpanda/manual/sizing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Size for throughput after compression, topic replication factor, and the number of producers and consumers. Choose node count from the criteria below, then add nodes for fault tolerance so a degraded cluster still runs at full throughput.

- **Network:** total bandwidth must cover peak simultaneous writes and reads multiplied by the replication factor. Worked example from the page: three nodes, one single-partition topic with replication factor three, one producer and one consumer. For every 75 MB written to the leader, 150 MB goes to other nodes for replication and 75 MB to the consumer. Intra-cluster full duplex is 150 MB/sec, plus 75 MB/sec ingress and 75 MB/sec egress half duplex. More replicas or consumers raise it.
- **Memory per core:** at least 2 GB per CPU core.
- **Memory per partition:** at least 2 MB per partition replica. Ten thousand partitions at replication factor 3 is 10,000 x 3 x 2 MB = 60 GB across brokers, or 20 GB each on three brokers.
- **CPU:** Redpanda handles roughly 1 GB/sec of writes per core depending on workload; two cores saturate one NVMe disk; the general recommendation is 100 MB/sec per core.
- Redpanda bypasses the Linux page cache and manages its own memory and disk I/O.

**Measure the network.** Cloud networks can burst with I/O credits, so soak test (the page uses `iperf3 -c redpanda1 -p 5201 -t 300` against `iperf3 -s`) for every route pair rather than trusting a short test.

**Before benchmarking** set production mode and run `rpk redpanda tune all` on every node.

## Checked

2026-11-08. Read the whole Sizing Guidelines page. Confirmed: sizing variables, network example (75 MB written, 150 MB replicated, 75 MB to consumer), 2 GB per core, 2 MB per partition replica and the 60 GB example, roughly 1 GB/sec per core, two cores per NVMe disk, 100 MB/sec per core recommendation, page cache bypass, iperf3 soak test, production mode and rpk redpanda tune all before benchmarking. Nothing removed.

Method: documentation only; no commands were run.
