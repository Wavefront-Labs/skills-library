---
id: social-sciences.sports-science-kinesiology.motor-control-learning-research.retention-transfer-tests-and-coordination-dynamics
name: retention-transfer-tests-and-coordination-dynamics
category: social-sciences
field: sports-science-kinesiology
product: motor-control-learning-research
tags: [motor-control-learning-research, motor-learning, motor-control, skill-acquisition, kinesiology, sports-science, retention-test, transfer-test, learning-vs-performance, acquisition-phase, practice-schedule, contextual-interference, blocked-practice, random-practice, feedback-frequency, knowledge-of-results, guidance-hypothesis, attentional-focus, external-focus, coordination-dynamics, hkb-model, relative-phase, continuous-relative-phase, vector-coding, movement-variability, uncontrolled-manifold, ucm, dynamical-systems, visuomotor-adaptation, sequence-learning]
level: practitioner
status: draft
description: "Design motor-learning experiments that separate learning from performance with retention and transfer tests, and analyse coordination with relative phase and variability."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Retention, transfer tests and coordination dynamics

**Goal:** show that a practice manipulation changes *learning* (a relatively permanent
capability) rather than just performance during practice, and quantify how movement
coordination is organised and changes.

## 1. Learning ≠ performance
Practice conditions that boost performance during acquisition can harm learning, and
vice versa (contextual interference; frequent feedback — the guidance hypothesis).
So the dependent variable is measured **after** practice:
- **Retention test:** same task, no augmented feedback, after a delay — immediate
  (~10 min) and delayed (≥ 24 h, allowing consolidation; sleep effects are debated).
- **Transfer test:** a novel variation (new parameter, new context, other limb). Many
  theories predict transfer differences more than retention differences.
- Report acquisition curves too, but don't infer learning from them alone.

## 2. Typical paradigms
| Paradigm | Measures | Notes |
|---|---|---|
| Visuomotor rotation / force-field adaptation | Angular error, aftereffects | Separates implicit and explicit processes (aiming reports) |
| Serial reaction time (SRT) | RT drop on sequence vs random blocks | Awareness checks needed |
| Discrete aiming / throwing | Constant error, variable error, absolute error | Report CE and VE separately — AE mixes them |
| Timing tasks | Timing error, variability | |
| Sport-specific skills | Outcome scores + kinematics | Ecological but harder to control |

## 3. Classic manipulations and cautions
- **Contextual interference** (random > blocked practice for retention): robust in lab
  tasks, weaker in applied/sport studies and for novices on complex skills.
- **Reduced or self-controlled feedback**: once considered robust; recent large,
  preregistered studies (e.g. on self-controlled practice) have found much smaller or
  null effects. Power accordingly.
- **External focus of attention** (on the effect, not the body; Wulf): large literature,
  but meta-analytic estimates are affected by publication bias — treat effect sizes cautiously.

## 4. Design details
- Pre-test (baseline) so groups can be compared on change; randomise to group; control
  practice amount (trials, time) exactly.
- Practice blocks and tests in counterbalanced orders where tests are repeated.
- Analyse with mixed models (participant random effects), testing group × phase.
- Avoid ceiling: tasks must leave room to improve.

## 5. Coordination dynamics
Dynamical systems view: coordination patterns are attractors; transitions occur as a
control parameter (e.g. movement frequency) is scaled.
- **HKB model** (Haken–Kelso–Bunz): bimanual in-phase is stable; anti-phase destabilises
  and switches to in-phase at higher frequencies — the canonical demonstration.
- **Discrete relative phase:** timing of a peak in one oscillator relative to the
  other's cycle.
- **Continuous relative phase (CRP):** from phase angles (Hilbert transform preferred
  over position–velocity phase portraits, which need normalisation) — interpret with caution
  for non-sinusoidal signals.
- **Vector coding** of angle–angle plots for joint coupling in gait/running; use circular
  statistics for averaging angles.
- **Variability analysis:** **Uncontrolled manifold (UCM)** separates "good" variability
  (not affecting the task outcome) from "bad"; also standard deviation of CRP,
  detrended fluctuation and entropy measures for structure of variability.

## Gotchas
- Learning claims without a delayed retention/transfer test are performance claims.
- Group differences at baseline undermine change comparisons — check and adjust.
- Averaging angular data linearly is wrong near the 0/360 boundary.
- Uncertain: strength of several "classic" effects is actively being re-evaluated; check the latest replications.

## Verify
- [ ] Retention (≥ 24 h) and/or transfer tests without augmented feedback included.
- [ ] Practice amount equalised; groups randomised and compared at baseline.
- [ ] Error components (CE, VE) reported separately.
- [ ] Coordination measure (CRP, vector coding, UCM) chosen and computed with circular statistics where needed.
- [ ] Sample size justified with realistic, bias-aware effect sizes.
