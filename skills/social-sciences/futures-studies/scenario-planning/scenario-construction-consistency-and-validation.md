---
id: social-sciences.futures-studies.scenario-planning.scenario-construction-consistency-and-validation
name: scenario-construction-consistency-and-validation
category: social-sciences
field: futures-studies
product: scenario-planning
tags: [scenario-planning, scenarios, scenario-building, futures-studies, foresight, intuitive-logics, shell-method, 2x2-matrix, scenario-matrix, driving-forces, steep, steepled, pestle, critical-uncertainties, predetermined-elements, morphological-analysis, zwicky-box, cross-impact-balance, cib, scenario-wizard, consistency-analysis, scenario-narratives, plausibility, scenario-validation, wildcards, shared-socioeconomic-pathways, ssp, participatory-scenarios, scenario-axes]
level: practitioner
status: draft
description: "Build research-grade scenarios: driving-forces analysis, choosing between 2x2 intuitive logics and morphological/CIB methods, consistency checks, narrative writing, and validation criteria."
sources: ["van der Heijden, Scenarios: The Art of Strategic Conversation (2nd ed., Wiley 2005)", "Bradfield et al. (2005), Futures 37(8)", "Weimer-Jehle (2006), Technological Forecasting and Social Change 73(4)", "Ritchey, Wicked Problems – Social Messes (Springer 2011)", "O'Neill et al. (2014), Climatic Change 122(3) on SSPs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scenario construction for futures research — rigour beyond the 2×2

**Goal:** a set of alternative futures that are internally consistent, jointly cover the
important uncertainty, and whose construction a reviewer could retrace.

The workshop-oriented strategy version (2×2, wind tunnelling, signposts) is in
business-finance.strategy-and-foresight.scenario-planning.two-axis-scenarios-wind-tunnelling-and-signposts.
This skill adds the research methods side: method choice, consistency analysis, documentation.

## 1. Frame
- **Focal question** and **horizon** (e.g. "urban mobility in region X, 2045"). Horizon must
  exceed the planning cycle so structural change is possible.
- **Scope**: geographic, sectoral, what is held fixed.
- **Purpose**: exploratory (what could happen) vs normative (how to reach a goal → see
  backcasting in social-sciences.futures-studies.foresight-methodology.causal-layered-analysis-backcasting-and-method-selection).

## 2. Driving forces
- Gather drivers with a STEEP/STEEPLE scan (social, technological, economic, environmental,
  political, legal, ethical), horizon-scanning outputs
  (social-sciences.futures-studies.horizon-scanning.scanning-protocol-signal-coding-and-clustering),
  interviews and literature. Expect 30–80 raw items.
- Cluster to 10–20 **key factors**; separate **predetermined elements** (demographic ageing
  already in the age structure) from **critical uncertainties** (high impact, high uncertainty).

## 3. Choose the construction method
| Method | When | Output |
|---|---|---|
| **Intuitive logics / 2×2** | Workshop-driven, communication matters, two dominant uncertainties | 4 scenarios |
| **Morphological analysis** (Zwicky box) | Many factors with discrete states; explore the full space | Large configuration space, then pruned |
| **Cross-impact balance (CIB)** | Need explicit, auditable consistency among 6–15 factors | Ranked set of consistent configurations |
| **Model-linked** (e.g. SSP-style narratives + quantitative models) | Quantified outcomes needed | Narratives with numbers |
A 2×2 forces two axes to be independent; check that they are, or the corners include
implausible combinations.

## 4. Consistency analysis
- **Morphological:** for each pair of factor states, judge compatible / incompatible;
  eliminate configurations containing incompatible pairs. Field anomaly relaxation and
  dedicated software do this at scale.
- **CIB:** for each factor state, rate the influence of every other factor's state (−3 to +3).
  A configuration is consistent if each factor's chosen state receives the highest impact
  balance given the others. ScenarioWizard (free software by Weimer-Jehle) computes this.
  Document the judgement matrix — it is the audit trail.
- Pick a final set (3–5) that spans the uncertainty space, not three variants of "business as
  usual". Avoid a "good/bad/middle" set: people pick the middle.

## 5. Narratives
- Each scenario: a memorable name, the logic (what drives it), a timeline of events from now
  to the horizon (how we got there), key indicators, and what it means for the focal question.
- 1–3 pages each; consistent structure across scenarios for comparison.
- Avoid assigning probabilities in exploratory sets unless the method supports it.

## 6. Validation criteria
Commonly used: **plausibility** (could happen given current knowledge), **internal
consistency** (CIB/morphological check), **differentiation** (meaningfully distinct),
**relevance** to the focal question, **challenge** (surprises the users), and
**transparency** (assumptions traceable). Test with external reviewers and users; record
changes made in response.

## Gotchas
- Choosing axes because they are interesting rather than most uncertain and impactful.
- Scenarios that are just trends extrapolated with different adjectives.
- Anchoring on the facilitator's preferred future.
- Ignoring wildcards: add a stress-test section for low-probability, high-impact events.

## Verify
- [ ] Focal question, horizon and scope documented.
- [ ] Driver list traceable to sources; predetermined vs uncertain separated.
- [ ] Construction method justified; consistency judgements recorded.
- [ ] 3–5 scenarios spanning the space, each with timeline and indicators.
- [ ] Validation criteria applied and reviewer feedback logged.

*Draft: CIB scoring ranges and software details recalled from the method papers; confirm before use.*
