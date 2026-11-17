---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.arm64-migration
name: arm64-migration
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, compute-selection, arm64-migration, graviton, cobalt, axion, multi-arch-images]
level: practitioner
status: docs-checked
description: "Migrate workloads to ARM (Graviton, Cobalt, Axion): compatibility audit, multi-arch builds, performance and price testing, staged rollout and fallback."
sources: ["https://github.com/aws/aws-graviton-getting-started", "https://learn.microsoft.com/azure/virtual-machines/sizes/cobalt-overview", "https://cloud.google.com/compute/docs/instances/arm-on-compute", "https://docs.docker.com/build/building/multi-platform/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating workloads to ARM processors

## Steps
1. **Pick candidates and platforms**: AWS Graviton, Azure Cobalt 100 VMs and Google Axion (N4A
   and C4A Compute Engine series) are the Arm options. The Graviton getting-started guide has
   per-language pages for Java, .NET, Node.js, Python, Go and Rust, and a table of minimum
   versions with Arm optimisations (for example .NET 8 or later, pip 19.3 or later for wheels).
2. **Compatibility audit**: native dependencies (Python wheels, Node native modules, JNI
   libraries), closed-source agents (monitoring, security), base images lacking arm64.
   A linux/amd64 container cannot run on an arm64 host without emulation.
3. **Multi-arch builds**: `docker buildx build --platform linux/amd64,linux/arm64 .` produces a
   multi-platform image (a manifest list). QEMU emulation requires no Dockerfile change but can
   be much slower than native builds, especially for compilation; Docker recommends multiple
   native nodes or cross-compilation instead.
4. **Benchmark** on your workload: compare throughput and p99 latency per dollar against the
   x86 instance. Google says Arm can yield better price-performance; verify for your workload.
5. **Kubernetes**: you can run Docker, Kubernetes, ECS and EKS on Graviton, and AKS runs on
   Cobalt 100 VMs; use a mixed-architecture node pool during the transition.
6. **Roll out** canary by canary with an x86 fallback until stable.

## Gotchas
- One amd64-only sidecar image blocks the whole pod from ARM nodes.
- Compiler flags and SIMD-optimised libraries may need ARM builds for parity; the Graviton guide has an assembly optimisation page.

## Verify
- [ ] All images in the workload publish arm64 manifests.
- [ ] Price-performance measured on production-like load.

## Checked
2026-11-08. Confirmed against the four cited pages: Graviton getting-started README (language pages, minimum-version table incl. .NET 8+ and pip 19.3+, containers/ECS/EKS support, assembly optimisation page), Azure Cobalt 100 VM overview (Cobalt 100 series, AKS on Cobalt), Google Arm on Compute page (N4A and C4A on Axion, price-performance wording) and Docker multi-platform builds (--platform command, manifest list, QEMU slower, native nodes, linux/amd64 on arm64 needs emulation). The per-language pages linked from the Graviton README were not opened. Removed: Java 11+, .NET 6+ and managed-service (RDS, ElastiCache, OpenSearch) claims, Karpenter and node-label advice, "typically show better price performance" for all three clouds.
Method: documentation only; no commands were run.
