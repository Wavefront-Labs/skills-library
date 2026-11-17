---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.carbon-aware-region-selection
name: carbon-aware-region-selection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-sustainability, carbon-aware-region-selection, grid-carbon-intensity, region-selection, green-software]
level: practitioner
status: draft
description: "Select lower-carbon regions: grid carbon intensity data, provider carbon-free energy figures, trading off latency, residency and cost."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/region-selection.html", "https://cloud.google.com/sustainability/region-carbon", "https://learn.microsoft.com/azure/well-architected/sustainability/sustainability-application-platform", "https://www.electricitymaps.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Low-carbon region selection

Region choice is often the largest single carbon lever for a workload: grid intensity varies
by an order of magnitude between regions.

## Steps
1. **Gather data**: Google publishes per-region carbon-free energy percentage (CFE%) and grid
   intensity (gCO2eq/kWh); AWS Well-Architected sustainability pillar recommends regions near
   renewable projects and lists regions with high renewable share; Electricity Maps and
   WattTime give live and historical grid intensity by zone.
2. **Constraints first**: data residency, latency to users, required services available,
   price. Carbon is a tie-breaker or weighted criterion within allowed regions.
3. **Batch and non-latency-sensitive work** (training, analytics, CI, backups) is the easiest
   to place in the lowest-carbon allowed region.
4. **Account for data movement**: shipping large data across regions costs egress and energy.
5. **Record** the carbon criterion in the region ADR, with the data source and date.
6. **Measure** with provider carbon tools after the move.

## Gotchas
- Provider market-based figures (with renewable purchases) differ from location-based grid
  figures; state which you use.
- Grid intensity changes over years; revisit periodically.

## Verify
- [ ] Region ADRs include a carbon criterion with source.
- [ ] Batch workloads placed in the lowest-carbon permitted region.
