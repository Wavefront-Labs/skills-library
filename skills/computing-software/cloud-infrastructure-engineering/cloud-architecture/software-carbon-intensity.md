---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.software-carbon-intensity
name: software-carbon-intensity
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-sustainability, software-carbon-intensity, sci-specification, iso-iec-21031, green-software-foundation, carbon-per-unit]
level: practitioner
status: draft
description: "Measure software carbon intensity with the Green Software Foundation SCI spec (ISO/IEC 21031): energy, grid intensity, embodied emissions per functional unit."
sources: ["https://sci.greensoftware.foundation/", "https://www.iso.org/standard/86612.html", "https://www.cloudcarbonfootprint.org/docs/methodology"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Software Carbon Intensity measurement

## Formula
`SCI = ((E x I) + M) per R`
- **E**: energy consumed by the software (kWh) over the time window.
- **I**: location-based marginal or average grid carbon intensity (gCO2e/kWh) where it runs.
- **M**: embodied emissions of hardware, apportioned by time share and resource share.
- **R**: functional unit (per API call, per user, per job, per GB processed).
SCI is a rate for comparison over time, not a total footprint; market-based offsets/RECs are excluded.

## Steps
1. Define the software boundary (compute, storage, network, plus supporting infra you control).
2. Choose R aligned with business value (same as unit economics where possible).
3. Estimate E: from utilisation x power models (Cloud Carbon Footprint coefficients, instance
   power data), or provider-reported data where available.
4. I: grid intensity data (Electricity Maps, WattTime, provider region data).
5. M: hardware embodied carbon estimates apportioned by usage.
6. Compute and publish SCI with assumptions; recalculate after optimisations.

## Gotchas
- Mixing location-based and market-based numbers.
- Cloud provider dashboards report totals with lag (monthly); SCI needs finer data for engineering feedback.

## Verify
- [ ] SCI calculation documented with data sources and repeated at least quarterly.
