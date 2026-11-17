---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.wire-gauge-sizing-and-current-derating
name: wire-gauge-sizing-and-current-derating
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [wire-sizing, wire-gauge, current-derating, voltage-drop, iso-6722, cable-temperature-class, bundle-derating, fuse-wire-coordination, harness-design, copper-resistance, awg]
level: practitioner
status: gated
description: "Size low-voltage vehicle wires: voltage drop, temperature class, bundle and ambient derating, fuse-wire coordination, and aluminium conductors. Worked resistance numbers."
sources:
  - "ISO 6722-1:2011 (https://www.iso.org/standard/50022.html) and ISO 6722-2:2013 (https://www.iso.org/standard/55714.html), both withdrawn"
  - "ISO 19642-1:2023 Automotive cables - Vocabulary and design guidelines (https://www.iso.org/standard/81326.html); ISO 19642-4:2019 (https://www.iso.org/standard/66302.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Wire gauge sizing and current derating

## 1. Inputs per circuit
Load current (continuous and peak), duty cycle, wire length, allowable voltage drop, ambient temperature and bundle conditions, insulation temperature class, protection device.

## 2. Voltage drop
Copper resistance at 20 degC is about 17.2 mohm per metre for a 1 mm2 conductor (resistivity 1.72e-8 ohm m (gated: unconfirmed, source is paywalled or blocked)); R scales inversely with cross-section. At higher conductor temperature multiply by (1 + 0.0039 x (T - 20)) (temperature coefficient (gated: unconfirmed, source is paywalled or blocked); this gives 1.2535 at 85 degC, computed). Include both supply and return path (or ground path), and terminal and connector resistance. Example: 10 A over 3 m round trip 6 m at 1.5 mm2 and 85 degC is R = 6 x 17.2/1.5 x 1.25 = 86 mohm and a drop of 0.86 V. Allowable drop is set by the load's voltage tolerance (typical limits range from a few hundred millivolts for sensors to a volt or so for heavy loads).

## 3. Thermal capacity
Choose the insulation class (ISO 6722-1 and 6722-2 are listed as withdrawn on iso.org and the ISO 19642 series is the successor; temperature classes run in steps such as 85, 100, 125, 150 and 175 degC (gated: unconfirmed, source is paywalled or blocked); check which standard your OEM requires). Ampacity depends on conductor temperature rise: I^2 R heating balanced against heat loss to ambient. Use a thermal model or supplier ampacity charts for the chosen cable, not a single rule table, because bundling, sleeves, ambient (engine bay vs cabin) and duty cycle change it. Derate for bundles (many loaded wires heat each other) and for hot zones.

## 4. Fuse coordination
The protective device must protect the wire: the fuse's melting characteristic (I2t) must trip before the wire insulation is damaged for any fault current, and the fuse's continuous rating must be above the load current with margin and below the wire's continuous capacity at its operating temperature. Typical practice is to load a fuse continuously to no more than about 75-80% of its nominal rating (gated: unconfirmed, source is paywalled or blocked), depending on ambient temperature derating (use supplier curves). Short-circuit protection of long thin wires needs a fuse or electronic protection at the source, not at the load.

## 5. Practical selection
Cross-sections in common use: 0.35, 0.5, 0.75, 1.0, 1.5, 2.5, 4, 6, 10 mm2 and above; use the smallest gauge that meets drop, thermal and mechanical (crimp, strength) needs; avoid very thin wires in hard-to-handle routes (minimum 0.35 or 0.5 mm2 in many harnesses). Aluminium conductors (covered in separate parts of the cable standards, for example ISO 19642-4 for 30 V a.c./60 V d.c. single-core aluminium cables) are lighter and cheaper per ampere but need larger cross-section, special terminals and corrosion control.

## Verify
- [ ] Voltage drop computed with round-trip and hot resistance.
- [ ] Ampacity checked with bundle and ambient derating at worst case.
- [ ] Fuse protects the wire and tolerates the load continuously.
- [ ] Terminal and crimp suitable for the gauge and class.
