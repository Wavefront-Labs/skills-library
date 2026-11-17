---
id: engineering-technology.biomedical-engineering.device-verification-validation.single-fault-condition
name: single-fault-condition
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [single-fault-condition, iec-60601-testing, hipot, electrical-safety-testing, sfc, fault-analysis, normal-condition, component-fault]
level: advanced
status: draft
description: "Analyse single fault conditions for IEC 60601-1: definition, typical electrical and thermal faults, consequential faults, pass criteria and risk-file documentation."
sources: ["IEC 60601-1:2005+AMD1:2012+AMD2:2020 clause 4.7 Single fault condition for ME equipment and clause 13 Hazardous situations and fault conditions (confirm edition)", "ISO 14971 Application of risk management to medical devices", "IEC 60601-1 rationale annex"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Single fault condition analysis

**Goal:** show that the equipment remains safe when any one means of risk reduction fails, as the standard requires.

## Concept
- **Normal condition (NC):** all means of protection intact.
- **Single fault condition (SFC):** a single means for reducing a risk is defective or a single external abnormal condition is present. The equipment must remain safe: no unacceptable risk. A fault that is a **consequence** of the first fault is considered part of the same fault, and two independent faults at the same time are not required unless the first is not detected and persists (a latent fault is assumed to have occurred already, so the next fault is then the single fault).
- For parts of equipment that cannot be shown to be reliable to a very high degree, assume the failure.

## Typical faults to apply (examples from IEC 60601-1)
- Interruption of one supply conductor, and of the protective earth conductor.
- Short circuit or open circuit of components that provide protection (for example insulation of non-double or non-reinforced types, Y-capacitors, resistors in current limiters), considering component reliability tests.
- Connection of mains voltage to a signal input/output part or an applied part (for patient leakage tests).
- Overload, blocked ventilation, cooling fan failure, thermostat or thermal fuse failure, relay contacts welded.
- Software or electronics faults that cause an output to stay on.

## Procedure
1. **List protective measures** from the risk analysis and block diagram: each insulation barrier, protective earth, current limiter, thermal cut-out, interlock, safety circuit.
2. For each, define the fault and the **expected outcome** (no hazardous temperature, voltage, leakage or mechanical hazard; essential performance maintained or the device enters a safe state with an alarm).
3. **Test or analyse:** apply the fault in a test setup (short or open the component, simulate load fault) and measure the relevant hazards; use analysis for faults where testing is not feasible, with component data or reliability evidence (for example electrolytic capacitor safety rating).
4. **Document** in a table: fault, method, result, pass or fail, reference to the risk control.
5. Maintain the table as design changes occur.

## Gotchas
- Applying only the faults listed in the standard and not those unique to your design.
- Not testing combined effects with maximum ambient temperature and maximum load.
- Testing with default firmware and not with fault-injected software states.

## Verify
- [ ] Fault table covers every protective measure.
- [ ] Temperatures and leakage under fault are within limits.
- [ ] Safe-state behaviour demonstrated for software-related faults.
