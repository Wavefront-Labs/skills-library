---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.maturity-assessment
name: maturity-assessment
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-assessment, maturity-assessment, finops-assessment-framework, capability-scoring, finops-assessment-lenses, target-maturity]
level: practitioner
status: docs-checked
description: "Run a FinOps capability assessment: target scope and group, five lenses scored 0 to 4, lens weighting, target scores and gap-driven focus areas."
sources: ["https://www.finops.org/framework/capabilities/finops-assessment/", "https://www.finops.org/wg/finops-assessment/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Capability maturity scoring

The FinOps Foundation assessment is a high-level overview, not precise analytics. It identifies
targeted areas for the FinOps team to investigate or develop.

## Steps
1. **Define scope**: Target Scope (which capabilities) and Target Group (which part of the organisation). Focus on a few capabilities with high business value; an organisation new to FinOps would look at foundational ones such as Allocation, Reporting and Analytics, Data Ingestion, Rate Optimization, Workload Optimization and Education, and a later-stage one at Forecasting, Budgeting, Invoicing and Chargeback and Unit Economics.
2. **Weight lenses**: Knowledge, Process, Metrics, Adoption and Automation. Weight higher what is realistic and most important now (for example, if little knowledge or process exists, reduce the weight of Automation).
3. **Set Target Scores**: with five lenses each scoring up to 4, a capability has a maximum of 20; a target of 12 of 20 may be good enough for a new capability.
4. **Measure**: run discovery questions, gather evidence and score each lens. Score each capability as a percentage of the potential maximum, applying weights, and aggregate across capabilities.
5. **Outcome**: look at the pattern by lens. A zero in Metrics or Automation shows a capability that works through human effort with no proof of effectiveness.
6. **Focus**: choose specific actions and prioritise by which capabilities the next roadmap stage relies on.
7. **Repeat** with the same Target Scope, Target Group and criteria so changes are trendable, and keep a record of the scope with each baseline.

## Gotchas
- Metrics lens scores how measurements are defined and used, not how good the numbers are.
- There is no need to operate at higher lens levels in all cases; read the next level up to decide if it adds value.

## Verify
- [ ] Scores per capability and lens, with evidence and recorded scope.
- [ ] Target Scores and lens weights are agreed before measuring.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Foundation FinOps Assessment capability page and the FinOps Assessment working group guide (read in full except the Acknowledgements and the individual lens level descriptions, which were skimmed).
Removed as unconfirmed: the maturity-model citation, the list of example capabilities to select, the crawl/walk/run anchors alternative scale, the 6-12 month repeat interval, and the persona interview list.
