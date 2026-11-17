---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.emc-risk-management
name: emc-risk-management
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [emc-risk, emc-risk-management, iec-60601-1-2, essential-performance-emc, immunity-levels]
level: advanced
status: draft
description: "Link EMC to risk management under IEC 60601-1-2: define essential performance, environment, immunity levels, pass criteria, mitigation and the documentation expected."
sources: ["IEC 60601-1-2 Medical electrical equipment - Electromagnetic disturbances - Requirements and tests (confirm edition and amendment)", "ISO 14971 Application of risk management to medical devices", "https://www.iec.ch"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# EMC and risk management

**Goal:** make EMC a risk-based design activity instead of a late test, with immunity levels and pass criteria justified by hazard.

## Method
1. Define the intended electromagnetic environments (professional healthcare facility, home healthcare, special environments) and the **essential performance** that must survive disturbances (see essential-performance).
2. Identify EMC-related hazardous situations in the ISO 14971 file: loss of alarm, false reading, therapy delivery error, reset, communication loss, damage.
3. For each, set the **immunity test level** and **pass criteria** (what degradation is acceptable) from the standard's tables and risk analysis. The standard allows different levels when justified by the risk file; the justification must be documented.
4. Design mitigation: filtering, shielding, grounding, layout, software watchdog and error detection, hardware interlocks.
5. Test per the standard (see emc-emissions and emc-immunity), including special wireless and proximity-field tests added in recent editions (confirm edition requirements).
6. Document in the technical file: the EMC risk summary, test plan, results and instructions (labelling about environment, accessory use and distance from RF sources).

## Traps
- Stating essential performance only as "device works".
- Accepting a pass criterion unrelated to harm.
- Changing a cable, shield or firmware after the EMC test without assessing impact.

## Verify
- [ ] Essential performance and pass criteria written and linked to hazards.
- [ ] Test report covers all enclosure ports and cables used.
- [ ] Labelling states environments and accessories tested.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
