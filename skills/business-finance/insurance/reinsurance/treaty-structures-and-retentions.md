---
id: business-finance.insurance.reinsurance.treaty-structures-and-retentions
name: treaty-structures-and-retentions
category: business-finance
field: insurance
product: reinsurance
tags: [insurance, reinsurance, treaty, treaty-reinsurance, facultative, quota-share, surplus-treaty, excess-of-loss, xol, cat-xol, catastrophe-reinsurance, stop-loss, retention, layers, reinstatements, rate-on-line, hours-clause, ceding-commission, programme-design, placement, losses-occurring, risks-attaching]
level: advanced
status: draft
description: "Design a reinsurance programme: quota share vs surplus vs per-risk and cat excess of loss, setting retentions from capital tolerance, layering and tracing losses through it."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing treaty structures and setting retentions

**Goal:** design a reinsurance programme that keeps the insurer's net results and
capital within appetite — protecting against single large losses and catastrophes —
at an acceptable cost.

*Draft: conceptual programme-design practice. Actual retentions come from the
insurer's capital model, risk appetite and regulator; placement is done with brokers.*

## 1. Know the structures
**Proportional** — reinsurer shares premium and losses in a fixed proportion.
- **Quota share:** cede a fixed % of every policy. 40% QS, $1m loss → reinsurer pays
  $400k. Provides capital relief and ceding commission; simple; cedes good business too.
- **Surplus:** insurer keeps a fixed **line** (retention) per risk; cedes the surplus
  up to a number of lines. Retention $1m, risk sum insured $4m → retain 25%, cede 75%
  of premium and every loss on that risk. Balances a book of uneven risk sizes.

**Non-proportional (excess of loss, XoL)** — reinsurer pays losses above a
retention up to a limit; priced separately (rate on line).
- **Per-risk XoL:** "$4m xs $1m" — a $3m loss on one risk → recovery $2m.
- **Catastrophe XoL:** per event, across many risks; protects against nat-cat
  accumulation. Usually structured in layers.
- **Aggregate / stop-loss:** caps the annual total loss or loss ratio.
- Key terms: **reinstatements** (restoring the limit after a loss, often for additional
  premium), **hours clause** (defining an "event" window for cat), **annual aggregate
  deductible**.

**Facultative** — individually negotiated for a single risk outside treaty capacity
or appetite.

## 2. Setting the retention
Consider together:
- **Capital and earnings tolerance:** the largest net loss the insurer will accept
  from one risk or event, often expressed as a % of capital or of annual profit.
- **Return period:** cat programmes are commonly bought to a modelled return period
  (e.g. 1-in-200 for solvency-driven buyers). *(Market convention; the right figure
  is the insurer's.)*
- **Cost vs volatility:** lower retentions buy more stability at a higher price;
  frequency layers are expensive because reinsurers price in expected losses plus margin.
- **Portfolio size:** a small insurer's retention is a small fraction of a large one's.

## 3. Build the programme
1. Exposure data: risk profile (bands of sums insured), cat exposure by zone,
   large-loss history.
2. Model gross losses (per risk, per event, annual).
3. Test alternative structures: net result distribution, capital requirement, cost.
4. Order of application matters: e.g. surplus → then per-risk XoL on the retained
   line → then cat XoL protecting the net retention of both. Write out a flow of a
   sample loss through the programme.
5. Check **counterparty security**: reinsurer ratings, panel diversification, collateral.

## 4. Placement and administration
Broker markets the programme; lead reinsurer sets terms, followers take shares.
After inception: bordereaux, accounts, claims notifications per treaty conditions
(late notice can lose recoveries), and recoveries tracking.

## Gotchas
- **Gaps between layers or vertical exhaustion** in a bad cat year — check
  reinstatements and aggregate exposure.
- **Basis mismatch:** treaty on losses-occurring basis vs policies written on a
  risks-attaching basis can leave periods uncovered at renewal.
- **Definition of event/occurrence** fights after cats.
- Underlying policy wordings broader than what the treaty follows.

## Verify
- [ ] Each treaty's type, retention, limit and order of application written out.
- [ ] A sample large loss and a cat event traced through the programme with net retained amounts.
- [ ] Retentions tie to stated capital/earnings tolerances.
- [ ] Reinstatements and aggregate exhaustion tested for a multi-event year.
- [ ] Reinsurer security and notification conditions reviewed.
