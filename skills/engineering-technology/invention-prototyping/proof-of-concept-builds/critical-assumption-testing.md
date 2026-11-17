---
id: engineering-technology.invention-prototyping.proof-of-concept-builds.critical-assumption-testing
name: critical-assumption-testing
category: engineering-technology
field: invention-prototyping
product: proof-of-concept-builds
tags: [invention-prototyping, proof-of-concept-builds, proof-of-concept, poc, critical-assumption, riskiest-assumption, risk-retirement, de-risking, test-rig, test-plan, pass-fail-criteria, go-no-go, stage-gate, technology-readiness-level, trl, works-like-prototype, looks-like-prototype, experiment-design, measurement-uncertainty, repeatability, build-measure-learn, minimum-viable-prototype, feasibility-study, kill-criteria]
level: practitioner
status: draft
description: "Retire the riskiest unknown first: name the critical assumption, set pass/fail criteria in advance, build the minimum rig, and read results honestly for go/no-go."
sources: ["Ulrich & Eppinger, Product Design and Development (prototyping chapter)", "Montgomery, Design and Analysis of Experiments", "NASA Systems Engineering Handbook (technology readiness levels)", "Savoia, The Right It (pretotyping)", "Taylor, An Introduction to Error Analysis"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Critical-assumption testing — proof of concept that actually proves something

**Goal:** spend the least time and money to find out whether the idea's single
riskiest assumption is true, with a result you would accept even if you dislike it.

## 1. Find the critical assumption
List every assumption the concept depends on, then score each:
- **Uncertainty** (1–5): how sure are we, on evidence, not hope?
- **Impact** (1–5): if wrong, does the idea die or merely need a tweak?
Test the highest uncertainty × impact first. Typical killers: *can the mechanism
generate enough force/flow/signal at all*, *does the physics scale down*, *is the
sensor accurate in the real environment*, *will it survive N cycles*. Cosmetics and
ergonomics are rarely the critical unknown at this stage.
Separate **works-like** (function) from **looks-like** (form) prototypes; a PoC is
works-like and may look nothing like the product.

## 2. Write the test card before building
| Field | Example |
|---|---|
| Assumption | Gripper pad holds a 200 g part at 2 g lateral acceleration |
| Measure | Slip onset, by high-speed video and load cell |
| Pass | No slip at 2.5 g (25% margin) in 10/10 trials |
| Fail | Slip below 2 g in any trial |
| Ambiguous zone | 2.0–2.5 g → test second pad material |
| Budget | 3 days, parts on hand |

Setting **pass/fail and the kill criterion in advance** is the whole point: it stops
you moving the goalposts after seeing data.

## 3. Build the minimum rig
- Test the **principle**, not the product: a clamp on a bench, a borrowed motor, a
  syringe pump. Buy or borrow before you build.
- Isolate the variable: everything else fixed and, ideally, oversized so it cannot be
  the failure.
- Instrument it. Know the measurement resolution and uncertainty; a reading of 2.4 g
  from an accelerometer good to ±0.3 g does not distinguish pass from fail.
- Include a **control** or known reference (a part that should slip, a calibration weight)
  to prove the rig can detect failure.
- Safety still applies: stored energy (springs, pressure, batteries, rotating parts)
  needs guarding even on a one-day rig.

## 4. Run and read honestly
- Repeat: at least 3–5 trials, more if the spread is large relative to the margin. Report
  mean and range (or standard deviation), not the best run.
- Change one factor at a time early; use a small factorial design once you know which
  two or three factors matter.
- Log everything: date, setup photo, settings, raw data, anomalies.
- Ask "what else could explain this?" before declaring success — friction in the rig,
  a warm-up effect, an operator who unconsciously helps.

## 5. Decide
- **Go:** passed with margin → next riskiest assumption, or move up a readiness level
  (lab principle → relevant environment → integrated prototype; TRL-style scales help
  communicate this).
- **Pivot:** failed but showed which parameter limits it → change concept, retest.
- **No-go:** failed with no credible route → stop and record why. A killed idea at
  week 2 is a success compared with one killed at month 9.

## Gotchas
- Testing what is easy instead of what is risky: a beautiful enclosure for an unproven sensor.
- Rig too good: lab power, ideal alignment and a skilled operator hide field problems.
  Note every condition that differs from real use.
- One successful run is an anecdote. Variance is the result.
- Sunk cost: the more the rig cost, the harder it is to read a fail as a fail.
- Scaling: forces, heat and friction do not scale linearly with size; a half-scale success
  may not transfer.
- Dated, witnessed records of the PoC also support any later invention disclosure.

## Verify
- [ ] The tested assumption was the top-scoring uncertainty × impact item.
- [ ] Pass, fail and kill criteria were written down before the first run.
- [ ] Measurement uncertainty is smaller than the pass/fail margin.
- [ ] Results report spread over repeated trials, with a control.
- [ ] A go / pivot / no-go decision and its reason are recorded.
