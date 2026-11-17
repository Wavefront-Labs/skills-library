---
id: engineering-technology.chemical-engineering.process-safety.hazop-guidewords-and-deviations
name: hazop-guidewords-and-deviations
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-hazard-identification, hazop-guidewords-and-deviations, hazop, guidewords, deviations, parameters, causes-and-consequences, safeguards, hazard-identification, no-flow, reverse-flow]
level: practitioner
status: gated
description: "Apply HAZOP guidewords (no, more, less, as well as, part of, reverse, other than) to process parameters to generate deviations, causes and consequences systematically."
sources:
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HAZOP guidewords and deviation logic

**Goal:** a complete, repeatable generation of credible deviations for each node. The study must be run by a trained facilitator within the applicable standard (IEC 61882; CCPS Guidelines).

## Method
For each node, apply each **guideword** to each relevant **parameter** to form a **deviation**, then find causes, consequences and existing safeguards.

## Guidewords (IEC 61882 set; confirm the list and wording in the current edition (gated: unconfirmed, source is paywalled or blocked))
- **No / None**: complete negation of the intent (no flow).
- **More / Less**: quantitative increase or decrease (more pressure, less temperature).
- **As well as**: qualitative increase (an extra component, extra phase).
- **Part of**: qualitative decrease (only part of the intent is achieved).
- **Reverse**: logical opposite (reverse flow).
- **Other than**: complete substitution (wrong material, wrong operation).

## Parameters (typical)
Flow, pressure, temperature, level, composition, phase, viscosity, reaction rate, mixing, and time-related, plus operability items (start-up, shutdown, sampling, maintenance, services/utilities failure, corrosion).

## Typical deviations
- No flow: blocked line, pump failure, valve closed in error; consequence: pump damage, reactor overheating if cooling stops.
- More pressure: blocked outlet, external fire, thermal expansion, control valve failure open; consequence: over-pressure, loss of containment.
- Reverse flow: pump trip with high downstream pressure, check valve failure; consequence: backflow into a lower rated system.
- Other than: wrong feed delivered; consequence: unexpected reaction.

## For each cause
1. Describe the **cause** and credible initiating event.
2. State the **consequence** without credit for safeguards at first (worst credible case), then list **safeguards** (design, alarms, instrumented systems, relief).
3. Apply the risk matrix to rank; if the risk is not tolerable, make a **recommendation**.

## Gotchas
- Do not turn the study into a design session; record the issue and move on.
- Do not skip a deviation because "it can't happen"; record and justify.
- Listing safeguards that are not independent of the initiating cause overstates protection.

## Verify
- [ ] Every parameter and guideword combination for the node considered or marked not applicable.
- [ ] Each tolerable-risk judgement uses the pre-agreed matrix.
