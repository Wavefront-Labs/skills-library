---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.utilisation-efficiency
name: utilisation-efficiency
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, sustainability, utilisation-efficiency, green-software, rightsizing, autoscaling, bin-packing, idle-resources]
level: practitioner
status: docs-checked
description: "Raise utilisation to cut cloud carbon: right-size, autoscale, remove idle and oversized resources, use scale-to-zero serverless, and balance against reliability headroom."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html", "https://learn.greensoftware.foundation/", "https://learn.microsoft.com/azure/well-architected/sustainability/sustainability-application-platform", "https://cloud.google.com/architecture/framework/sustainability"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Maximising utilisation for sustainability

## Steps
1. **Baseline utilisation** per workload from your provider's monitoring. Azure guidance notes workloads are often
   designed for peak demand rather than actual utilisation, leaving idle VMs, oversized AKS clusters and unused resources.
2. **Right-size** VMs and container requests to measured demand (Google Cloud and Azure both list right-sizing).
3. **Autoscale**: Google calls for aggressive autoscaling; Azure lists autoscaling effectively as a cost and
   sustainability lever.
4. **Eliminate idle or redundant resources**; Azure calls removing waste "often the first and most effective
   sustainability improvement".
5. **Use serverless services that scale to zero** where they fit (Google Cloud customer responsibilities).
6. **Manage data lifecycles**: archive old data and avoid unnecessary replication and data movement.
7. **Trim telemetry**: excessive logs, traces and long retention add storage and processing overhead.
8. **Choose low-carbon regions** where requirements allow (a Google Cloud sustainability principle).
9. **Measure**: carbon can be measured with the GHG Protocol or the Software Carbon Intensity specification (Green
   Software Foundation training). Track utilisation alongside carbon reports.

## Gotchas
- Resilience trades against efficiency: multiregion and active-active designs add excess capacity (Azure). Aim for
  resiliency objectives without unnecessary overprovisioning, not zero headroom.
- Performance work can need extra caching, replication, memory or compute, so check the net effect.
- Scale-to-zero may affect latency; verify against your SLOs.

## Verify
- [ ] Utilisation of steady fleets tracked over time.
- [ ] Idle and orphaned resources reviewed on a schedule.

## Checked
2026-11-08. Confirmed against the Azure sustainable workloads page (overprovisioning, idle VMs and oversized AKS,
removing waste first, reliability and telemetry trade-offs), the Google Cloud Well-Architected sustainability pillar
(right-size, aggressive autoscaling, archive data, eliminate idle resources, scale-to-zero serverless, low-carbon
regions principle) and the Green Software Foundation training welcome page (GHG Protocol and SCI measurement). The AWS
sustainability pillar page is an introduction only. Removed: the 14-30 day window, Compute Optimizer, Advisor,
Recommender, KEDA, Karpenter, Instance Scheduler, Arm and bin-packing advice, embodied carbon claim and spot guidance
(not stated on these pages).
Method: documentation only; no commands were run.
