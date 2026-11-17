---
id: engineering-technology.electrical-engineering.electrical-installation-design.installation-inspection-testing
name: installation-inspection-testing
category: engineering-technology
field: electrical-engineering
product: electrical-installation-design
tags: [continuity-test, earth-fault-loop-test, eic, electrical-engineering, electrical-installation-design, iec-60364-6, installation-inspection-testing, installation-testing, insulation-resistance-testing, rcd-and-loop-testing]
level: practitioner
status: draft
description: "Inspect and test new electrical installations: continuity, insulation resistance, loop impedance and RCD tests per IEC 60364-6 and BS 7671."
sources:
  - "https://www.iec.ch/"
  - "https://electrical.theiet.org/bs-7671/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Inspection and testing of installations

1. **Order (dead tests first, then live):** continuity of protective conductors and bonding, continuity of ring final circuits, insulation resistance, polarity, then earth electrode resistance, earth fault loop impedance, prospective fault current, RCD operation, phase sequence and functional testing.
2. **Insulation resistance:** test at 500 V DC for circuits up to 500 V (250 V for SELV/PELV); minimum 1 megohm for circuits (BS 7671 Table 61); disconnect electronic equipment and surge protective devices before testing.
3. **Loop impedance Zs:** measured at the furthest point; compare with the maximum value for the protective device and temperature correction (the test is at ambient conductor temperature, while the tabulated limit assumes operating temperature; use the 80 percent rule of thumb or the limits in the guidance).
4. **RCD tests:** trip at 1x I_dn within 300 ms (general) and 40 ms at 5x I_dn; test the integral test button as well.
5. **Records:** certificate (Electrical Installation Certificate in the UK), schedule of test results, and inspection checklist.
6. **Periodic inspection:** frequency set by use (for example 5 years for domestic in UK practice, shorter for commercial or special locations).
7. Testing must be performed by a competent person using calibrated test instruments (GS 38 safe test leads in the UK).

**Verify:** compare results to expected values from the design; unexpected values require investigation.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
