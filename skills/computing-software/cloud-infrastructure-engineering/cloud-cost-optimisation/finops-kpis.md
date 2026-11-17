---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.finops-kpis
name: finops-kpis
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-kpis, kpi-formulas, effective-savings-rate, forecast-accuracy, commitment-utilisation]
level: practitioner
status: docs-checked
description: "Core FinOps KPI formulas as published in the Framework capability pages: ESR, commitment utilisation and waste, forecast accuracy, unit and data KPIs."
sources: ["https://www.finops.org/framework/capabilities/rate-optimization/", "https://www.finops.org/framework/capabilities/unit-economics/", "https://www.finops.org/framework/capabilities/data-ingestion/", "https://www.finops.org/framework/capabilities/reporting-analytics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FinOps KPIs and their published formulas

The Framework attaches KPIs to each capability page. These are the formulas that appear there.
Define each KPI precisely (candidate data sources, cost basis, scope) before publishing it.

| KPI | Formula as published | Capability |
|---|---|---|
| Effective Savings Rate % | Option 1: (CB discount savings - cost to achieve them) / compute on-demand equivalent spend. Option 2: 1 - (actual spend with discounts / equivalent spend at on-demand rate) | Rate Optimization |
| Commitment Utilization Score | (Used commitment / total commitment) x 100 | Rate Optimization |
| Commitment discount waste % | (Cost of unused commitment discount / total cost of commitment discount) x 100 | Rate Optimization |
| Consumption versus Commitment (SaaS) | Actual consumption units / committed units | Rate Optimization, Licensing and SaaS |
| Forecast accuracy rate (spend) | (Forecasted - actual public cloud spend) / forecasted public cloud spend | Forecasting |
| Forecast accuracy rate (usage) | (Forecasted - actual resource utilisation) / forecasted resource utilisation, for a specific service name, category or SKU | Forecasting |
| Cost per GB stored | Cloud storage costs / number of GB stored | Unit Economics |
| Cost per API call | Total API costs / number of API calls | Unit Economics |
| Cost visibility delay | Time of displaying cost - time of cost generation | Data Ingestion |
| Data update frequency | Time of latest cost update - time of previous update | Data Ingestion |
| ETL processing time | End time - start time | Data Ingestion |

## Reading the KPIs
- Commitment utilisation near 100 percent suggests good forecasting; much lower values signal
  wasted capital, and values over 100 percent mean exposure to on-demand rates.
- Under-utilised commitments and significant usage not covered by discounts both reduce ESR.
- Each organisation defines its own acceptable forecast variance; percent variance is the primary
  measure and dollar differences can also help.
- Overall tagging compliance above 90 percent is listed as a Reporting and Analytics measure of
  success.
- Cost avoidance is future spend prevented (not a reduction from the existing run rate) and needs a
  documented counterfactual baseline.

## Steps
1. Choose KPIs that match the capabilities you are maturing, not every KPI in the library.
2. Write each definition down: formula, cost basis, scope and data source, plus an owner.
3. Compute them automatically from the repository so trends stay comparable.
4. Review on a cadence and retire KPIs that stop informing decisions.

## Checked
Method: docs-checked 2026-11-09 against the Rate Optimization, Unit Economics, Data Ingestion and Reporting and Analytics capability pages (KPI sections read) plus the Forecasting and Benchmarking pages for the forecast accuracy and cost avoidance statements.
Removed as unconfirmed: allocated spend percent, commitment coverage, waste percent of total spend and anomaly MTTR formulas, the utilisation target of 95 percent or more, the maturity-to-KPI mapping, the 5 to 8 KPI count, and the KPI library and ESR how-to sources (individual entries not readable, or 404).
