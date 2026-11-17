---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.rightsizing-compute-workloads
name: rightsizing-compute-workloads
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, rightsizing, compute, ec2, azure-vm, compute-engine, instance-families, burstable-instances, cpu-credits, t3, b-series, e2-shared-core, memory-metrics, cloudwatch-agent, compute-optimizer, azure-advisor, gcp-recommender, kubernetes-requests, resource-requests-and-limits, vpa, goldilocks, krr, bin-packing, karpenter, jvm-heap, graviton, arm64, scheduling, off-hours-shutdown, autoscaling]
level: practitioner
status: draft
description: "Rightsize VMs and Kubernetes pods safely: collect peak CPU and memory, pick family before size, handle burstable credits and JVM heaps, set requests from VPA data, and roll changes out with rollback."
sources: ["AWS Compute Optimizer User Guide", "Azure Advisor cost recommendations documentation", "Google Cloud Recommender - VM machine type recommendations", "Kubernetes documentation - Vertical Pod Autoscaler and resource management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rightsizing compute workloads — shrink without causing the next incident

**Goal:** VMs and containers sized to their real peak demand plus deliberate headroom, changed
through a safe rollout, and kept right as code and traffic change.

The overall cost-reduction order (allocate → waste → rightsize → commit) is in
`computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.rightsizing-and-commitments`.
This skill is the detailed rightsizing practice.

## 1. Get the right data
- Window: ≥ 14 days, ideally 30+, covering month-end jobs and weekly peaks.
- Use **p95/p99 or max of 5-minute samples**, not averages. An average 15% CPU box may hit 95% every night.
- **Memory is not collected by default** on EC2 or Compute Engine VMs (hypervisors can't see guest memory) — install the CloudWatch agent / Ops Agent / Azure Monitor agent first, or recommenders will only size on CPU.
- Include network bandwidth, EBS/disk IOPS and throughput — some instance sizes cap these, and shrinking can throttle I/O.

## 2. Family before size
1. Move to the **current generation** (often 10-20% better price-performance for the same size).
2. Match the shape: compute-optimised (c), general (m), memory (r/x), or ARM (Graviton, Azure Cobalt/Ampere, Google Axion/Tau T2A). ARM needs multi-arch images and a benchmark.
3. Then size: halve when p99 CPU < 40% and peak memory < 50% with headroom.
4. **Burstable** (AWS t-series, Azure B-series, GCP e2 shared-core) fit spiky, low-baseline workloads. Check CPU credit balance — sustained use above baseline throttles (standard mode) or bills surplus credits (unlimited mode), sometimes costing more than a fixed instance.

## 3. Use recommenders, then verify
AWS Compute Optimizer (enable enhanced infrastructure metrics for 3-month lookback),
Azure Advisor, GCP Recommender. Treat output as candidates: they don't know about planned
launches, licence-per-core software, or the batch job that runs quarterly.

## 4. Kubernetes: rightsize requests, not nodes
Node cost follows **requests**, not usage. Typical clusters have requests far above usage.
- Measure request vs usage per container (kube-state-metrics + cAdvisor; Goldilocks, KRR, Kubecost, or VPA in `updateMode: "Off"` for recommendations).
- CPU request ≈ p95 usage; CPU **limits** often omitted or generous (CPU limits cause CFS throttling at low utilisation).
- Memory request ≈ p99 usage + 10-20%; memory limit = request for predictable OOM behaviour.
- Then let Cluster Autoscaler or Karpenter consolidate nodes; Karpenter consolidation replaces underused nodes with cheaper ones.
- **JVM/runtime caveat:** the JVM reserves heap by `-Xmx` or `MaxRAMPercentage`; observed memory reflects configuration, not need. Lower the heap setting and watch GC time before cutting memory requests. Similar for .NET GC and Node `--max-old-space-size`.

## 5. Roll out safely
- One service at a time, canary one instance/AZ, compare latency SLI and error rate for a full traffic cycle.
- Keep a one-command rollback (IaC revert). Resizing a VM usually requires stop/start — schedule it.
- Track realised savings from the bill, not the recommender's estimate.

## 6. Schedule and autoscale
Non-production: stop outside working hours (~65% fewer hours for 12h × 5d). Production with
diurnal traffic: autoscale on a load metric so min capacity — not peak — runs at night.

## Gotchas
- Rightsizing then buying commitments on the *old* size locks in waste; rightsize first.
- Licences priced per vCPU (SQL Server, Oracle) can make a larger, faster instance with fewer vCPUs cheaper overall; consider optimize-CPUs options.
- Downsizing reduces network and EBS bandwidth caps.
- VPA in `Auto` mode evicts pods to apply changes — combine with PDBs, and don't run it alongside HPA on the same CPU/memory metric.

## Verify
- [ ] Memory metrics exist for every VM considered.
- [ ] Each change has before/after p95 latency and error rate for a full cycle.
- [ ] Container requests are within ~30% of p95 usage for the top-spend workloads.
- [ ] Non-prod schedules are in place and enforced by tag.
- [ ] Realised monthly savings reported from billing data.

Uncertain: percentage gains for new generations and ARM are typical vendor claims; benchmark your workload.
