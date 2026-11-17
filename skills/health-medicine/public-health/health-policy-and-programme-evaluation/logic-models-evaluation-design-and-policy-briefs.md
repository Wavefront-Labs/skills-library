---
id: health-medicine.public-health.health-policy-and-programme-evaluation.logic-models-evaluation-design-and-policy-briefs
name: logic-models-evaluation-design-and-policy-briefs
category: health-medicine
field: public-health
product: health-policy-and-programme-evaluation
tags: [public-health, health-policy-and-programme-evaluation, programme-evaluation, program-evaluation, policy-evaluation, logic-model, theory-of-change, process-evaluation, outcome-evaluation, impact-evaluation, re-aim, cdc-evaluation-framework, mrc-complex-interventions, realist-evaluation, difference-in-differences, interrupted-time-series, stepped-wedge, natural-experiment, counterfactual, cost-effectiveness, qaly, icer, policy-brief, evidence-brief, evidence-synthesis, stakeholder-engagement, pdsa, quality-improvement]
level: practitioner
status: gated
description: "Public-health evaluation and policy practice: logic models and theory of change, choosing evaluation designs (ITS, DiD, stepped-wedge), process and economic evaluation, and writing policy briefs."
sources: ["https://www.cdc.gov/evaluation/php/evaluation-framework/index.html", "https://www.nice.org.uk/news/articles/changes-to-nice-s-cost-effectiveness-thresholds-confirmed"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logic models, evaluation design and policy briefs

> General professional reference. Ethical approval and data-governance requirements
> for evaluation differ by jurisdiction and whether the work counts as research or
> service evaluation — check locally before collecting data.

**Goal:** show whether and how a programme or policy works, for whom and at what cost
— and put that evidence in front of decision-makers in a form they'll use.

## 1. Build the logic model first
- **Inputs → activities → outputs → short-term outcomes → intermediate → long-term
  impact**, with **assumptions** and **external factors**. A theory of change adds the
  causal "because" for each arrow.
- Agree it with stakeholders; it defines what to measure at each level and exposes
  untestable leaps ("leaflet → reduced mortality").

## 2. Frame the evaluation questions
- **Process**: was it delivered as intended (fidelity, dose, reach, adaptation)? Why
  did implementation succeed or fail?
- **Outcome/impact**: did it change outcomes compared with what would otherwise have
  happened (the counterfactual)?
- **Economic**: at what cost per outcome?
- Use frameworks to structure: the CDC Program Evaluation Framework six steps (assess the context, describe the program,
  focus the evaluation questions and design, gather credible evidence, generate and support
  conclusions, act on findings), **RE-AIM**
  (Reach, Effectiveness, Adoption, Implementation, Maintenance) (gated: unconfirmed, source is paywalled or blocked), MRC complex
  interventions framework (gated: unconfirmed, source is paywalled or blocked).

## 3. Choose a design that fits reality
| Situation | Design |
|---|---|
| Can randomise individuals/clusters | RCT / cluster RCT |
| Phased rollout anyway | **stepped-wedge** |
| Policy starts at a known date, long routine series | **interrupted time series** (enough points before and after to model seasonality and autocorrelation) |
| Some areas get it, others don't | **difference-in-differences** (check parallel pre-trends), synthetic control |
| Eligibility cut-off | regression discontinuity |
| Complex, context-dependent | realist evaluation ("what works for whom in what circumstances") |
| Little data, early stage | before–after with comparison, mixed methods — state weakness |
Plan evaluation **before** launch so baseline data exist.

## 4. Measurement
- Indicators at each logic-model level with source, frequency and owner.
- Mixed methods: qualitative interviews explain the numbers.
- Unintended consequences and equity impacts (who benefited, who didn't).

## 5. Economic evaluation (overview)
- Cost-effectiveness (cost per outcome), cost-utility (cost per QALY; ICER vs
  threshold; NICE's England threshold was £20,000–£30,000 per QALY and NICE has announced £25,000–£35,000 to apply once regulations allow — check current), cost-benefit, return on
  investment. Public-health benefits often accrue to other sectors and over long
  horizons — state perspective and discounting.

## 6. Policy briefs
- **2–4 pages**. Structure: key messages (3–5 bullets on page 1) → the problem (with
  local data) → policy options (each with evidence of effect, costs, equity,
  feasibility, risks) → implementation considerations → recommendation (if asked)
  → references.
- Write for a non-specialist: plain language, one chart per point, numbers in absolute
  terms (e.g. "prevents ~200 admissions a year").
- Grade evidence certainty (e.g. GRADE language) and be explicit about uncertainty and
  gaps.
- Time it to the decision window; brief in person where possible.

## 7. Using findings
Feed into programme improvement (PDSA cycles), decommissioning or scale-up; publish
negative findings too.

## Gotchas
- Measuring only outputs ("1,000 leaflets distributed").
- Declaring success from a pre–post change during a secular trend.
- Evaluations commissioned after launch with no baseline.
- Briefs that bury the recommendation on page 6.

## Verify
- [ ] Logic model agreed and indicators mapped to each level.
- [ ] Counterfactual design chosen and its threats named.
- [ ] Process, outcome and (where relevant) economic questions addressed.
- [ ] Equity and unintended effects examined.
- [ ] Policy brief has key messages on page 1 and options with evidence and costs.

## Checked

- Date checked: 2026-10-25. Jurisdiction: England and international; CDC framework is US public-health practice.
- Sources read: CDC Program Evaluation Framework page (dated 20 Aug 2024); NICE announcement on thresholds (read through search-result summaries because the NICE page returned 403).
- Confirmed: The CDC framework has six steps and five standards.
- Corrected or removed: The six step names were corrected to the current CDC wording (the old list used the 1999 labels); the NICE threshold now notes the announced rise to 25,000-35,000 pounds per QALY; the unsupported "8-12 points each side" ITS figure was removed.
- Gated: RE-AIM and MRC framework descriptions (not read). Confirm the date the new NICE thresholds actually took effect.

Method: documentation only; no commands were run.
