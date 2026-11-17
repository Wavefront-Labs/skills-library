---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.protective-earth-test
name: protective-earth-test
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [protective-earth, electrical-safety, iec-60601-1, patient-electrical-safety, earth-bond-test, iec-62353, continuity-test, ground-bond]
level: practitioner
status: gated
description: "Test protective earth continuity per IEC 60601-1 and IEC 62353: test current, source voltage limit, resistance limits with and without mains cord, and measurement technique."
sources: ["IEC 60601-1:2005+AMD1:2012+AMD2:2020 (protective earthing tests; confirm edition and values)", "IEC 62353 Recurrent test and test after repair of medical electrical equipment (confirm edition)", "Safety analyser manufacturer manuals"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Protective earth resistance test

**Goal:** confirm that exposed conductive parts connected to protective earth have a low-impedance path to earth that can carry fault current.

Values below are those usually quoted; every figure in this skill is (gated: unconfirmed, source is paywalled or blocked), so confirm in the standard and edition applied.

## Type test (IEC 60601-1)
- Pass a test current from a source with an open-circuit voltage not exceeding about 6 V through the protective earth path: **25 A** or **1.5 times the rated current** of the relevant circuit, whichever is greater, for **5 to 10 seconds**.
- Measure the voltage drop between the protective earth terminal (or the earth pin of the appliance inlet) and each accessible conductive part that is protectively earthed.
- Resistance limit: **0.1 ohm** for the equipment (with a detachable power cord), and **0.2 ohm** including the power cord if the cord is non-detachable.

## In-service test (IEC 62353)
- Lower test current and source voltage, and a limit that includes the mains cable, as set in IEC 62353 (read the test current, open-circuit voltage and limit for your edition there; they differ from the type test). Used for periodic testing and after repair.

## Method
1. Disconnect the device from mains.
2. Connect the test lead to the protective earth pin or terminal of the inlet and the probe to a bare metal accessible part (not painted).
3. Apply the current and read the resistance; flex the mains cable at the plug and strain reliefs during the test to find intermittent breaks.
4. Test each accessible conductive part that is connected to earth, including screws holding earth bonds.
5. Record test current, duration, results and instrument calibration.

## Gotchas
- Painted or anodised surfaces give false failures; connect to an intended earth point.
- Long cords raise resistance; check the cord conductor size.
- Test leads add resistance; zero them out before measurement.

## Verify
- [ ] Measured values below limits with margin.
- [ ] Equipment under test sees the specified test current (check the analyser setting).
- [ ] Earth bonds located in the design drawing and checked in production tests.
