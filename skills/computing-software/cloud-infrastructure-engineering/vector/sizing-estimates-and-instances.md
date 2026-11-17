---
id: computing-software.cloud-infrastructure-engineering.vector.sizing-estimates-and-instances
name: sizing-estimates-and-instances
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [sizing, capacity-planning, throughput, vcpu, memory, instance-types, vector]
level: practitioner
status: docs-checked
description: "Estimate Vector instance size from per-vCPU throughput numbers and the recommended CPU and memory ratios."
sources:
  - https://vector.dev/docs/setup/going-to-prod/sizing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Most Vector workloads are CPU intensive. Starting estimates (conservative, per the docs) are per vCPU:

| Event type | Size | Throughput |
|---|---|---|
| Unstructured log | about 256 bytes | about 10 MiB/s |
| Structured log | about 768 bytes | about 25 MiB/s |
| Metric | about 256 bytes | about 25 MiB/s |
| Trace span | about 1 KB | about 25 MiB/s |

One vCPU means one ARM physical CPU or 0.5 Intel physical CPU with hyperthreading. Test your own workload when you can.

Instances: at least 8 vCPUs and 16 GiB are good units for scaling. Examples named: AWS c6i.2xlarge (recommended) or c6g.2xlarge, GCP c2 with 8 vCPUs and 16 GiB. Vector vertically scales automatically.

CPU: at least 2 vCPUs for the agent role and 4 for the aggregator. ARM64 is typically better value, and larger CPU caches help because VRL compiles to machine code.

Memory: start with 2 GiB per vCPU. More sinks use more memory for batching and buffering; add memory or move to disk buffers (slower, so prefer memory).

Disks matter only for disk buffers: choose durable generic block storage, give at least 2x peak throughput headroom, and size for about 10 minutes of data. Example: 10 MiB/s x 60 x 10 x 8 vCPUs gives 48 GiB.

## Checked

Method: docs-checked 2026-11-09 against the full Vector sizing and capacity planning page (raw markdown from the vectordotdev/vector repo). Dropped an unsourced verification line; the page rounds the disk example to 48 GiB.
