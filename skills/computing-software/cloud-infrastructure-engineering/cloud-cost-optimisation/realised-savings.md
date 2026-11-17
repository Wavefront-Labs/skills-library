---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.realised-savings
name: realised-savings
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-assessment, realised-savings, savings-tracking, cost-avoidance]
level: practitioner
status: docs-checked
description: "Track realised savings credibly: separate cost savings from cost avoidance, document baselines before acting, validate outcomes and report rate savings via ESR."
sources: ["https://www.finops.org/framework/capabilities/benchmarking/", "https://www.finops.org/framework/capabilities/rate-optimization/", "https://www.finops.org/framework/capabilities/workload-optimization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tracking realised savings

## Definitions (FinOps Framework wording)
- **Cost savings / cost reduction**: a reduction from the existing run rate (deleted idle resources, a rightsized instance).
- **Cost avoidance**: future expenditure prevented, not a reduction from the existing run rate. A credible claim needs
  a documented counterfactual baseline, consistent demand and service assumptions, intervention evidence, a defined
  time horizon and post-action validation.
- **Rate savings**: the effect of commitment-based discounts, measured as the Effective Savings Rate (ESR).

Report the three separately. The Framework lists "separate avoidance, savings, and cost reduction measurements" as a
FinOps Practitioner activity.

## Steps
1. **Record the baseline and counterfactual before the intervention**, then the intervention and outcome evidence
   (the Framework's Walk-stage behaviour; at Crawl, avoidance is asserted with no baseline).
2. **Log every action** with resource, date, owner and the estimated saving, in a tracker that follows each
   recommendation from identification to resolution.
3. **Compare estimate with actual** once the change is live, and feed the variance back into future estimates
   (the Run-stage behaviour).
4. **Rate optimisation**: use the Framework's ESR formulas: 1 minus (actual spend with discounts divided by the
   equivalent spend at on-demand rates), or (commitment discount savings minus the cost to achieve them) divided by
   the on-demand-equivalent spend. Unused commitments and usage not covered by discounts lower ESR.
5. **Account for the cost of acting**: the Framework says to weigh expected savings or avoidance against the full cost
   of the change (labour hours, disruption, complexity).
6. **Report** realised savings by category and owning team, and track the share of recommendations acted on and the
   time to resolution.

## Gotchas
- Mixing avoidance into reduction numbers damages credibility with finance.
- A claim with no documented baseline is an assertion, not a saving.

## Verify
- [ ] Each claim records baseline, intervention and outcome evidence, and is tagged as savings, reduction or avoidance.
- [ ] Finance has reviewed the method.

## Checked
Confirmed on the FinOps Framework KPIs and Benchmarking page (avoidance versus savings definition, counterfactual
baseline requirements, Crawl/Walk/Run baseline behaviour, separating avoidance, savings and reduction), the Rate
Optimization page (both ESR formulas, effect of under-utilisation) and the Usage Optimization page (ROI and
tracking of recommendations from identification to resolution). Removed: 12-month cap on annualised claims, 30-day
persistence check, FOCUS column names ListCost, ContractedCost, EffectiveCost, the Cost Explorer reference, and the
finops-assessment and key-performance-indicators source pages (assessment page does not cover savings; the KPI page
404s).
Method: docs-checked 2026-11-09 against finops.org Framework KPIs and Benchmarking, Rate Optimization and Usage Optimization capability pages
