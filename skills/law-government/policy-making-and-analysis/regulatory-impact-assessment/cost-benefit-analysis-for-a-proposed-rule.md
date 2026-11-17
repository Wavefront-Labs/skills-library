---
id: law-government.policy-making-and-analysis.regulatory-impact-assessment.cost-benefit-analysis-for-a-proposed-rule
name: cost-benefit-analysis-for-a-proposed-rule
category: law-government
field: policy-making-and-analysis
product: regulatory-impact-assessment
tags: [regulatory-impact-assessment, policy-making-and-analysis, ria, impact-assessment, cost-benefit-analysis, cba, benefit-cost-analysis, regulatory-analysis, omb-circular-a-4, executive-order-12866, green-book, better-regulation, sme-test, small-business-impact, regulatory-flexibility-act, paperwork-reduction-act, burden-estimate, standard-cost-model, administrative-burden, discount-rate, net-present-value, npv, value-of-statistical-life, sensitivity-analysis, distributional-analysis, familiarisation-costs, equivalent-annual-net-direct-cost-to-business, eancdb]
level: practitioner
status: draft
description: "Build a regulatory impact assessment for a proposed rule: baseline, options, monetised costs and benefits, burden estimates, discounting, sensitivity, distribution and small-business tests."
sources: ["US OMB Circular A-4 (Regulatory Analysis)", "HM Treasury, The Green Book", "UK Better Regulation Framework guidance", "OECD, Regulatory Impact Assessment best practice"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cost-benefit analysis for a proposed rule (regulatory impact assessment)

**Goal:** show decision-makers and the public, with transparent numbers, whether a
proposed regulation's benefits justify its costs compared with alternatives — robust
enough to survive review by an oversight body (OIRA in the US, the Regulatory Policy
Committee in the UK, the Regulatory Scrutiny Board in the EU) and, in some systems,
judicial review. Models: US federal (Executive Order 12866 and OMB Circular A-4) and UK
(Green Book / Better Regulation Framework). Thresholds, discount rates and required
tests differ by jurisdiction and are revised — check current guidance.

## 1. Frame the analysis
1. State the problem and why it needs government intervention (market failure, legal
   requirement).
2. Define the **baseline**: the world without the rule, including other rules already
   adopted and expected behaviour change.
3. Pick the **appraisal period** (often 10 years; longer for long-lived capital) and the
   **price year**.
4. List options: no action, the preferred rule, at least one more and one less stringent
   alternative, and a non-regulatory alternative where plausible.

## 2. Identify every impact before costing anything
| Group | Typical costs | Typical benefits |
|---|---|---|
| Regulated businesses | familiarisation, compliance capital, running costs, admin/reporting | reduced liability, level playing field |
| Consumers / households | price pass-through, reduced choice | safety, health, savings |
| Government | enforcement, IT, guidance | fewer harms to treat |
| Wider society | — | environmental and health gains |
Use an impact map: rule requirement → behaviour change → outcome → monetisable value.

## 3. Monetise costs
- **Standard cost model** for admin burden: number of affected entities x frequency x
  time per activity x loaded wage rate (wage plus overheads, often +20-30% — use your
  official uplift).
- **Familiarisation**: staff hours to read and understand the rule, per entity, one-off.
- **Compliance**: capital (equipment, systems) annualised or in the year incurred, plus
  ongoing operating costs.
- Source counts from business registers or census data; source unit costs from
  consultation responses, industry surveys or engineering estimates. Record every
  assumption in an assumptions log.
- US: information collections need a separate Paperwork Reduction Act burden estimate.

## 4. Monetise (or describe) benefits
- Health and safety: avoided deaths valued using the official value of a statistical
  life (or value of a prevented fatality), plus avoided injuries and illness.
- Environmental: official carbon values and damage costs.
- If a benefit cannot be credibly monetised, quantify it in natural units, then describe
  it qualitatively; do not leave it out. Consider **break-even analysis**: how large
  would the unquantified benefit need to be to justify the costs?

## 5. Discount and summarise
- Convert flows to present values using the official discount rate (the UK Green Book
  uses a declining schedule starting around 3.5%; US guidance was revised in 2023 —
  check the current Circular A-4 rate).
- Report NPV, benefit-cost ratio and, for the UK, the equivalent annual net direct cost to
  business (EANDCB) where required.
- Present a central estimate with low and high scenarios.

## 6. Sensitivity, distribution and special tests
- **Sensitivity:** vary the top 3-5 uncertain parameters; report switching values.
- **Distribution:** who bears costs and who gains (by income, region, firm size).
- **Small business:** US Regulatory Flexibility Act analysis where a rule has a
  significant impact on a substantial number of small entities; UK small and micro
  business assessment. Consider exemptions or phased compliance.
- Other screens your system requires: competition, trade, equality, rural, environment.

## 7. Use consultation to fix the numbers
Publish the draft assessment with the proposal and ask targeted questions ("How many
hours would form X take your firm?"). Update the final assessment with responses and
explain what changed.

## Gotchas
- Counting transfers (taxes, fees, price changes between parties) as net costs or benefits.
- Double-counting the same benefit via two routes.
- A baseline that assumes zero compliance with existing law, inflating benefits.
- False precision — showing costs to the pound or dollar on guessed inputs.

## Verify
- [ ] Baseline, appraisal period, price year and discount rate stated.
- [ ] At least three options appraised against the same baseline.
- [ ] Every assumption sourced in an assumptions log; non-monetised impacts described.
- [ ] Sensitivity, distributional and small-business analyses included.
- [ ] Consultation evidence reflected in the final version.
