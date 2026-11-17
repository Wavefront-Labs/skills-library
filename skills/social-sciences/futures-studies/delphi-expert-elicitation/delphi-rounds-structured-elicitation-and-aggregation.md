---
id: social-sciences.futures-studies.delphi-expert-elicitation.delphi-rounds-structured-elicitation-and-aggregation
name: delphi-rounds-structured-elicitation-and-aggregation
category: social-sciences
field: futures-studies
product: delphi-expert-elicitation
tags: [delphi-expert-elicitation, delphi-method, delphi-study, policy-delphi, real-time-delphi, expert-elicitation, structured-expert-judgement, expert-panel, consensus, interquartile-range, stability, idea-protocol, shelf, sheffield-elicitation-framework, cookes-classical-model, seed-questions, calibration, performance-weighting, probability-elicitation, quantiles, anchoring, overconfidence, aggregation, linear-opinion-pool, nominal-group-technique, credes]
level: practitioner
status: draft
description: "Run a Delphi study or structured expert elicitation: panel selection, round design and feedback, consensus and stability criteria, elicitation protocols (IDEA, SHELF, Cooke) and aggregation."
sources: ["Linstone & Turoff (eds.), The Delphi Method: Techniques and Applications (1975)", "Jünger et al. (2017), Palliative Medicine 31(8) — CREDES reporting guidance", "Hemming et al. (2018), Methods in Ecology and Evolution 9(1) — IDEA protocol", "Oakley & O'Hagan, SHELF (Sheffield Elicitation Framework)", "Cooke, Experts in Uncertainty (Oxford 1991)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Delphi and expert elicitation — rounds, protocols, aggregation

**Goal:** turn expert judgement about uncertain futures into documented estimates —
consensus statements or probability distributions — with known biases reduced and
the process reportable.

## 1. Choose the format
| Need | Method |
|---|---|
| Agreement on statements/priorities, anonymous, distributed experts | **Classic Delphi** (2–4 rounds) |
| Map the range of views rather than force consensus | **Policy Delphi** |
| Fast, continuous updating online | **Real-time Delphi** |
| Quantities/probabilities for decisions or models | **Structured elicitation**: IDEA, SHELF, Cooke's classical model |
Delphi's defining features: anonymity, iteration, controlled feedback, statistical group
response.

## 2. Panel
- Define expertise criteria in advance (publications, roles, lived experience) and
  diversity (disciplines, sectors, regions, viewpoints). Record why each was invited.
- Size: often 10–30 per panel/stakeholder group; more does not add much accuracy but helps
  absorb dropout (expect 20–30% attrition per round — plan for it).
- Disclose that experts' identities are known to the facilitator but not to each other.

## 3. Delphi rounds
1. **Round 1** — open questions or a seed list from literature/scanning; experts add items.
   Content-analyse responses into clear statements (one idea each).
2. **Round 2** — rate each statement (e.g. 1–9 Likert on agreement/importance/likelihood, or
   year of occurrence) with optional reasons.
3. **Round 3+** — feed back the group distribution (median, IQR, histogram), the expert's own
   previous answer, and anonymised reasons; ask for re-rating with reasons for outlying answers.
- **Pre-define stopping and consensus rules**: e.g. consensus if ≥70–80% rate 7–9 or IQR ≤ 1 on a
  9-point scale; stop when consensus is reached or responses are **stable** between rounds
  (little change in distribution), or after a set number of rounds. The specific thresholds vary
  widely in the literature — choose and justify yours before starting.
- Report non-consensus items; they are findings.

## 4. Structured quantitative elicitation
- **Train** experts in probability and bias (anchoring, overconfidence, availability) with
  practice questions.
- **Elicit quantiles, not points**: ask for lower and upper plausible bounds *first*, then best
  estimate, then confidence that the truth lies within the bounds (IDEA's four-step format).
  Asking for the best guess first anchors the range.
- **IDEA** — Investigate, Discuss, Estimate, Aggregate: private estimates, facilitated discussion
  of reasoning, private revised estimates, mathematical aggregation.
- **SHELF** — behavioural aggregation: experts agree on a fitted distribution for a "rational
  impartial observer"; R package `SHELF` fits distributions to quantiles.
- **Cooke's classical model** — experts also answer **seed questions** (true answers known to the
  analyst); weights reflect calibration and informativeness. Performance-weighted pools often
  outperform equal weights in published evaluations.

## 5. Aggregation
- Linear opinion pool (weighted average of distributions) is simple and keeps disagreement visible.
- Don't average medians and call it a distribution; combine distributions.
- Report individual estimates (anonymised) as well as the aggregate.

## 6. Reporting
Follow a reporting guideline (e.g. **CREDES** for health-related Delphi studies): panel
selection, response rates per round, exact questions, feedback given, consensus definition,
changes to items between rounds.

## Gotchas
- Delphi consensus ≠ correctness; conformity pressure via feedback can manufacture agreement.
- Poorly worded compound statements produce meaningless ratings.
- Experts dropping out non-randomly (dissenters leave) biases later rounds — compare leavers.

## Verify
- [ ] Format chosen to fit purpose; panel criteria and composition documented.
- [ ] Consensus, stability and stopping rules defined before round 1.
- [ ] Feedback includes distribution and reasons; attrition reported per round.
- [ ] Quantities elicited as bounds-then-best with confidence; training given.
- [ ] Aggregation method stated; individual estimates retained.

*Draft: consensus thresholds and panel sizes are ranges from the literature, not standards.*
