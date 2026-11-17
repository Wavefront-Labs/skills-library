---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.kpi-library-selection
name: kpi-library-selection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, benchmarking, kpi-library-selection, finops-kpis, kpi-library, metrics-design, finops-framework]
level: practitioner
status: docs-checked
description: "Choose KPIs from the FinOps KPI library: tie them to organisational strategy and maturity, define and document them, and review them on a governed cadence."
sources: ["https://www.finops.org/wg/finops-kpis/", "https://www.finops.org/framework/capabilities/benchmarking/", "https://www.finops.org/framework/maturity-model/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Selecting KPIs from the FinOps KPI library

The FinOps KPI library is a community-curated collection usable regardless of cloud provider,
industry, size or maturity. It can be searched by KPI or sorted by related capability, and each KPI
shows a definition, formulas, examples and data sources.

## Steps
1. **Start from strategy.** Work with Leadership and Finance so KPIs and benchmarks connect to
   organisational strategy and executive expectations, across cost, performance, efficiency and
   sustainability dimensions.
2. **Pick what each persona can act on.** Choose KPIs that are meaningful and actionable for all
   relevant personas, and translate technology efficiency KPIs into executive-level narratives.
3. **Match ambition to maturity.** The maturity model says to prioritise capabilities that give the
   most business value; do not aim for Run everywhere. Its sample community goals:

   | Level | Allocated to a known owner | Commitment coverage target | Forecast variance |
   |---|---|---|---|
   | Crawl | at least 70% | about 60% | below 20% |
   | Walk | at least 85% | above 75% | below 10% |
   | Run | above 90% of spend allocated | above 80 | below 5% |

4. **Document each KPI**: consistent definition, formula, data sources, owner and reporting.
   Benchmarking at Crawl is often ad hoc; at Walk KPIs are standardised enough to compare teams;
   at Run reporting is automated and self-service.
5. **Governance.** Review and update KPIs iteratively so they stay aligned with business priorities,
   and retire ones that no longer serve.
6. **Baselines for savings claims.** Define the counterfactual baseline before an intervention and
   keep avoidance, savings and cost reduction separate; avoidance is future spend prevented, not a
   reduction from the current run rate.

## Verify
- [ ] Each KPI has a documented definition, data source and owner.
- [ ] KPIs are reviewed on a stated cadence and linked to organisational goals.

## Checked
Method: docs-checked 2026-11-09 against the FinOps KPI library landing page, the Framework KPIs and Benchmarking capability page and the FinOps Maturity Model page. The library's individual KPI entries load dynamically and were not read; a few formulas were seen on the Unit Economics and Data Ingestion pages.
Removed as unconfirmed: the per-persona limit of 3 to 5 KPIs, the typical KPI pick list by capability (effective savings rate, coverage and utilisation pairing), the KPI register template and the quarterly review rule.
