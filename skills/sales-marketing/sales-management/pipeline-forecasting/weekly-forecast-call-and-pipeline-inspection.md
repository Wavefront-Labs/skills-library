---
id: sales-marketing.sales-management.pipeline-forecasting.weekly-forecast-call-and-pipeline-inspection
name: weekly-forecast-call-and-pipeline-inspection
category: sales-marketing
field: sales-management
product: pipeline-forecasting
tags: [pipeline-forecasting, sales-forecast, forecasting, pipeline-review, pipeline-inspection, commit, best-case, upside, weighted-pipeline, stage-probability, win-rate, sales-cycle, slipped-deals, pipeline-coverage, forecast-accuracy, crm, salesforce, hubspot, sales-management, revops, deal-review]
level: practitioner
status: draft
description: "Call the sales number weekly: inspect pipeline hygiene, roll up commit and best case, sanity-check against weighted and coverage math, and measure forecast accuracy each period."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Weekly forecast call and pipeline inspection

**Goal:** a forecast that lands within a few percent of actual, made from deals you've
inspected, not hopes rolled up from reps.

## 1. Define the categories (write them down)
- **Commit:** the rep would bet their bonus on it closing this period. Buyer has confirmed
  timing, budget is approved, the paperwork path is known.
- **Best case:** could close this period if things go right; a named risk exists.
- **Pipeline:** real opportunity, not this period or not yet qualified.
- **Omitted/closed lost:** out.
Commit is a judgment call by the rep *and* manager, separate from CRM stage.

## 2. Pipeline hygiene check (before the call)
Pull a report of open deals closing this period and next. Flag:
- **Close date in the past** — every one must be updated or closed lost.
- **No activity in 14+ days** (adjust to your cycle).
- **Close date pushed 2+ times** (slip count).
- **Stage doesn't match evidence**: e.g. "Proposal" with no proposal sent.
- **Missing amount, next step or decision-maker contact.**
Salesforce: a report on Opportunities with `Close Date < TODAY` and `Stage != Closed`;
HubSpot: a deals view filtered on close date and last activity date. Reps fix flags before the call.

## 3. The 1:1 deal inspection (per rep, 20–30 min)
For each commit and best-case deal, ask:
1. "What's the next step, and is it on the buyer's calendar?"
2. "Who signs, and have we spoken to them?"
3. "What does their buying process look like from here — legal, procurement, security review?"
4. "What would make this slip?"
Dates that depend on steps nobody has scheduled go to best case.

## 4. Roll up and sanity-check
```
call            = commit + (a judged share of best case)
weighted        = Σ (amount × stage probability)        # cross-check, not the call
coverage        = open pipeline this period / remaining target
historic_conv   = closed won ÷ pipeline at same point in past periods
```
- If your call is far above weighted and historic conversion, you're optimistic; explain why.
- Coverage of roughly 3× is a common rule of thumb for new business; the right number
  is 1 ÷ your actual win rate from that point — calculate yours.
- Calibrate stage probabilities from your own history (wins ÷ deals that reached the stage),
  not defaults.

## 5. Report and close the loop
- Submit commit / best case / call by a fixed time each week; note movement vs last week
  and the top 3 deals at risk.
- At period end: **forecast accuracy = 1 − |actual − call| / actual**, tracked by week of
  quarter. Run a post-mortem on big misses: which deals slipped and why.

## Gotchas
- **Sandbagging** (reps under-calling) and **happy ears** (over-calling) both hurt;
  compare each rep's history of call vs actual.
- Big single deals distort everything — forecast them separately with a probability.
- Changing stage definitions mid-quarter breaks comparisons.
- CRM field names and reporting menus differ by edition; examples above are generic.

## Verify
- [ ] Zero open deals with past close dates before the call.
- [ ] Every commit deal has a buyer-confirmed next step and known signer.
- [ ] Call compared against weighted pipeline and historical conversion.
- [ ] Stage probabilities based on your own win data.
- [ ] Forecast accuracy recorded each period with a slip post-mortem.
