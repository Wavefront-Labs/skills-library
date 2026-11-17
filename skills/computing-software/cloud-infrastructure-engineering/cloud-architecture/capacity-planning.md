---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.capacity-planning
name: capacity-planning
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, scalability, capacity-planning, demand-forecasting, headroom, saturation, capacity-reservations, littles-law, utilisation-targets, bottleneck-analysis]
level: advanced
status: draft
description: "Plan capacity where autoscaling can't help: demand forecasts, per-instance capacity from load tests, failure headroom, non-elastic bottlenecks and reservations."
sources: ["https://sre.google/sre-book/software-engineering-in-sre/#intent-based-capacity-planning", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-reservations.html", "https://learn.microsoft.com/azure/well-architected/performance-efficiency/capacity-planning"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capacity planning

Autoscaling handles the elastic tiers; capacity planning covers everything that isn't elastic
or can't scale fast enough: databases, quotas, IP space, GPU availability, licences, third-party limits.

## Steps
1. **Demand forecast**: peak requests/s, data volume, users — from business plans and seasonality
   (Black Friday, tax deadlines), 6-18 months ahead.
2. **Per-unit capacity**: from load tests, the max throughput of one instance/shard at SLO
   latency (not at 100% CPU).
3. **Required units** = peak / per-unit capacity × (1 + headroom). Headroom covers forecast error
   and **N+1 / AZ loss** (with 3 AZs, losing one leaves 2/3 capacity — plan at ≤ ~66% utilisation at peak).
4. **Non-elastic bottlenecks**: DB write throughput, connection limits, partition throughput,
   NAT/port limits, IP addresses per subnet, provider quotas. Each has a ceiling date — when will
   growth hit it?
5. **Secure scarce capacity**: on-demand capacity reservations (EC2 ODCR, Azure capacity
   reservations, GCP reservations) for critical events or GPU workloads; raise quotas ahead.
6. Review quarterly; compare forecast vs actual peaks.

## Gotchas
- Assuming the cloud always has capacity — specific instance types/AZs do run out, especially GPUs.
- Planning on averages; peaks and burst rates matter.

## Verify
- [ ] Capacity model lists each bottleneck with current usage, ceiling and projected date.
- [ ] Peak event plans include reservations and pre-scaling.
