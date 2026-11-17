---
id: energy-mining-utilities.power-generation.nuclear-plant-operation.conduct-of-operations-for-reactivity-manipulations
name: conduct-of-operations-for-reactivity-manipulations
category: energy-mining-utilities
field: power-generation
product: nuclear-plant-operation
tags: [nuclear-plant-operation, power-generation, nuclear, reactor-operator, sro, conduct-of-operations, reactivity-management, reactivity-manipulation, control-rods, boration, dilution, pre-job-brief, peer-check, three-way-communication, stop-when-unsure, human-performance, hu-tools, reactor-engineering, estimated-critical-position, approach-to-criticality, pwr, bwr, inpo, wano, nrc]
level: advanced
status: draft
description: "Conduct-of-operations discipline for nuclear reactivity changes: predictions, briefs, peer checks, three-way communication, and stopping when the core does not respond as predicted."
sources: ["INPO/WANO conduct-of-operations and reactivity management principles (paraphrased, public summaries)", "US NRC NUREG-1123 knowledge topics (public)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conduct of operations for reactivity manipulations

**Goal:** every deliberate change to core reactivity — rod motion, boron concentration
change, recirculation flow change, temperature change — is predicted, briefed,
controlled, peer-checked and monitored, and any unexpected response leads to a
conservative stop rather than a push to finish. This is the operating discipline,
not reactor physics or a plant procedure; only licensed operators manipulate the
reactor, under their site's approved procedures and supervision.

## 1. Why reactivity is special
Most operating events that regulators and industry bodies (INPO, WANO, NRC) flag as
significant involve **reactivity management weaknesses**: an unplanned dilution, rods
withdrawn in the wrong group, a temperature change nobody connected to reactivity,
a criticality earlier than predicted. The fix is behavioural rigour, not cleverness.

## 2. Before the manipulation
- **Prediction:** reactor engineering provides the expected response — e.g. an
  estimated critical position (ECP) for an approach to criticality, or expected
  power/temperature change per step. Know the acceptance band (an ECP is commonly
  bounded by a site limit in pcm or rod steps; know yours).
- **Pre-job brief** (shift supervisor / SRO leads): the procedure step, the
  prediction, the expected indications, what "unexpected" looks like, the stop
  criteria, roles (who moves rods, who monitors, who peer-checks), and the conservative
  action if things go wrong (e.g. stop rod motion, insert rods, stop dilution).
- Check plant conditions match the procedure's prerequisites. Verify no other
  evolution on shift will change reactivity at the same time (a feedwater heater
  being removed, a chemistry addition, a turbine load change).

## 3. During the manipulation — the human-performance tools
- **Procedure in hand**, place-keeping (mark each step as done).
- **Three-way communication:** "Withdraw control bank D to 150 steps" → "Withdraw
  control bank D to 150 steps" → "That is correct." Use the phonetic alphabet for
  letters.
- **Peer check** before the action: a second qualified person confirms the right
  control, the right direction, the right amount — *before* the hand moves.
- **Small steps, then wait** for the response: delayed neutrons and temperature
  feedback mean the full effect lags the action.
- **Monitor the right indications:** startup-rate/period, nuclear instrumentation on
  all channels, average temperature, pressure. Compare each against prediction.
- **Self-check (STAR):** Stop, Think, Act, Review.

## 4. When it does not behave as predicted
- **Stop when unsure.** Halt the manipulation and place the plant in a stable
  condition. Inform the shift supervisor.
- Example: approaching criticality, the count-rate response indicates criticality
  will occur well outside the ECP band → stop withdrawal, insert per procedure, and
  investigate before continuing. Never "just a bit more to see".
- Unexplained reactivity change with no manipulation in progress → treat as an
  abnormal condition: enter the relevant abnormal procedure, look for the source
  (dilution path, temperature change, rod drift).
- Conservative decision-making: when indications conflict, believe the one that
  says the plant is in the worse condition until proven otherwise.

## 5. After
Log the manipulation, the response and any deviation from prediction; feed
deviations to reactor engineering. Report unexpected responses through the
corrective action programme even if nothing went wrong.

## Gotchas
- "Routine" evolutions (a small dilution to hold temperature) cause most events —
  the brief can be shorter, never absent.
- Shift turnover mid-evolution is a classic error trap; avoid it or brief the
  oncoming crew on exact status.
- Distraction: the reactor operator at the controls should not be pulled into
  unrelated tasks during the manipulation.
- Uncertain: specific acceptance bands, brief formats and terminology differ
  between PWR/BWR designs, utilities and regulators — check site procedures.

## Verify
- [ ] Prediction obtained and acceptance band known before starting.
- [ ] Pre-job brief held, roles and stop criteria stated.
- [ ] Every action peer-checked and three-way communicated.
- [ ] Response compared with prediction after each step.
- [ ] Any unexpected response led to a stop, not a continuation, and was reported.
