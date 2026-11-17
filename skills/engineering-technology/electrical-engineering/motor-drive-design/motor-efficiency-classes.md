---
id: engineering-technology.electrical-engineering.motor-drive-design.motor-efficiency-classes
name: motor-efficiency-classes
category: engineering-technology
field: electrical-engineering
product: motor-drive-design
tags: [efficiency-class-ie, electrical-engineering, ie3, iec-60034-30-1, motor-drive-design, motor-efficiency-classes, motor-nameplate, nema-design-b, nema-premium-and-design-letters]
level: intro
status: draft
description: "Read motor nameplates and compare IEC 60034-30-1 IE efficiency classes and NEMA design letters."
sources:
  - "https://www.iec.ch/"
  - "https://www.nema.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Motor nameplate and efficiency classes

- **Nameplate items:** rated power (kW or hp), voltage, frequency, current, speed, power factor, efficiency, duty (S1 continuous), insulation class, IP code, service factor (NEMA), design letter or IEC design N/H.
- **IEC 60034-30-1** defines IE1 to IE4 (and IE5 in the newer edition) classes for 0.12 kW to 1000 kW motors at 50 and 60 Hz; efficiency is determined by IEC 60034-2-1. Regional regulations mandate minimum levels (for example IE3 in the EU for most motors, with IE2 plus VSD for some) and change over time; check local law.
- **NEMA:** MG 1 defines design letters (A, B, C, D) by locked-rotor torque, breakdown torque and slip; Design B is the general purpose. NEMA Premium is the high-efficiency label for MG 1 tables.
- **Payback:** efficiency gain times operating hours times energy tariff against the extra purchase price; running hours dominate.
- **Slip and speed:** rated speed differs with efficiency class; a high-efficiency motor runs a little faster, which raises fan and pump power by the speed cubed.

**Verify:** compare the guaranteed efficiency at 75 and 100 percent load from the datasheet or test report.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
