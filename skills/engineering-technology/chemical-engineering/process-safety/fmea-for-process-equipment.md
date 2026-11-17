---
id: engineering-technology.chemical-engineering.process-safety.fmea-for-process-equipment
name: fmea-for-process-equipment
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-hazard-identification, fmea-for-process-equipment, fmea, failure-mode-and-effects-analysis, iec-60812, rpn, equipment-failure, reliability, criticality, hazard-analysis]
level: practitioner
status: gated
description: "Perform FMEA on process equipment: list failure modes, causes, local and system effects, detection, ranking and actions, following IEC 60812 style worksheets."
sources:
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FMEA for process equipment

**Goal:** a systematic list of how equipment can fail and what happens, to guide design, maintenance and spares.

## Worksheet columns
Item/component, function, failure mode, cause, local effect, system (end) effect, detection/safeguard, severity (S), occurrence (O), detectability (D), risk ranking, recommended action, owner.

## Steps
1. **Define the system and boundaries**; list components (for example pump, motor, seal, coupling, valve, instrument).
2. **For each component**, list functions and the ways it can fail (fails to start, fails to stop, leaks, plugs, drifts, false signal).
3. **Effects**: local (the component itself), next level (the unit), end effect on the process and plant (loss of containment, trip, quality).
4. **Rank**: severity 1 to 10, occurrence 1 to 10 (common scale, not mandated (gated: unconfirmed, source is paywalled or blocked)) (from field data or generic failure rate tables), detectability 1 to 10 (higher meaning harder to detect); risk priority number RPN = S x O x D. Many practitioners prefer a severity-first criticality matrix because RPN can hide severe low-likelihood items; follow the standard and client practice (IEC 60812 describes the method and alternatives; confirm the current edition (gated: unconfirmed, source is paywalled or blocked)).
5. **Actions**: design change, monitoring (vibration, temperature), preventive maintenance, spares; re-rank after actions.
6. Link failure modes to the HAZOP and LOPA scenarios where they are initiating events.

## Practice
- Use generic failure rate data (for example from OREDA or CCPS equipment reliability data) as a starting point, and plant data when available; cite the source.
- Prioritise safety-critical functions first; limit the effort on trivial items.

## Gotchas
- Combining multiple failures is outside basic FMEA; use fault tree analysis for that.
- Do not average RPNs across items.

## Verify
- [ ] Every critical item has at least one detection or protection measure.
- [ ] Action list closed or tracked.
