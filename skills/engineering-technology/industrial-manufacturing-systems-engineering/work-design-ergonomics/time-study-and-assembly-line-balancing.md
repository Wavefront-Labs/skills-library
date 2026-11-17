---
id: engineering-technology.industrial-manufacturing-systems-engineering.work-design-ergonomics.time-study-and-assembly-line-balancing
name: time-study-and-assembly-line-balancing
category: engineering-technology
field: industrial-manufacturing-systems-engineering
product: work-design-ergonomics
tags: [time-study, stopwatch-study, work-measurement, standard-time, normal-time, performance-rating, allowances, pfd, mtm, most, predetermined-time, line-balancing, assembly-line-balancing, precedence-diagram, ranked-positional-weight, rpw, takt-time, balance-efficiency, balance-delay, yamazumi, standard-work, ergonomics, niosh-lifting-equation, workstation-design, industrial-engineering]
level: practitioner
status: gated
description: "Set standard times by stopwatch study (cycles, rating, PF&D allowances), then balance an assembly line to takt with precedence diagrams, RPW heuristic and balance efficiency."
sources:
  - "Niebel & Freivalds, Methods, Standards, and Work Design"
  - "Groover, Work Systems and the Methods, Measurement, and Management of Work"
  - "NIOSH, Applications Manual for the Revised NIOSH Lifting Equation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time study and assembly-line balancing

**Goal:** get defensible standard times for every work element, then assign elements
to stations so each station's load sits just under takt, with no ergonomic hot spots.

## 1. Fix the method before timing it
Timing a bad method standardises waste. Agree the method, tools and part presentation
first, write it as standard work, then train a qualified operator on it.

## 2. Run the stopwatch (or video) study
1. Break the task into **elements** of roughly 2-30 s with clear audible/visible break
   points ("grasp screwdriver" ends when hand touches it).
2. Pilot ~10 cycles; compute mean x̄ and standard deviation s per element.
3. **Cycles needed** for ±5% at 95% confidence: n = (1.96 × s ÷ (0.05 × x̄))².
   Example: x̄ = 12.0 s, s = 1.5 s → (1.96 × 1.5 ÷ 0.6)² = 24.01 → round up to 25 cycles (recomputed: 24.01). Normal time 13.2 s, standard time 15.18 s, 175/60 = 2.92, efficiencies 97% and 73%, and the 58 s / s = 5 s station exceeding a 60 s takt about 34% of cycles were all recomputed.
4. **Rate** the operator's pace against a defined normal (100%); rating needs trained,
   periodically calibrated observers (rating films). Discard foreign elements (a dropped
   part, a chat), but log irregular-but-real ones (refill bin every 50 parts) and prorate them.
5. **Normal time** = observed mean × rating. 12.0 s × 110% = 13.2 s.
6. **Standard time** = normal × (1 + allowance), allowance as a fraction of job time.
   Personal, fatigue and delay (PF&D) allowances commonly total ~10-20% (gated: unconfirmed, source is paywalled or blocked); fatigue
   allowance rises with load, posture, heat and noise. At 15%: 13.2 × 1.15 = **15.2 s**.
   (Some systems apply allowances on a workday basis, ST = NT ÷ (1 - a); state which.)
For new designs with no line to time, use a predetermined-time system (MTM-1, MTM-UAS,
MOST); they need certified analysts and are licensed systems.

## 3. Build the precedence diagram
List each element with its standard time and its immediate predecessors; draw it as a
network. Add zoning constraints (must be same station: hold-and-torque; must be
separate: wet and electrical) and positional constraints (top-side vs underside).

## 4. Balance to takt
Cycle time C = takt (or slightly less, to absorb variation: many lines plan at
~90-95% of takt, a common practice (gated: unconfirmed, source is paywalled or blocked)). Then:
- **Theoretical minimum stations** = ⌈Σ t ÷ C⌉.
- **Ranked positional weight (RPW)**: for each element, weight = its time + times of all
  elements that follow it. Assign in descending weight to the first station where
  precedence is satisfied and remaining time allows; open a new station when nothing fits.
- **Balance efficiency** = Σ t ÷ (stations × C); balance delay = 1 - efficiency.

Example: 7 elements total 175 s; takt 60 s → minimum ⌈2.92⌉ = 3 stations. If precedence
allows 3: efficiency 175 ÷ 180 = 97% (too tight to run; no slack for variation).
At 4 stations: 175 ÷ 240 = 73%; use the spare time for in-station quality checks or
rebalance at a lower takt. Plot each station as a **yamazumi** (stacked bar) against
the takt line so the balance can be seen and discussed on the floor.

## 5. Check each station's ergonomics
- Reach and height: work at roughly elbow height (lower for heavy work, higher for
  precision); keep frequent reaches inside the normal reach zone.
- **Lifting**: revised NIOSH equation, RWL = 23 kg × HM × VM × DM × AM × FM × CM (load constant and form confirmed in NIOSH documents on CDC Stacks);
  Lifting Index = load ÷ RWL. LI > 1 indicates elevated risk; aim for ≤ 1 by design.
- Avoid repeated high-force pinch grips, wrist deviation and overhead work; rotate
  operators across stations where repetition is high. Check local regulation for
  manual handling limits.

## Gotchas
- A balance that uses the mean time ignores variation: a station at 58 s mean with
  s = 5 s will exceed a 60 s takt often. Leave slack at high-variation stations.
- Mixed-model lines must be balanced on the weighted model mix, then checked per model
  so no single model overloads a station (sequence high/low content models).
- Standards drift as methods change; re-study after any method or product change.

## Verify
- [ ] Method is standardised and documented before timing.
- [ ] Cycle count meets the confidence/accuracy formula; rating basis and allowance basis stated.
- [ ] Precedence and zoning constraints are respected in the station assignment.
- [ ] Station loads ≤ planned cycle time with slack where variation is high.
- [ ] Balance efficiency reported; yamazumi chart shows each station against takt.
- [ ] Every lift has an LI ≤ 1 or a documented mitigation.
