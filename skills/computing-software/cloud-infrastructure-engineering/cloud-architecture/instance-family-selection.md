---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.instance-family-selection
name: instance-family-selection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, compute-selection, instance-family-selection, arm-graviton, processor-architecture, burstable-instances]
level: practitioner
status: draft
description: "Choose instance family, size and processor architecture: vCPU-to-memory ratio, x86 vs ARM, burstable credits, network and storage limits, and benchmarking."
sources: ["https://aws.amazon.com/ec2/instance-types/", "https://learn.microsoft.com/azure/virtual-machines/sizes/overview", "https://cloud.google.com/compute/docs/machine-resource", "https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/compute-and-hardware.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Instance family and processor architecture choice

## Families
- General purpose (about 4 GiB per vCPU): AWS M, Azure D, GCP N/E2/C4 standard.
- Compute optimised (about 2 GiB/vCPU): AWS C, Azure F, GCP C/H.
- Memory optimised (8+ GiB/vCPU): AWS R/X, Azure E/M, GCP M/highmem.
- Storage optimised (local NVMe): AWS I/D, Azure L.
- Burstable (credit-based): AWS T, Azure B, GCP shared-core E2.

## Steps
1. **Profile the workload**: CPU vs memory bound, memory per vCPU needed, network bandwidth,
   EBS/managed disk throughput needs (instance types cap disk throughput and IOPS), local disk.
2. **Pick ratio then generation**: latest generation usually gives better price-performance.
3. **Processor**: ARM (AWS Graviton, Azure Cobalt/Ampere, GCP Axion/Tau T2A) often 20-40%
   better price-performance for Linux workloads with ARM builds (Java, Go, Python, Node,
   containers built multi-arch); x86 Intel vs AMD differ by price and per-core licensing.
4. **Burstable only for low average CPU** (below baseline, e.g. 10-40% depending on size);
   watch credit balance; T unlimited mode bills surplus credits.
5. **Benchmark** the real workload on 2-3 candidates (throughput per dollar), not synthetic only.
6. **Licensing**: per-core licences favour high-frequency, fewer-core or constrained-vCPU sizes.

## Gotchas
- Network bandwidth "up to" figures are burst; sustained baseline is lower on small sizes.
- vCPU means a hyperthread on most x86 types but a full core on Graviton.

## Verify
- [ ] Benchmark results (cost per unit of work) recorded for chosen type.
- [ ] Disk and network limits of the size exceed measured peak needs.
