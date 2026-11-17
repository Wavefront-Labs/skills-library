---
id: business-finance.risk-management.enterprise-risk-management.risk-register-and-appetite-statement
name: risk-register-and-appetite-statement
category: business-finance
field: risk-management
product: enterprise-risk-management
tags: [enterprise-risk-management, risk-management, erm, risk-register, risk-appetite, risk-appetite-statement, risk-tolerance, heat-map, risk-matrix, likelihood-impact, inherent-risk, residual-risk, target-risk, risk-owner, key-risk-indicators, kri, coso-erm, iso-31000, three-lines-model, board-risk-reporting, emerging-risks, risk-taxonomy, bow-tie]
level: practitioner
status: draft
description: "Build an ERM risk register the board can use: well-formed risk statements, inherent and residual scoring, owners and actions, and an appetite statement with measurable tolerances and KRIs."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Risk register and appetite statement — make ERM drive decisions

**Goal:** a concise register of the organisation's principal risks, scored consistently,
each owned and linked to a measurable appetite, so leadership can see which risks are
outside tolerance and what is being done. Frameworks: ISO 31000 and COSO ERM (2017) —
both principle-based; neither prescribes the scales below.

## 1. Write risk statements properly
Use **cause → event → consequence**:
> "Because we rely on a single cloud region (cause), a regional outage (event) could stop
> customer ordering for more than 24 hours, losing ~€2M revenue and breaching SLAs (consequence)."
Not "IT risk" or "cyber". A vague risk cannot be scored or owned. Keep the top-level register
to the principal risks (often 10–20); detail lives in departmental registers.

## 2. Score on defined scales
Define 1–5 scales in writing:
- **Impact** — with financial bands sized to the organisation (e.g. 1 = < €100k ... 5 = > €10M
  or > x% of EBITDA), plus non-financial columns: reputation, regulatory, safety, customers.
  Score on the highest column hit.
- **Likelihood** — over a stated horizon (e.g. 3 years): 1 = rare (< 5%) ... 5 = almost certain (> 80%).
Score **inherent** (before controls), **residual** (with current controls as they actually
operate) and **target** (after planned actions). The heat map plots residual.

## 3. Owners, controls, actions
Each risk gets one **risk owner** — a senior person with authority over the response, not
the risk team. List key controls (and whether they're tested — see business-finance.risk-management.operational-risk-management),
and actions with owners and dates to move residual toward target. Response options: avoid,
reduce, transfer (insurance, contracts), accept.

## 4. Risk appetite statement
The board states how much risk it will take in pursuit of objectives, per category:
- **Qualitative stance** per category — e.g. "averse" to safety and regulatory breaches,
  "open" to product innovation risk.
- **Quantitative tolerances** that make it testable: "no more than 2 hours of unplanned
  downtime of core platforms per quarter"; "single customer < 15% of revenue"; "zero
  tolerance for sanctions breaches"; "liquidity headroom ≥ 3 months of operating costs".
- **KRIs** with thresholds (green/amber/red) tied to each tolerance, reported monthly or
  quarterly. Amber triggers management action; red triggers escalation to the board/risk committee.
An appetite statement without numbers is a values statement, not a control.

## 5. Report and review
- Quarterly to the executive and the board/risk committee: heat map with movement arrows,
  risks outside appetite, KRI breaches, overdue actions, new and **emerging risks**.
- Annual refresh of appetite with strategy planning; risks should be discussed when
  decisions are made (new market, acquisition), not only at quarter end.
- Clarify roles via the **three lines** model: business owns risk (1st line), risk/compliance
  oversees and challenges (2nd), internal audit assures (3rd).

## Gotchas
- Scoring residual risk assuming controls work perfectly when they haven't been tested.
- Heat-map "colour inflation": everything amber, so nothing stands out.
- Multiplying likelihood × impact treats a 5×1 and 1×5 as equal — display both dimensions
  and give extra weight to severe-impact risks.
- Registers that never change quarter to quarter signal a compliance exercise.
- Mixing causes and risks ("staff turnover" is often a cause of several risks).
- Missing interdependencies: one event (e.g. a cyber attack) can hit several risks at once.

## Verify
- [ ] Every principal risk is written as cause–event–consequence with a single named owner.
- [ ] Impact and likelihood scales are written down, with a time horizon.
- [ ] Inherent, residual and target scores recorded; residual reflects tested controls.
- [ ] Each appetite category has at least one measurable tolerance and KRI with thresholds.
- [ ] Board report shows risks outside appetite and the actions/owners/dates for each.

Related: business-finance.risk-management.business-continuity-planning; business-finance.compliance.compliance-program-management.
