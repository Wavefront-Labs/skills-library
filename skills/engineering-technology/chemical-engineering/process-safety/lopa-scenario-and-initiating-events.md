---
id: engineering-technology.chemical-engineering.process-safety.lopa-scenario-and-initiating-events
name: lopa-scenario-and-initiating-events
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-lopa-and-sil, lopa-scenario-and-initiating-events, lopa, layer-of-protection-analysis, initiating-event-frequency, scenario-development, tolerable-risk, mitigated-event-likelihood, conditional-modifiers, ccps]
level: advanced
status: gated
description: "Develop a LOPA scenario: define consequence and tolerable frequency, select initiating events and frequencies, and compute mitigated frequency per CCPS LOPA practice."
sources:
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LOPA scenario and initiating event frequency

**Goal:** a single cause-consequence pair evaluated against a tolerable risk target. LOPA is a semi-quantitative method from CCPS (Layer of Protection Analysis: Simplified Process Risk Assessment, 2001); it must be performed by trained practitioners using the organisation's approved criteria and data.

## Steps
1. **Select the scenario** from HAZOP or other PHA: one initiating event leading to one consequence (for example loss of cooling leading to overpressure and vessel rupture).
2. **Consequence** categorised by severity (multiple fatality, single fatality, serious injury, environmental, financial) per the company risk matrix; give the unmitigated outcome.
3. **Tolerable frequency** for that consequence category (company criterion, for example 1e-5 per year for a fatality-level event; use your own, not a published number from memory).
4. **Initiating event frequency (per year)**: use the organisation's table or published data (CCPS provides typical ranges). Typical orders of magnitude: BPCS loop failure about 0.1 per year; pump seal failure about 0.1 per year; cooling water failure about 0.1; operator error on a routine task about 0.1 to 0.01 per opportunity (scaled by the number of opportunities); a general gasket leak much lower. Confirm site-specific values (the typical orders of magnitude above are unconfirmed, CCPS data is paywalled (gated: unconfirmed, source is paywalled or blocked)).
5. **Enabling conditions and conditional modifiers**: probability the unit is in the relevant mode, probability of ignition, probability of the area being occupied, probability of fatality given exposure.
6. **Mitigated frequency** = f_initiating x (product of the PFDs of independent protection layers) x conditional modifiers.
7. **Compare with the tolerable frequency**; the shortfall is the risk reduction (in orders of magnitude) still needed (the required PFD of additional layers).

## Gotchas
- Use one initiating event per scenario; multiple initiating events should be summed separately.
- Initiating event frequencies must come from a consistent source; mixing optimistic and pessimistic numbers invalidates the result.
- Frequencies and PFDs are order-of-magnitude, not precise; document conservative choices.

## Verify
- [ ] Scenario description is complete: initiating event, consequence, safeguards considered.
- [ ] Data sources and tolerable criteria cited.
