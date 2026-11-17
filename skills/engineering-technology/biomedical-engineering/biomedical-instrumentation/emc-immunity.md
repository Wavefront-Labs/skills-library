---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.emc-immunity
name: emc-immunity
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [emc-immunity, medical-emc, iec-60601-1-2, esd, radiated-immunity, eft, surge, proximity-fields, basic-safety-essential-performance]
level: advanced
status: gated
description: "Plan EMC immunity testing for medical electrical equipment under IEC 60601-1-2: ESD, radiated RF, EFT, surge, dips and home-use levels, with pass criteria from the risk file."
sources: ["IEC 60601-1-2 Medical electrical equipment - Electromagnetic disturbances - Requirements and tests (4th edition 2014 with Amendment 1 2020; confirm current edition and regional adoption)", "IEC 61000-4 series basic immunity test methods", "FDA guidance on EMC for medical devices (current text on fda.gov)"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# EMC immunity for medical electrical equipment

**Goal:** show the device keeps its basic safety and essential performance in the electromagnetic environments of use.

Every test level below is (gated: unconfirmed, source is paywalled or blocked). The numbers below are typical of IEC 60601-1-2 4th edition and must be checked against the edition accepted in your market and the environment you declare (professional healthcare facility, home healthcare, special).

## Build the test plan
1. **Define essential performance** and the allowed degradation per test, from the risk file (see essential-performance).
2. **Declare the environment:** professional healthcare facility, home healthcare, or special; the home environment tests are harsher in some respects.
3. **Choose immunity tests** (indicative levels):
   - ESD (IEC 61000-4-2): contact discharge 8 kV and air discharge up to 15 kV (gated: unconfirmed, source is paywalled or blocked).
   - Radiated RF (IEC 61000-4-3): about 3 V/m for professional facilities, up to 10 V/m for home use, over 80 MHz to 2.7 GHz (gated: unconfirmed, source is paywalled or blocked), plus spot **proximity-field** levels near RF communications bands.
   - EFT/burst (61000-4-4): around 2 kV on mains (gated: unconfirmed, source is paywalled or blocked).
   - Surge (61000-4-5), conducted RF (61000-4-6), magnetic field at mains frequency (61000-4-8), voltage dips and interruptions (61000-4-11).
4. **Set the monitoring** (what to watch during each test: waveforms, alarms, measurement error) and acceptance criteria; a failure is any loss of essential performance outside the tolerance.
5. **Test in the worst-case configuration:** all cables, accessories, modes, battery and mains.

## Design measures
- Shielded enclosures with seams and cable entries treated; ferrites and filters; input protection; PCB layout with continuous ground; software watchdogs and sensor validity checks.

## Gotchas
- Wireless features need their own radio standard tests plus coexistence.
- Software changes can alter EMC response; assess.

## Verify
- [ ] Test report from an accredited lab with the declared environment.
- [ ] Pass criteria linked to risk analysis, not just "no damage".
- [ ] Re-test after hardware change.
