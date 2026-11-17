---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.hv-battery-post-crash-safety
name: hv-battery-post-crash-safety
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [hv-post-crash, post-crash, hv-disconnect, pyro-fuse, fmvss-305, electrical-safety, isolation-resistance, electrolyte-spillage, reess-retention, thermal-event, ev-crash-safety]
level: practitioner
status: verified
description: "Define post-crash high-voltage safety: crash-triggered disconnect, isolation and discharge criteria, electrolyte and retention requirements, and delayed thermal event cautions."
sources:
  - "https://www.ecfr.gov/current/title-49/part-571/section-571.305a"
  - "https://www.ecfr.gov/current/title-49/part-571/section-571.305"
  - "UN Regulations 94, 95 and 100 and FMVSS 305 (electric vehicle post-crash requirements); UN GTR 20; confirm current texts at https://unece.org"
  - "Kramer, Passive Safety of Vehicles (chapter list)"
  - "https://www.law.cornell.edu/cfr/text/49/571.305"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

Safety-critical, regulated work. This is professional practice guidance: confirm the current regulation, edition and market, and defer sign-off to qualified safety and homologation engineers.

# HV battery post-crash safety

## 1. Objectives
After a crash the vehicle must not expose occupants or responders to electric shock, fire, or electrolyte hazard. Requirements appear in UN R94 and R95 (post-crash electrical safety criteria in frontal and side tests), FMVSS 305 in the US (applies to vehicles made before 1 September 2027; FMVSS 305a, which adds fire, explosion and gas venting requirements, is mandatory from that date, per eCFR), and UN R100 and GTR 20 for the battery itself. Thresholds and test procedures are revised; confirm the current text and your market.

## 2. Typical criteria (commonly stated; verify exact values)
- **Protection against electric shock:** after the crash test, either the HV bus voltage falls below a low-voltage limit (30 V AC or 60 V DC in FMVSS 305, checked in eCFR), or capacitor energy is below a low value (0.2 J in FMVSS 305; the UN R94/R100 value is higher, about 2 J (gated: unconfirmed, source is paywalled or blocked)), or physical protection (touch-proof, IPXXB) and isolation resistance are maintained (FMVSS 305: 500 ohm/V for AC and 100 ohm/V for DC, checked in eCFR).
- **Electrolyte spillage:** FMVSS 305 allows no visible electrolyte in the passenger compartment and at most 5.0 litres outside it, measured for 30 minutes after the vehicle stops (eCFR). UN R94/R95 limits differ; confirm.
- **REESS retention:** the battery remains attached within defined displacement limits.
- **Fire:** no fire or explosion for a period after the crash (the standards define observation periods).
Delayed thermal events (hours or days later) can still occur; the regulation windows are not a guarantee against them.

## 3. System design
- **Crash trigger:** airbag ECU or dedicated crash sensor sends a signal to the HV system; the battery contactors open and a pyrotechnic fuse/disconnect can isolate the pack and cables; discharge (active or passive) of DC-link capacitors in the inverter.
- **Redundancy:** a hardwired crash signal path plus network message; contactor open on loss of low-voltage supply; welded-contactor diagnostics and fallback (pyro).
- **Isolation monitoring** continues after the crash for as long as powered (see isolation monitoring).
- **Layout:** HV cables routed away from deformation zones with protective conduit; orange cables; service disconnect and its labelling.
- **Pack protection:** see pack crash protection design.

## 4. Validation
Crash test measurements after impact: voltage, isolation, spillage, retention, fire observation; CAE for intrusion; component tests for the disconnect; HIL tests of crash signal reaction time.

## 5. Vehicle after the crash
Provide first-responder information (rescue sheet, labels), advise on storage after a crash (quarantine, away from buildings for a period under qualified guidance), and service instructions for damaged batteries.

## Verify
- [ ] Regulation editions and thresholds confirmed per market.
- [ ] Hardwired and network crash signals tested, with timing.
- [ ] Post-crash isolation, spillage and retention measured in crash tests.
- [ ] Responder and service documentation complete.
