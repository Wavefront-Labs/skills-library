---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.carbon-aware-scheduling
name: carbon-aware-scheduling
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-sustainability, carbon-aware-scheduling, demand-shaping, carbon-aware-sdk, time-shifting]
level: practitioner
status: draft
description: "Shape demand and schedule flexible work by grid carbon intensity: time and location shifting, Carbon Aware SDK, deadlines, and measuring the effect."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/alignment-to-demand.html", "https://github.com/Green-Software-Foundation/carbon-aware-sdk", "https://learn.microsoft.com/azure/well-architected/sustainability/sustainability-application-design", "https://sci-guide.greensoftware.foundation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Carbon-aware scheduling and demand shaping

## Techniques
- **Time shifting**: run flexible jobs (batch, ML training, report generation, backups,
  CI-heavy workloads) when grid intensity is forecast to be lowest.
- **Location shifting**: run in the lowest-intensity allowed region at run time.
- **Demand shaping**: degrade non-essential features (lower video quality, defer
  recommendations refresh) when intensity is high; the Green Software Foundation pattern.
- **Buffering and queueing** to smooth peaks so less capacity is provisioned.

## Steps
1. **Classify work** by flexibility: deadline (must finish by 06:00), window, and whether it is
   region-portable (data residency, data location).
2. **Get forecasts**: Green Software Foundation Carbon Aware SDK (Web API / CLI) wrapping
   WattTime or Electricity Maps; returns the optimal window for a given duration and location set.
3. **Integrate with schedulers**: compute start time before submitting (Airflow, Argo,
   Kubernetes CronJob with a pre-step, KEDA carbon-aware scaler for scaling flexible workloads).
4. **Respect deadlines**: fall back to running immediately if no low window exists before deadline.
5. **Measure**: Software Carbon Intensity (SCI) = ((E x I) + M) per functional unit; compare
   shifted vs unshifted intensity.

## Gotchas
- Shifting all flexible work to the same window recreates a peak and may raise cost.
- Location shifting moves data and may breach residency; check constraints first.

## Verify
- [ ] Flexible jobs tagged with deadline and scheduled using forecasts.
- [ ] Reported average grid intensity of shifted jobs lower than baseline.
