---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.esd-protection-design
name: esd-protection-design
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [esd-protection, medical-emc, iec-60601-1-2, esd, tvs-diode, transient-protection, iec-61000-4-2, enclosure-design]
level: practitioner
status: gated
description: "Design medical device inputs and enclosures to survive IEC 61000-4-2 ESD: discharge paths, TVS selection, ground strategy, enclosure seams, and recovery behaviour."
sources: ["IEC 61000-4-2 Electrostatic discharge immunity test (confirm edition)", "IEC 60601-1-2 (ESD test levels; confirm edition)", "Ott, Electromagnetic Compatibility Engineering"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ESD protection design

**Goal:** the device withstands electrostatic discharge during use without damage or loss of essential performance, and recovers cleanly.

## Targets
IEC 60601-1-2 (4th edition) requires contact discharge to conductive accessible parts at 8 kV and air discharge to insulating surfaces at 2, 4, 8 and 15 kV (confirm in the edition applied) (gated: unconfirmed, source is paywalled or blocked), at several polarity and repetition conditions. Define acceptable behaviour from the risk file (no change in essential performance, or automatic recovery).

## Strategy
1. **Keep the discharge outside:** use insulating enclosures with adequate wall thickness and overlap seams (a labyrinth) so that air discharge does not reach the internals; avoid exposed screws and gaps near circuitry.
2. **Give the current a path:** conductive enclosures bonded to a chassis ground; connector shells bonded 360 degrees; discharge currents flow around, not through, the electronics.
3. **Clamp at the entry:** bidirectional **TVS diodes** with low capacitance for high-speed lines, placed right at the connector with short, wide traces to ground; check clamping voltage versus the protected IC's absolute maximum; series resistors or ferrites reduce peak current.
4. **Ground plane:** continuous plane under the board; avoid slots under signal traces; keep reset, interrupt and clock lines short and filtered.
5. **Isolated applied parts:** barrier components (capacitors, optocouplers) must withstand ESD; protect on the patient side with series resistance and diodes (also see defibrillation protection in ECG design).
6. **Software resilience:** watchdog, brown-out detection, debounced inputs, sensor validity checks, and a safe restart sequence; state retained for continuous therapy.
7. **Touch surfaces and displays:** capacitive touch controllers need ESD-tolerant designs; test through the front panel.

## Gotchas
- TVS far from the connector adds inductance and fails to clamp the first nanoseconds.
- Isolated grounds that float can collect charge; give a high-value bleed resistor and capacitor to chassis.
- ESD can cause latent damage that appears later; run repeated discharges and function tests.

## Verify
- [ ] Pre-compliance with an ESD gun at all accessible points and seams.
- [ ] Post-test full function check and leakage test.
- [ ] Documented behaviour for any degradation within allowed criteria.
