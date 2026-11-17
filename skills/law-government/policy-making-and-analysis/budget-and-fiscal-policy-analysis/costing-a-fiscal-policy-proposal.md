---
id: law-government.policy-making-and-analysis.budget-and-fiscal-policy-analysis.costing-a-fiscal-policy-proposal
name: costing-a-fiscal-policy-proposal
category: law-government
field: policy-making-and-analysis
product: budget-and-fiscal-policy-analysis
tags: [budget-and-fiscal-policy-analysis, policy-making-and-analysis, fiscal-costing, policy-costing, budget-scoring, cbo-score, scoring, static-costing, behavioural-response, dynamic-scoring, revenue-estimate, tax-expenditure, spending-review, budget-analysis, baseline, scorecard, ten-year-window, budget-window, paygo, fiscal-rules, obr-certification, appropriations, mandatory-spending, discretionary-spending, capital-vs-current, distributional-analysis, microsimulation, revenue-options, offsets]
level: practitioner
status: draft
description: "Cost a tax or spending proposal: baseline, static estimate, behavioural responses, phasing over a budget window, offsets and fiscal rules, distributional tables and uncertainty."
sources: ["Congressional Budget Office and Joint Committee on Taxation, published scoring methodology", "UK Office for Budget Responsibility, policy costings documents", "IMF, Fiscal Transparency Code"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Costing a fiscal policy proposal

**Goal:** produce a defensible estimate of what a tax or spending proposal will cost
(or raise) year by year, how certain that is, who is affected, and how it fits fiscal
rules — the way an official scorekeeper or a serious opposition or think-tank costing
unit would. Models: US federal (CBO/JCT scoring, a 10-year budget window) and UK (HM
Treasury costings certified by the Office for Budget Responsibility, usually over a
five-year forecast). Budget rules, windows and scorekeeping conventions differ by
jurisdiction and change — check the current rulebook.

## 1. Specify the policy precisely
Costings fail on vague specs. Pin down: the exact rate/threshold/benefit amount,
eligibility, start date, phasing, indexation (inflation-linked or frozen), interaction
with existing taxes and benefits, administration method and any sunset.

## 2. Establish the baseline
Use the official current-law (or current-policy) forecast for the tax base or caseload
over the window: e.g. number of claimants, aggregate taxable income, unit costs.
Document which forecast vintage you used; costings drift when the baseline updates.

## 3. Static estimate
- Spending: **caseload x unit cost x take-up**, by year, plus administration costs.
- Tax: **tax base x rate change**, using microsimulation on survey or administrative
  tax data where available, otherwise aggregate elasticities.
- Apply timing: tax receipts often lag the liability year (payments on account, annual
  returns); spending ramps up as systems open.

## 4. Behavioural responses
Adjust for how people and firms will react — avoidance, income shifting,
forestalling (bringing transactions forward before a tax rise), changes in take-up,
cross-border effects. Use published elasticities and say which. Conventional US scoring
includes many micro behavioural responses but not, by default, macroeconomic feedback
("dynamic scoring" is reported separately for major bills); UK costings include
behavioural effects and the OBR may adjust for wider economic effects. Never let a
behavioural assumption silently do most of the work — show static and post-behaviour
figures side by side.

## 5. Present the costing table
| Year | 1 | 2 | 3 | 4 | 5 | ... | Total |
|---|---|---|---|---|---|---|---|
| Static | | | | | | | |
| Behavioural adjustment | | | | | | | |
| Admin costs | | | | | | | |
| **Net Exchequer / deficit effect** | | | | | | | |
Use the scorekeeper's sign convention (state it: "+ = increase in deficit" or "+ = gain
to Exchequer"). Note one-off vs recurring and whether figures are nominal.

## 6. Fiscal rules and offsets
- Check against the relevant rules: pay-as-you-go requirements, deficit or debt targets,
  spending caps, balanced-budget rules (common for US states and many local governments).
- Identify offsets (savings or revenues) and cost them with the same rigour — offsets are
  where weak costings hide.
- Separate capital from current/resource spending where the fiscal framework does.

## 7. Distribution and uncertainty
- Distributional table: average change in household income by income decile (or quintile),
  plus counts of winners and losers.
- Uncertainty rating per component (data quality, behavioural uncertainty, modelling
  complexity) — the OBR publishes such ratings; adopt the idea.
- Sensitivity: show the total under low and high behavioural assumptions.

## 8. Reviewing someone else's costing
Check: is the spec clear? Is the baseline current? Is take-up realistic (new benefits
rarely reach 100%)? Are behavioural effects plausible and symmetric? Are admin and IT
costs included? Do the offsets actually materialise within the window? Is there
back-loading beyond the window (a common gaming technique)?

## Gotchas
- Counting the same revenue twice to fund two different pledges.
- Using a full-year figure for the first year of a mid-year start.
- Ignoring interactions (e.g. a new allowance reduces means-tested benefit spending).
- Treating a one-off asset sale as a recurring revenue.

## Verify
- [ ] Policy specification written and agreed.
- [ ] Baseline vintage and data sources documented.
- [ ] Static and behavioural estimates shown separately, year by year, with sign convention.
- [ ] Offsets costed; fiscal-rule compliance checked; effects beyond the window flagged.
- [ ] Distributional analysis and uncertainty/sensitivity ranges included.
