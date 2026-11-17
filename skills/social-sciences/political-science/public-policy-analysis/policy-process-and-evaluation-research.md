---
id: social-sciences.political-science.public-policy-analysis.policy-process-and-evaluation-research
name: policy-process-and-evaluation-research
category: social-sciences
field: political-science
product: public-policy-analysis
tags: [public-policy-analysis, policy-process, policy-studies, agenda-setting, kingdon, multiple-streams, policy-window, punctuated-equilibrium, comparative-agendas-project, cap, advocacy-coalition-framework, policy-diffusion, implementation-research, street-level-bureaucracy, lipsky, policy-evaluation, program-evaluation, difference-in-differences, synthetic-control, regression-discontinuity, theory-of-change, logic-model, process-evaluation, realist-evaluation]
level: practitioner
status: draft
description: "Researching policy: agenda-setting (Kingdon, punctuated equilibrium), Comparative Agendas Project coding, implementation studies and evaluation designs."
sources: ["Kingdon, Agendas, Alternatives, and Public Policies (1984/2011)", "Baumgartner & Jones, Agendas and Instability in American Politics", "Comparative Agendas Project master codebook", "Lipsky, Street-Level Bureaucracy (1980)", "Weible & Sabatier (eds), Theories of the Policy Process"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Policy process and evaluation research

**Goal:** study how issues get onto the agenda, how policies change, how they are
implemented on the ground, and whether they work — as a researcher, not an advocate.

## 1. Pick a lens that fits the question
- **Multiple Streams (Kingdon):** problems, policies and politics streams flow
  separately; change happens when a **policy entrepreneur** couples them in a **policy
  window**. Good for "why now?" case studies. Gotcha: easy to fit after the fact —
  specify in advance what would count as each stream.
- **Punctuated Equilibrium (Baumgartner & Jones):** long stasis, sudden large shifts
  as attention moves. Testable with budget or agenda data: change distributions are
  *leptokurtic* (many tiny changes, a few huge ones).
- **Advocacy Coalition Framework:** coalitions sharing core beliefs compete over years;
  policy learning mostly within coalitions.
- **Policy diffusion:** adoption spreads across states/countries via learning,
  competition, coercion or emulation; event-history models on adoption year.

## 2. Measuring agendas: Comparative Agendas Project (CAP)
CAP codes bills, laws, speeches, budgets, hearings and media into ~20 major topics and
~200 subtopics with a shared master codebook across many countries. Use their datasets,
or code your own corpus with their scheme so results are comparable. Train coders on
the codebook, double-code a subsample, report agreement. Supervised ML classifiers
trained on CAP-coded text can scale coding — validate on held-out human codes.

## 3. Implementation research
Policies change in delivery. Methods: interviews and observation with frontline
staff (**street-level bureaucrats** exercise discretion under resource pressure),
document analysis of guidance vs practice, and process tracing of top-down vs
bottom-up adaptations. Map the delivery chain explicitly — who interprets what, at
which level.

## 4. Evaluation research
- Start with a **theory of change / logic model**: inputs → activities → outputs →
  outcomes → impacts, plus assumptions.
- **Impact designs:** randomised trials where feasible; otherwise
  difference-in-differences (check pre-trends; with staggered adoption use modern
  estimators such as Callaway–Sant'Anna rather than naive two-way fixed effects),
  synthetic control (one treated unit, good donor pool), regression discontinuity
  (eligibility cutoffs), interrupted time series.
- **Process evaluation:** was it delivered as designed (fidelity, dose, reach)?
  A null effect with poor implementation is a different finding from a null effect
  of a well-delivered programme.
- **Realist evaluation:** what works for whom, in what context, through which
  mechanism (CMO configurations).

## 5. Gotchas
- Policy adoption is endogenous — places adopt because of the problem's trajectory.
- Outcome data often come from the implementing agency; check incentives to game it.
- Commissioned evaluations face pressure; agree publication rights up front.

*Uncertainty:* CAP topic counts are approximate and the codebook is periodically
revised — check the current master codebook.

## Verify
- [ ] Theoretical lens stated with observable implications specified in advance.
- [ ] Agenda coding follows a published codebook with reported reliability.
- [ ] Implementation chain mapped from policy text to frontline practice.
- [ ] Evaluation design identifies its counterfactual and tests key assumptions (e.g. pre-trends).
- [ ] Process evaluation accompanies any impact claim.
