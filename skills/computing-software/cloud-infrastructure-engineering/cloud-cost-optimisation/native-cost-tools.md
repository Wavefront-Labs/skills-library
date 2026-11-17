---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.native-cost-tools
name: native-cost-tools
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-tools, native-cost-tools, aws-cost-explorer, azure-cost-management, gcp-billing-reports]
level: practitioner
status: draft
description: "Use native provider cost tools effectively: AWS Cost Explorer, Budgets and Data Exports, Azure Cost Management, Google Cloud Billing reports and BigQuery export."
sources: ["https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html", "https://learn.microsoft.com/azure/cost-management-billing/costs/overview-cost-management", "https://cloud.google.com/billing/docs/how-to/reports", "https://www.finops.org/framework/capabilities/finops-tools-services/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Native provider cost tools

## AWS
- **Cost Explorer**: filter/group by service, account, tag, cost category; amortised vs
  unblended views; savings plan and RI utilisation/coverage reports; forecasting.
- **Data Exports** (CUR 2.0 and FOCUS 1.x exports) to S3, query with Athena; **Cost
  Categories** for allocation rules; **Budgets** and **Cost Anomaly Detection**; **Cost
  Optimization Hub** and Compute Optimizer for recommendations.
- Enable cost allocation tags in the payer account (not retroactive).

## Azure
- **Cost Management**: cost analysis views (accumulated, by resource, amortised), budgets
  with action groups, anomaly alerts, exports (actual, amortised, FOCUS) to storage,
  cost allocation rules for shared costs, Advisor recommendations, Power BI connector.
- Scope matters: billing account / management group / subscription views differ in
  available features by agreement type (EA, MCA, CSP).

## Google Cloud
- **Billing reports** and cost table; **budgets** with Pub/Sub notifications for automation;
  **BigQuery billing export** (standard, detailed, pricing) - enable early, not retroactive;
  FinOps hub and Recommender; Looker Studio templates.

## Steps
1. Enable exports in every provider on day one into a central data store.
2. Set amortised views as defaults for team reporting.
3. Use native budgets and anomaly detection everywhere as a baseline safety net.
4. Decide where native tools stop (multi-cloud views, complex allocation) and a platform starts.

## Gotchas
- Exports and tag activation are not retroactive; delays lose history.
- Native consoles show different numbers for the same period depending on cost type selected.

## Verify
- [ ] Billing exports enabled for all providers into central storage.
- [ ] Budgets and anomaly detection active on every account/subscription/project.
