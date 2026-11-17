---
id: engineering-technology.biomedical-engineering.device-verification-validation.dielectric-strength-test
name: dielectric-strength-test
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [dielectric-strength, iec-60601-testing, hipot, electrical-safety-testing, dielectric-withstand, humidity-preconditioning, mopp, y-capacitor]
level: advanced
status: gated
description: "Run IEC 60601-1 dielectric strength tests: test voltages by MOPP and MOOP and working voltage, humidity preconditioning, ramp and duration, pass criteria and common failures."
sources: ["IEC 60601-1:2005+AMD1:2012+AMD2:2020 Medical electrical equipment - General requirements for basic safety and essential performance (clause 8.8 insulation and 8.9 creepage; confirm edition and table values)", "IEC 62353 Recurrent test and test after repair of medical electrical equipment", "UL 60601-1 and CSA C22.2 No. 60601-1 national differences"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dielectric strength (hipot) testing

**Goal:** show that insulation withstands the voltage stress the standard requires, between the parts that need isolating.

Values below reflect common use of IEC 60601-1 3rd edition and must be confirmed against the edition and tables for the working voltage and means of protection you declared.

## Determine the test voltage
- Identify each insulation barrier (for example mains to protectively earthed accessible parts, mains to applied part, applied part to enclosure) and classify it as a means of patient protection (MOPP) or operator protection (MOOP), basic, supplementary, double or reinforced.
- Use the standard's tables for the **working voltage** across that barrier. Typical values at up to 250 V rms working voltage: 1 MOPP 1500 V ac; 2 MOPP 4000 V ac; MOOP basic 1500 V ac and reinforced about 3000 V ac. Check the table for other working voltages. These figures (gated: unconfirmed, source is paywalled or blocked).
- DC test at a higher voltage (approximately 1.4 times the ac rms) is accepted in some cases (gated: unconfirmed, source is paywalled or blocked); confirm.

## Procedure
1. **Humidity preconditioning:** typically 48 h at 93% relative humidity and 20-30 C, then test within a short time in the same conditions (confirm times (gated: unconfirmed, source is paywalled or blocked)).
2. Disconnect or protect components that cannot withstand the test voltage per the standard's instructions (for example surge protectors across the barrier), and keep Y-capacitors in place only where the standard allows; document any modifications.
3. Apply the test voltage from zero, ramped to no more than half then rising to full within about 10 seconds; hold for 1 minute (gated: unconfirmed, source is paywalled or blocked).
4. **Pass:** no insulation breakdown (sustained arc or flashover); corona or momentary current spikes are judged per the standard.
5. Measure temperatures and test at operating temperature where required.
6. Repeat for each barrier; record voltage, duration, trip current and the tester calibration.

## Common failures
- Creepage or clearance too small at connectors and PCB slots (see creepage-clearance).
- Contaminated or damp boards, and transformers with thin insulation.
- Isolated DC-DC converters with inadequate isolation rating.

## Verify
- [ ] Tester calibrated and trip current set per the standard.
- [ ] Every barrier tested and recorded in a table.
- [ ] Post-test insulation resistance and function checks.
