---
id: engineering-technology.electrical-engineering.motor-drive-design.motor-testing
name: motor-testing
category: engineering-technology
field: electrical-engineering
product: motor-drive-design
tags: [electrical-engineering, ieee-43, insulation-resistance, megger, motor-drive-design, motor-insulation-test, motor-testing, polarisation-index, surge-and-winding-resistance-test, vibration-based-condition-monitoring]
level: practitioner
status: draft
description: "Test motor condition: insulation resistance, polarization index, winding resistance, surge test and vibration trends."
sources:
  - "https://standards.ieee.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Motor insulation and condition testing

1. **Safety:** isolate, lock out, discharge windings after testing, test only on de-energised and grounded equipment by competent personnel.
2. **Insulation resistance (IEEE 43):** apply DC (500 V for rated up to 1 kV; higher for medium-voltage) for 1 min; minimum acceptable `IR_min = kV + 1` megohm for older windings and about 100 megohm for modern random-wound at 40 C, corrected to 40 C (halves for every 10 C rise). Confirm with the standard.
3. **Polarization index:** `PI = IR(10 min)/IR(1 min)`; values above about 2 are generally acceptable for class B/F/H windings per the guide; meaningless if the 1-minute value exceeds 5000 megohm.
4. **Winding resistance:** compare phases (within about 1 percent) and with factory values corrected for temperature.
5. **Surge comparison test** finds turn-to-turn faults; hipot DC test on medium voltage is applied cautiously.
6. **Vibration and thermography:** ISO 20816 velocity trends and bearing frequencies; thermography on terminal boxes under load.
7. Trend values over time; one reading is less informative than a change.

**Verify:** record test conditions (temperature, humidity, voltage) with each reading so they are comparable.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
