---
id: business-finance.project-and-program-management.portfolio-pmo-governance.portfolio-intake-and-stage-gates
name: portfolio-intake-and-stage-gates
category: business-finance
field: project-and-program-management
product: portfolio-pmo-governance
tags: [project-and-program-management, portfolio-pmo-governance, portfolio-management, ppm, pmo, project-intake, prioritisation, prioritization, weighted-scoring, stage-gate, phase-gate, business-case, capacity-planning, resource-allocation, portfolio-review, project-governance, wip-limits, investment-committee, project-register]
level: practitioner
status: draft
description: "Govern a project portfolio: single intake, weighted scoring and ranking, fitting to scarce-skill capacity, stage gates with real stop decisions, and quarterly re-ranking."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Portfolio intake, prioritisation and stage gates

**Goal:** decide which projects the organisation starts, continues or stops, so
limited money and people go to the work that matters most — and nothing gets
funded just because it was proposed loudly.

## 1. One front door (intake)
- All proposed projects above a threshold (cost, effort, risk) enter through a single
  **intake form**: problem/opportunity, strategic objective served, rough cost and
  effort (order of magnitude), benefits, key risks, dependencies, sponsor, urgency
  driver (regulatory date, contract expiry).
- Below threshold → handled as business-as-usual within team budgets.
- PMO checks completeness, not merit; incomplete ideas go back to the sponsor.

## 2. Score and rank
Use a **weighted scoring model** agreed by the executive in advance, e.g.:
| Criterion | Weight |
|---|---|
| Strategic alignment | 30% |
| Financial value (NPV/payback band) | 25% |
| Risk reduction / compliance | 20% |
| Delivery risk (inverse) | 15% |
| Urgency | 10% |
- **Mandatory** items (regulatory, safety) skip ranking but still consume capacity — book
  them first.
- Calibrate scoring with descriptors (what is a 1, 3, 5?) and score as a panel.
- Rank by score ÷ cost (or effort) to see value per unit of scarce resource.

## 3. Fit to capacity — the constraint is usually people
- Compare the ranked list against **capacity by key skill** (e.g. data engineers,
  business analysts), not just budget. Draw the cut line where the scarce skill runs
  out.
- **Limit work in progress** at portfolio level: fewer projects in parallel finish
  sooner. Starting everything at once stretches every project.
- Publish the result: approved, queued (with position), rejected (with reason).

## 4. Stage gates
Typical gates:
| Gate | Decision | Evidence |
|---|---|---|
| G0 Idea | Worth investigating? | Intake form |
| G1 Business case | Fund planning/design? | Options appraisal, outline case |
| G2 Investment | Fund delivery? | Full business case, plan, baseline, risks |
| G3 Go-live | Ready to deploy? | Test results, readiness, support |
| G4 Closure | Benefits handed over? | Lessons, benefits plan |
- Gate outcomes: **go / go with conditions / hold / recycle / stop**. A gate that
  never stops anything isn't a gate.
- Proportionality: small projects get a lighter path (fewer gates, shorter templates).

## 5. Portfolio reviews (quarterly)
- Re-rank including in-flight projects; compare forecast cost/benefit with the case.
- **Kill or re-scope** projects whose case no longer holds — sunk cost is irrelevant.
- Rebalance resources; release capacity for the next queued items.
- Portfolio dashboard: spend vs budget, RAG by project, benefits forecast, capacity
  utilisation, strategic coverage (how much spend serves each objective).

## 6. PMO standards (minimum viable)
Templates (intake, business case, status report), a RAG definition everybody uses,
a central project register, and a risk/issue escalation route. Keep standards
light; heavy PMO process pushes work outside the system.

## Gotchas
- **Pet projects** bypassing intake via senior sponsors — the whole system's credibility
  depends on no exceptions.
- Scoring gamed by inflated benefits; check past cases' realised vs claimed benefits
  to calibrate sponsors.
- Approving by budget only while key people are 200% allocated.
- Gates as paperwork reviews rather than real investment decisions.

## Verify
- [ ] Every in-scope project came through intake and has a sponsor.
- [ ] Scoring criteria and weights approved before ranking.
- [ ] The approved list fits capacity of the scarcest skills.
- [ ] Each gate records a decision, including stops and holds.
- [ ] Quarterly review re-ranked in-flight work and explicitly considered stopping or re-scoping each item.
