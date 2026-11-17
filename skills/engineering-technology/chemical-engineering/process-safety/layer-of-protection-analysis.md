---
id: engineering-technology.chemical-engineering.process-safety.layer-of-protection-analysis
name: layer-of-protection-analysis
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, lopa, layer-of-protection-analysis, hazop, risk-assessment, initiating-event, ipl, independent-protection-layer, pfd, pfdavg, rrf, conditional-modifier, enabling-condition, tolerable-risk, tmel, sif, sis, sil, sil-determination, iec-61511, isa-84, ccps, relief-valve, api-520, api-521, safety-instrumented-system, functional-safety]
level: advanced
status: gated
description: "Run a LOPA: scenario selection from HAZOP, initiating-event frequency, IPL credit rules, PFD arithmetic, tolerable-risk gap and SIL target per IEC 61511."
sources:
  - "CCPS, Layer of Protection Analysis: Simplified Process Risk Assessment (method only)"
  - "CCPS, Guidelines for Initiating Events and Independent Protection Layers in LOPA (method only)"
  - "IEC 61511 Functional safety: Safety instrumented systems for the process industry sector (current edition)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Layer of protection analysis (LOPA)

**Goal:** for each high-consequence HAZOP scenario, estimate how often the consequence
happens with the existing safeguards, compare it with your organisation's tolerable
frequency, and size any gap as a SIL target or another protection layer.

**Scope warning.** LOPA is a semi-quantitative, order-of-magnitude tool. It must be run to
your company's risk criteria and the **current editions** of IEC 61511 (ISA 61511 in the
US) and CCPS guidance, by a team with a competent, experienced facilitator, and the result
reviewed and approved before it is used for design. The numbers below are typical
illustrations, not values to copy into a study.

## 1. Pick the scenario
One cause → one consequence pair, from the HAZOP (e.g. "level control fails, LV closes,
vessel overpressures, rupture, fire"). Define the consequence in terms your risk matrix uses
(fatalities, environmental release, cost). Cases that are too complex (many interacting
causes, common-mode failures) need a fault tree or QRA instead.

## 2. Initiating event frequency (IEF, per year)
Use company or CCPS tabulated values with their stated conditions. Typical orders:
- BPCS control loop failure: ~0.1 /y (IEC 61511 does not allow claiming a BPCS dangerous
  failure rate below 1e-5 per hour; 1e-5 x 8760 h = 0.088 /y, computed (gated: unconfirmed, source is paywalled or blocked) for the clause itself).
- Pump seal leak, gasket failure: ~0.1–0.01 /y depending on type.
- Operator error on a routine task: ~0.01–0.1 per opportunity, times opportunities per year.
For tasks done a few times a year (batch steps, start-up), multiply by frequency of
the operation and apply enabling conditions (fraction of time at risk) only where they
are real and documented.

## 3. Credit only true IPLs
An IPL must be **independent** (of the initiating event and the other IPLs: separate sensor,
logic, final element), **specific**, **dependable** (PFD validated), and **auditable**
(tested, maintained, under management of change). Typical PFDs (illustrative; values gated (gated: unconfirmed, source is paywalled or blocked)):
- BPCS loop independent of the initiator: 0.1 (usually only one BPCS layer credited).
- Operator response to an independent alarm with enough time to act (often ≥ 10–20 min
  between alarm and consequence; use your company rule): 0.1.
- Pressure relief valve sized and installed for **this** scenario (inlet/outlet per the
  current API 520/521, relief load calculated for this cause): 0.01.
- Dike/bund, passive fire protection: ~0.01.
- SIF: per its SIL (SIL 1: PFD 0.1–0.01; SIL 2: 0.01–0.001; SIL 3: 0.001–0.0001; confirm the low-demand table in IEC 61511 (gated: unconfirmed, source is paywalled or blocked)).
Not IPLs: training, procedures alone, PPE, the sensor that already failed in the initiator,
a relief valve that is undersized for the case, "good design practice".

## 4. Arithmetic
f_mitigated = IEF × Π(PFD_IPL) × Π(conditional modifiers)
Conditional modifiers (probability of ignition, of personnel presence, of fatal injury) are
allowed only if your company procedure allows them; many apply them only at high level or
not at all. Then:
RRF_required = f_mitigated / f_tolerable, SIF PFD_avg target = 1/RRF_required.

## Worked example (illustrative numbers)
Vessel overpressure from control-loop failure; tolerable frequency for this consequence
category = 1e-5 /y (company criterion, assumed).
- IEF = 0.1 /y.
- High-pressure alarm (independent transmitter) + operator, 20 min available: PFD 0.1.
- PSV sized for the blocked-outlet case: PFD 0.01.
- No modifiers.
f_mitigated = 0.1 × 0.1 × 0.01 = 1e-4 /y. Gap = 1e-4/1e-5 = 10 → SIF with PFD ≤ 0.1,
i.e. SIL 1, and design it well inside the band (e.g. PFD_avg ≈ 0.01–0.05) rather than on the
boundary. Alternatively, an inherently safer change (vessel rated for the maximum pump
shut-off pressure) removes the scenario; ask that question first.

## 5. Record and close out
For each scenario record: cause, consequence, IEF source, each IPL with PFD and its
justification, modifiers, gap, recommendation, owner. The SIF then goes into the safety
requirements specification and its PFD_avg is verified with real proof-test interval,
architecture and failure data. LOPA results are invalid if IPLs are not tested at the
interval assumed.

## Gotchas
- Double counting: the alarm and the BPCS loop that failed share a transmitter → not independent.
- One relief valve cannot be credited for a case it wasn't sized for (fire vs blocked outlet vs
  runaway reaction loads differ by orders of magnitude).
- Order-of-magnitude rounding: don't report 3.7e-5 as more precise than it is.
- Uncertain specific values above (operator-response time rule, seal-leak IEF ranges) vary
  between companies and CCPS editions; check yours.

## Verify
- [ ] Each scenario is a single cause–consequence pair traced to the HAZOP.
- [ ] IEF and every PFD cite a source (company table / CCPS) and its conditions.
- [ ] Every IPL passes independence, specificity, dependability, auditability.
- [ ] Gap, SIL target and alternatives (inherently safer design) recorded.
- [ ] Study done to the current IEC 61511 / CCPS guidance and reviewed by a competent person.
