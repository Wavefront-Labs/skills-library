---
id: business-finance.accounting.management-accounting.standard-costing-and-variance-analysis
name: standard-costing-and-variance-analysis
category: business-finance
field: accounting
product: management-accounting
tags: [management-accounting, cost-accounting, standard-costing, variance-analysis, price-variance, usage-variance, efficiency-variance, volume-variance, mix-variance, flexed-budget, flexible-budget, overhead-absorption, contribution-margin, budget-vs-actual, cima, cma, activity-based-costing, abc]
level: practitioner
status: draft
description: "Set standard costs, flex the budget to actual volume, split variances into price, usage, efficiency and volume, and turn the numbers into actions managers can take."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Standard costing and variance analysis

**Goal:** explain *why* actual profit differs from budget, in terms a manager can act
on ("we paid 6% more per kg of resin" rather than "materials over by 40k").

## 1. Build the standard cost card
Per unit of output: standard **quantity** × standard **price** for each input.
```
Material A   2.0 kg  × 5.00/kg   = 10.00
Labour       0.5 h   × 24.00/h   = 12.00
Variable OH  0.5 h   × 6.00/h    =  3.00
Fixed OH     0.5 h   × 10.00/h   =  5.00   (absorption costing only)
Standard cost per unit            = 30.00
```
Set standards as *attainable*, not ideal: ideal standards guarantee adverse variances
that everyone learns to ignore. Review them at least annually and after big
price/process changes.

## 2. Flex the budget first
Compare actual results with the budget **restated for actual volume**. The gap between
original and flexed budget is the *volume* effect; everything else is performance.
Skipping this step is the most common error: making 20% more units "overspends"
materials by 20% without anyone doing anything wrong.

## 3. The core variances (F = favourable, A = adverse)
Let AQ = actual quantity, AP = actual price, SQ = standard quantity for actual output,
SP = standard price.
- **Material price** = (SP − AP) × AQ purchased (or used — pick one and be consistent).
- **Material usage** = (SQ − AQ) × SP.
- **Labour rate** = (SR − AR) × actual hours paid.
- **Labour efficiency** = (standard hours for actual output − actual hours worked) × SR.
- **Idle time** = hours paid but not worked × SR (always adverse; show separately).
- **Variable overhead** spend and efficiency mirror labour.
- **Fixed overhead** expenditure = budget − actual; under absorption costing also a
  volume variance = (actual output − budgeted output) × fixed OH per unit.
- **Sales price** = (actual price − standard price) × actual units sold.
- **Sales volume** = (actual − budgeted units) × standard *contribution* (marginal
  costing) or standard *profit* (absorption).
With several materials or products, split usage/volume into **mix** and **yield/
quantity** variances.

## 4. Reconcile and report
Budgeted profit + all variances = actual profit. If it doesn't reconcile to the cent,
there's an arithmetic or classification error — fix it before writing commentary.
Report as an operating statement: budgeted profit → sales variances → cost variances
→ actual profit, then a short commentary per material variance with **cause, owner,
action**.

## Gotchas
- **Variances interact.** Cheap, poor-quality material gives a favourable price
  variance and an adverse usage/efficiency variance. Read them together; assign the
  combined effect to the decision-maker (often purchasing, not production).
- **Controllability:** charge managers only with what they control; an
  exchange-rate-driven price variance isn't the buyer's fault.
- **Materiality:** set a threshold (e.g. >5% and >a fixed amount) so commentary goes
  where it matters.
- **Overhead absorption distorts product cost** where overhead is driven by setups or
  complexity rather than labour hours; that's when activity-based costing earns its
  cost. ABC design itself is out of scope here.
- Exact naming conventions differ between CIMA/ACCA (UK) and CMA/IMA (US) syllabi;
  formulas above follow the common textbook forms.

## Verify
- [ ] Budget flexed to actual volume before any cost variance is computed.
- [ ] Budgeted profit + variances reconciles exactly to actual profit.
- [ ] Each material variance has cause, owner and action, not just a number.
- [ ] Interacting variances (price vs usage, rate vs efficiency) are discussed together.
- [ ] Standards have a review date and source.
