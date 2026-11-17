---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.savings-baseline
name: savings-baseline
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-assessment, savings-baseline, waste-assessment, savings-potential]
level: practitioner
status: docs-checked
description: "Baseline waste and savings potential: categorise opportunities, estimate savings and effort, balance usage against rate optimisation and freeze a dated baseline."
sources: ["https://www.finops.org/framework/capabilities/workload-optimization/", "https://www.finops.org/framework/capabilities/benchmarking/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Waste and savings potential baseline

## Steps
1. **Collect opportunities** from billing data, infrastructure monitoring, observability and data-efficiency tools, plus
   your cloud provider's and third parties' recommendation services. Utilisation and performance data are needed
   alongside cost data.
2. **Categorise** using the Framework's usage optimisation types: waste reduction (stranded volumes, excessive
   backups or snapshots, unused sandboxes, redundant licences, inactive SaaS entitlements), workload management
   (start/stop scheduling, with pre-production the biggest target), scaling, rightsizing, licence and SaaS
   optimisation, temporal and geographic shifting, and modernisation (newer generations and tiers). For storage,
   estimate latent inefficiency (infrequently accessed data in a high-performance tier, compressible but uncompressed data).
3. **Estimate savings and the cost of acting** for each opportunity: expected saving, plus labour, disruption and any
   tooling cost, so the baseline shows return on investment and not only gross potential.
4. **Balance usage against rate optimisation**: the Framework says the strategy should set guidelines for balancing
   workload optimisation against commitment-based approaches, so rank them together rather than summing separately.
5. **Check usage patterns before rightsizing**: the Framework warns of longer-cycle peaks (month-end, quarterly) and
   resources with warranty, contractual or software requirements.
6. **Document the baseline and method with a date.** The Framework requires a baseline and counterfactual to be
   documented before an intervention is credited with avoided cost; the frozen baseline is the reference for realised
   savings.

## Gotchas
- Summing every tool's recommendations without ranking or de-duplicating them overstates potential.
- Rightsizing typically means recreating or reconfiguring resources, which can disrupt service.

## Verify
- [ ] Baseline document records sources, categories, method, date and owners.
- [ ] Each opportunity carries an estimated saving and an estimated cost of acting.

## Checked
Confirmed on the FinOps Framework Usage Optimization page (optimisation type list, storage latent inefficiency,
cost-of-acting and ROI estimation, balance with rate optimisation, long-cycle peak warning, rightsizing disruption)
and the KPIs and Benchmarking page (baseline and counterfactual documented before crediting avoidance). Removed:
the realisation rates (idle 80-90 percent, rightsizing 40-60 percent), the 30-day lookback, the named provider
services (Cost Optimization Hub, Azure Advisor, Google Recommender) and the claim that Cost Optimization Hub
de-duplicates by default, plus the finops-assessment, AWS and Microsoft sources.
Method: docs-checked 2026-11-09 against finops.org Framework Usage Optimization and KPIs and Benchmarking capability pages
