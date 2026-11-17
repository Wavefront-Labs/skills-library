---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-dashboards
name: cost-dashboards
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-reporting, cost-dashboards, persona-dashboards, engineering-cost-view, executive-cost-view, quicksight, power-bi, looker-studio, cudos]
level: practitioner
status: docs-checked
description: "Build cost dashboards per persona using the FinOps Reporting and Analytics capability: needs by persona, terminology, self-service, data in the path and maturity steps."
sources: ["https://www.finops.org/framework/capabilities/reporting-analytics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Persona-specific cost dashboards

The FinOps Reporting and Analytics capability defines reporting broadly (reports, dashboards,
data feeds and APIs) and asks for mechanisms that serve each persona group's needs. Its outputs
include context-specific analysis curated by persona (Finance, Engineer, Product,
Sustainability, Leadership).

## Steps
1. **Ask each persona** how data should be presented, sorted, summarised and delivered. The page
   has Finance, Procurement, Product, Leadership and Allied Personas give that guidance, and the
   FinOps practitioner works with every group on the metrics and metadata in "official" output.
2. **Define common terminology precisely** and set guidelines on data sensitivity and who sees
   which data.
3. **Provide dashboards centrally to teams** (Walk), with custom views and aggregations,
   granular reporting for KPI tracking and showback, and enriched data such as synthetic tags.
4. **Put data in the path**: push analytics results into dashboards and work queues engineers
   already use (Run), and enable teams to self-serve.
5. **Show estimates beside actuals**: Walk adds a projected-versus-actual view for decisions
   that carried a documented estimate.
6. **Report key dates** for renewals and expiries of commitments, marketplace purchases, BYOL
   usage and SaaS services.

## Measures of success on the page
- Overall tagging compliance above 90 percent.
- Context-relevant cost reporting available to all core personas.
- Self-service reporting and ad hoc analysis of anomalies, utilisation, outliers, budgets and
  forecast variances.
- Reduced investigative time for usage and cost questions.

## Verify
- [ ] Each persona has a view built from their stated needs.
- [ ] Self-service use is tracked and teams rely less on the central FinOps team.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Reporting and Analytics capability page (read in full). The AWS Cloud Intelligence Dashboards workshop and Microsoft FinOps toolkit pages were not read and were dropped. Removed unconfirmed: the persona table of grain and cost view, the interview count, the tooling list, data-as-of labelling, row-level security, and the gotchas on billed versus amortised mixing and daily minimum.
