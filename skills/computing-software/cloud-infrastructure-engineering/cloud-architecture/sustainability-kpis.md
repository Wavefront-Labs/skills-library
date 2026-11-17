---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.sustainability-kpis
name: sustainability-kpis
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, sustainability, sustainability-kpis, carbon-intensity, proxy-metrics, green-software, science-based-targets]
level: practitioner
status: draft
description: "Define cloud sustainability KPIs: carbon per unit of work, proxy metrics like utilisation and storage growth, targets tied to corporate goals, and review cadence."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/evaluate-specific-improvements.html", "https://sci-guide.greensoftware.foundation/", "https://sciencebasedtargets.org/", "https://learn.microsoft.com/azure/well-architected/sustainability/sustainability-get-started"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sustainability KPIs and targets

## Steps
1. **Anchor to corporate targets** (for example an SBTi-validated reduction path) so cloud
   KPIs show their contribution.
2. **Pick an intensity KPI** per workload: kgCO2e per transaction, per active user, per GB
   processed, or the Green Software Foundation SCI score (`(E x I + M) per R`). Intensity
   lets the business grow while efficiency improves.
3. **Add proxy metrics** that update daily, because provider carbon data lags months. The AWS
   Sustainability Pillar recommends proxies such as vCPU-hours, storage GB-months, data
   transferred, per business outcome:
   - average CPU/GPU utilisation of steady fleets
   - share of compute on Arm or current generations
   - storage under lifecycle policies; data growth rate
   - non-production hours off; idle resource count
   - share of workload in low-carbon regions
4. **Set targets** per KPI with owners and dates (for example "vCPU-hours per 1k orders down
   20% by Q4").
5. **Instrument**: join CUR/billing usage with business metrics in the data warehouse; publish
   a dashboard next to cost (FinOps and GreenOps share data).
6. **Review** quarterly in architecture or FinOps forums; feed regressions into backlogs.

## Gotchas
- Absolute emissions alone punish growth; pair with intensity.
- Market-based provider numbers can hide efficiency regressions; proxies reveal them.
- Too many KPIs dilute focus; 3-5 per workload.

## Verify
- [ ] Each major workload has one intensity KPI and 2-4 proxy metrics with targets.
- [ ] Dashboard refreshes at least daily for proxies.
