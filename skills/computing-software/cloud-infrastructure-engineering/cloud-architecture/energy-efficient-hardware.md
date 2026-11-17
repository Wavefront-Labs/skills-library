---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.energy-efficient-hardware
name: energy-efficient-hardware
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, sustainability, energy-efficient-hardware, graviton, arm64, ampere, accelerators, instance-family-selection]
level: practitioner
status: draft
description: "Choose energy-efficient cloud hardware: Arm instances, current-generation families, accelerators matched to workload, and measuring performance per watt and per carbon."
sources: ["https://aws.amazon.com/ec2/graviton/", "https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/hardware-and-services.html", "https://learn.microsoft.com/azure/virtual-machines/sizes/cobalt-overview", "https://cloud.google.com/compute/docs/instances/arm-on-compute"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Energy-efficient hardware choice

## Steps
1. **Prefer Arm where software allows**: AWS Graviton (provider states up to 60% less energy
   for the same performance), Azure Cobalt 100 and Ampere Altra, Google Axion and Tau T2A.
   Check language runtimes, native dependencies and container images for `linux/arm64`.
2. **Use current generations.** Newer families deliver more work per watt; migrate off old
   generations (for example m4/m5 to m7g/m8g) during routine refreshes.
3. **Match accelerators to the work**: GPUs for training, purpose-built inference chips
   (AWS Inferentia, Google TPU) for steady inference, and CPUs for small models. Underused GPUs
   are the largest single waste; share via MIG or time-slicing.
4. **Benchmark** candidate families with your workload: throughput per vCPU-hour and p99
   latency; convert to cost and estimated emissions per unit of work.
5. **Build multi-arch images** (`docker buildx build --platform linux/amd64,linux/arm64`) and
   run mixed node pools so schedulers can pick the efficient option.
6. **Use managed services that run on efficient hardware** (many managed databases, caches and
   serverless runtimes offer Arm options, e.g. Lambda `arm64`, RDS Graviton classes).
7. Record the choice and its measured efficiency gain in the architecture decision record.

## Gotchas
- Emulated amd64 containers on Arm (QEMU) are slow and waste energy; build native.
- Some licensed software (and some SIMD-optimised libraries) is x86-only; check first.
- Burstable instances with exhausted credits deliver poor work per watt under sustained load.

## Verify
- [ ] Share of compute on Arm / current generation tracked.
- [ ] Benchmarks show per-unit work improvement for migrated workloads.
