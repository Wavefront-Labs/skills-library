---
id: computing-software.cloud-infrastructure-engineering.aws.well-architected-cost-optimization-pillar-practices
name: well-architected-cost-optimization-pillar-practices
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, well-architected, cost-optimization-pillar, cloud-financial-management, expenditure-awareness, rightsizing, commitments]
level: practitioner
status: docs-checked
description: "Well-Architected Cost Optimization pillar in practice: financial management, expenditure awareness, cost-effective resources, demand and continuous review."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html", "https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Well-Architected Cost Optimization pillar practices

The pillar has 11 questions (COST 1 to COST 11) with numbered best practices (for example `COST01-BP01`). Use the
lists below as an evidence checklist; titles are from the Cost Optimization pillar contents page.

## Practice cloud financial management (COST 1)
- [ ] COST01-BP01/BP02: ownership of cost optimization and a partnership between finance and technology.
- [ ] COST01-BP03 to BP06: budgets and forecasts, cost awareness in organisational processes, reporting and
      notification, proactive cost monitoring.
- [ ] COST01-BP07 to BP09: keep up with new releases, a cost-aware culture, quantify the business value of
      optimisation.

## Expenditure and usage awareness (COST 2-4)
- [ ] COST02: usage policies, goals and targets, account structure, groups and roles, cost controls, project
      lifecycle tracking.
- [ ] COST03: detailed information sources, organisation information added to cost and usage, attribution
      categories, organisation metrics, billing and cost management tools configured, costs allocated by workload
      metrics (unit costs).
- [ ] COST04: resources tracked over their lifetime; a decommissioning process; decommission, and automate it;
      enforce data retention policies.

## Cost-effective resources (COST 5-8)
- [ ] COST05: requirements and component analysis when selecting services; cost-effective software licensing;
      cost analysis for different usage over time.
- [ ] COST06: cost modelling; resource type, size and number chosen from data or automatically from metrics;
      shared resources considered.
- [ ] COST07: pricing model analysis, Regions chosen on cost, third-party agreements with efficient terms, pricing
      models for all components, analysis at the management account level.
- [ ] COST08: data transfer modelled; components and services chosen to reduce data transfer cost.

## Manage demand and supply (COST 9)
- [ ] COST09: analyse workload demand, buffer or throttle to manage demand, supply resources dynamically.

## Optimise over time (COST 10-11)
- [ ] COST10: a workload review process and regular reviews of the workload.
- [ ] COST11-BP01: automation for operations where its cost is justified.

## Review tips
Evidence: cost views by allocation tag or category, budget list, commitment coverage and utilisation reports,
right-sizing recommendations with actions taken. Typical high-risk findings: no cost allocation, no budgets, no
decommissioning process, unmanaged data retention.

## Verify
- [ ] Cost pillar answered with links to reports; top 3 savings actions with owners and estimated savings.
- [ ] A unit cost metric (COST03-BP06) defined and trended.

## Checked
Date: 2026-10-27. Documentation release: AWS Well-Architected Cost Optimization pillar (latest). Confirmed: question
and best-practice numbering and titles COST01-BP01 to COST11-BP01 against the pillar contents page. Removed
specifics no page confirmed: the "coverage below 50%" threshold, Graviton, gp3, NAT gateway and S3 traffic claims, and
named product lists (Compute Optimizer, Cost Anomaly Detection, CUR). Replaced prose-title `sources` with real URLs.
Prices were not checked.
Method: documentation only; no commands were run.
