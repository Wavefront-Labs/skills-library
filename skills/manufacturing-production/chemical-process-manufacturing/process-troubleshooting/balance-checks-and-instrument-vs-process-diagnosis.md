---
id: manufacturing-production.chemical-process-manufacturing.process-troubleshooting.balance-checks-and-instrument-vs-process-diagnosis
name: balance-checks-and-instrument-vs-process-diagnosis
category: manufacturing-production
field: chemical-process-manufacturing
product: process-troubleshooting
tags: [process-troubleshooting, troubleshooting, root-cause, mass-balance, material-balance, energy-balance, heat-balance, instrument-validation, transmitter-fault, flowmeter, level-transmitter, valve-stiction, control-valve, deviation-diagnosis, cause-isolation, historian, pi-historian, trend-analysis, process-engineer, plant-engineer, kepner-tregoe, is-is-not, yield-loss, chemical-plant, refinery]
level: advanced
status: draft
description: "Diagnose why a live process is off: frame the deviation, close mass and energy balances around it, decide whether it is the instrument or the process, and isolate the cause with minimum-risk tests."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Process troubleshooting: balances and instrument-versus-process diagnosis

**Goal:** find the real cause of a process problem (yield loss, off-spec, capacity
shortfall, a strange reading) on running plant, quickly and without making it worse.

## 1. Frame the deviation precisely
Write a one-line problem statement and an **is / is-not** table:
- **What:** which variable/product, by how much (with numbers, not "high").
- **Where:** which unit, train, line — and which similar ones are *not* affected.
- **When:** started when (pull historian data to find the step or the drift onset),
  continuous or intermittent, any pattern (shift, ambient temperature, feed tank).
- **Extent:** getting worse, stable, cycling?
Then list **changes** near the onset: maintenance, MOCs, raw material lots, weather,
production rate, catalyst age, instrument calibration. The cause is usually in the
intersection of "what is different about where/when it is" and "what changed".

## 2. Close the balances
Draw a boundary around the suspect section and check:
- **Mass balance:** in = out + accumulation. Use the best meters, convert to the same
  basis (mass, not volume, with correct densities at temperature). On a good unit an
  overall closure within a few percent is achievable; a sudden worsening of closure
  points to a meter or a leak/unaccounted stream (relief valve passing, drain open,
  stream to flare).
- **Component balance:** for the key component (e.g. product), using lab analyses —
  shows where yield goes.
- **Energy balance:** duty from steam flow × latent heat vs process side ΔT × flow ×
  Cp. A heat exchanger whose duty falls at constant conditions is fouling; one whose
  balance doesn't close has a bad meter or bad temperature.
Balances turn "it feels low" into "12% of the feed is unaccounted for after the
flash drum", which tells you where to look.

## 3. Instrument or process?
Before reacting to a reading, try to prove it:
- **Redundancy:** a second transmitter, a local gauge, a sight glass, an analyser vs lab.
- **Physical consistency:** does the reading agree with related variables? A level
  "rising" while inflow is unchanged and outflow valve opened should not happen; a
  temperature that changed but its neighbours and the heat input did not, is suspect.
- **Signal behaviour:** flatlined (frozen) values, values pinned at range limits,
  sudden steps with no process cause, noise that changed character — instrument signs.
- **Field check:** impulse lines blocked or frozen, purge failed, transmitter
  isolated, wiring/junction box wet.
- **Control valves:** compare controller output to actual valve position
  (positioner feedback). A sawtooth PV with square-wave OP is classic stiction.
Instrument faults are common; but assume process until proven, when the process
hazard is high.

## 4. Isolate the cause
- Rank hypotheses by how well each explains **all** the is/is-not facts. One that
  explains everything beats three that each explain part.
- Test with the **least risky, most informative** move first: an extra lab sample, a
  meter cross-check, swapping to the parallel pump, a small step test with operator
  agreement. Change one thing at a time and give it the process time constant to
  respond.
- Confirm the cause by making the problem go away **and** come back (or by a
  convincing physical finding) before declaring victory.

## 5. Use the historian well
- Plot candidate causes and the symptom on one time axis; shift by transport delay.
- Compare a good period and a bad period side by side (same rate, same grade).
- Beware correlation from common causes (rate drives both variables).

## Gotchas
- Tuning a loop to hide a symptom ("it oscillates, slow it down") buries the cause
  (often a sticking valve or a changed process gain).
- Lab results have error too; ask for the method's repeatability before chasing a
  1% difference.
- "Nothing changed" is rarely true; look at the MOC log, maintenance work orders and
  raw-material certificates.

## Verify
- [ ] Problem statement has numbers and an is/is-not table.
- [ ] Mass (and energy where relevant) balance done on the right boundary.
- [ ] Key readings cross-checked by an independent measurement.
- [ ] Chosen cause explains every fact in the table.
- [ ] Fix confirmed on the trend for at least one full process time constant.

*Draft note:* the is/is-not structure follows the Kepner–Tregoe style problem
analysis widely used in plants; balance closure targets vary by unit and metering.
