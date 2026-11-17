---
id: engineering-technology.electronics-engineering.emc-design.emc-layout-and-precompliance
name: emc-layout-and-precompliance
category: engineering-technology
field: electronics-engineering
product: emc-design
tags: [emc-design, emc, emi, electromagnetic-compatibility, cispr-32, cispr-35, fcc-part-15, en-55032, iec-61000-4-2, esd, radiated-emissions, conducted-emissions, immunity, common-mode-current, cable-emissions, return-path, filtering, common-mode-choke, ferrite, shielding, near-field-probe, lisn, pre-compliance, spread-spectrum]
level: advanced
status: docs-checked
description: "Design boards to pass FCC Part 15 / CISPR emissions and IEC 61000-4 immunity: return paths, filtering, cable treatment, near-field pre-compliance scans."
sources:
  - "https://www.ecfr.gov/current/title-47/part-15/section-15.107"
  - "https://www.ecfr.gov/current/title-47/part-15/section-15.109"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# EMC by design and pre-compliance — pass the chamber on the first visit

**Goal:** design so emissions and immunity margins exist before the lab visit, and use
cheap bench pre-compliance to find and fix problems while the board is still changeable.

## 1. Know the limits you face
- Emissions for IT/multimedia: **CISPR 32 / EN 55032** (Class A / Class B) and, in the
  US, **FCC Part 15 Subpart B**. The CISPR limits are in the paid standard: read the
  current edition. FCC limits (47 CFR 15.107 and 15.109) are free on eCFR.
- FCC conducted limits, measured with a 50 µH / 50 ohm LISN, general (Class B) limits
  in dBµV: quasi-peak 66 to 56 (decreasing with log frequency) from 0.15 to 0.5 MHz,
  56 from 0.5 to 5 MHz, 60 from 5 to 30 MHz; average 56 to 46, 46, 50 over the same
  bands. Class A: quasi-peak 79 (0.15-0.5 MHz) and 73 (0.5-30 MHz); average 66 and 60.
- FCC radiated limits at 3 m for devices other than Class A digital (general limits),
  in µV/m: 100 (30-88 MHz), 150 (88-216 MHz), 200 (216-960 MHz), 500 above 960 MHz.
  Class A digital devices are specified at 10 m: 90, 150, 210 and 300 µV/m over the same
  bands.
- Immunity is covered by CISPR 35 / EN 55035 and the IEC 61000-4 series (ESD, radiated
  RF, EFT, surge, conducted RF); take test levels from the current editions.
- Product-specific standards (medical, automotive, industrial) can override these.

## 2. The physics that matters most
- **Cables radiate, boards mostly don't.** Small common-mode currents on attached
  cables are a common cause of failing radiated emissions. Every design decision below
  is about keeping common-mode noise off cables.
- **Loop area is the antenna**: every signal current returns, at high frequency
  directly under its trace in the reference plane. Gaps force a detour = loop area
  = emissions and susceptibility.
- **Edge rate, not clock frequency, sets spectrum reach**: slower edges are free margin.

## 3. Layout and circuit rules
1. **One solid ground plane** (more layers help for fast digital). No splits
   under signals; partition by placement.
2. **All connectors on one edge** where possible, so cable-to-cable noise voltage
   across the ground plane is minimised.
3. **Filter at the connector**, at the point where cables enter: series ferrite or
   resistor plus capacitor to chassis/ground, common-mode chokes on differential
   pairs and power inputs. A filter in the middle of the board is bypassed by coupling.
4. **Chassis bond**: on metal enclosures, a low-inductance connection from board ground
   to chassis at the I/O connector (multiple screws/gaskets, not a long wire).
5. **Cable shields**: 360° termination to the connector shell/chassis. A long pigtail
   degrades a shield at high frequency.
6. **Switching regulators**: minimise the hot loop (input cap–switch–diode), keep the
   switch node copper small, consider gate resistors/snubbers to slow edges, and use
   input π-filters (C–L–C) for conducted emissions.
7. **Clocks**: series-terminate at source, route on inner layers between planes if
   possible, and use spread-spectrum clocking where the interface tolerates it (it
   lowers peak, not total, energy — it helps against quasi-peak/peak detectors).
8. **ESD**: TVS at the connector with the shortest path to ground/chassis, series
   resistance or ferrite after the TVS, reset and long-trace inputs filtered.

## 4. Bench pre-compliance
Kit: spectrum analyser (or SDR-based analyser for rough work), H-field near-field
probe set, RF current clamp, LISN for conducted, a preamp.
1. **Near-field scan** the board with an H-probe to find sources (regulators, clocks,
   ICs). Near-field amplitude does not map to far-field dBµV/m — it is for locating
   and for A/B comparison only.
2. **Clamp each cable** to measure common-mode current. Convert with the transfer
   impedance of the clamp and use the result to rank cables. Treat this as relative.
3. **Conducted**: LISN between supply and DUT, analyser at the LISN output with a
   limiter/attenuator to protect its input. This can track the real limit fairly
   closely.
4. **Fix-and-compare**: add a ferrite, change a capacitor, slow an edge — remeasure in
   the same setup. Change one thing at a time.
5. **ESD**: an ESD gun at rated levels on the connectors and seams; watch for resets,
   lock-ups, and data corruption, not just damage.

## 5. Plan the lab visit
Book a pre-scan at an accredited lab early; take spare ferrites, capacitors, copper
tape and firmware builds with clocks/features switchable, and a written mode list.

## Verify
- [ ] Applicable standards and class identified with the current editions.
- [ ] Every cable entry has a filter or shield termination at the connector.
- [ ] No high-speed or switching trace crosses a plane gap; connectors grouped on one edge.
- [ ] Common-mode current on each cable measured and ranked; the worst one addressed.
- [ ] Conducted emissions with a LISN show a margin to the limit that you chose in advance.
- [ ] ESD at the specified levels causes no unrecovered malfunction.

## Checked
2026-11-01. Confirmed on eCFR: 47 CFR 15.107 conducted limits (Class A and general/Class B tables, 50 µH / 50 ohm LISN) and 15.109 radiated limits (general limits at 3 m, Class A digital at 10 m). Removed (paid standards CISPR 32/35, IEC 61000-4 and textbooks not readable): CISPR dBµV/m limits, ESD test voltages, the 20 dB/decade roll-off formula, the Ott microamp rule of thumb, the 6 dB margin and the 3 m versus 10 m conversion. Design rules in section 3 and the bench method are practice guidance, not figures.
Method: documentation only; no commands were run.
