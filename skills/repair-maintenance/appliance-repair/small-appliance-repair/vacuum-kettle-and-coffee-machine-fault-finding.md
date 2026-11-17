---
id: repair-maintenance.appliance-repair.small-appliance-repair.vacuum-kettle-and-coffee-machine-fault-finding
name: vacuum-kettle-and-coffee-machine-fault-finding
category: repair-maintenance
field: appliance-repair
product: small-appliance-repair
tags: [appliance-repair, small-appliance-repair, vacuum-cleaner, cordless-vacuum, dyson, vacuum-motor, brushroll, belt, kettle, thermostat, strix-control, coffee-machine, espresso-machine, descaling, citric-acid, solenoid-valve, pump, ulka-pump, stand-mixer, kitchenaid, gear-grease, fan, thermal-fuse, mains-cable, security-screws, repair-cafe]
level: intro
status: draft
description: "Repair common small appliances: vacuum suction loss and brushroll faults, kettles that won't switch on/off, espresso machines that won't pump or heat, mixers and fans, plus safety tests."
sources: ["Repair Café / iFixit community repair guides (general practice)", "Author's synthesis; designs vary widely"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vacuum, kettle and coffee machine fault-finding

**Goal:** fix the frequent, cheap faults in small household appliances, and know when a
repair is unsafe or uneconomic. Small appliances are often mains-powered with exposed
live parts once opened: unplug, and never test opened mains devices live unless you are
trained and using an isolating transformer/RCD.

## Toolkit
Security bits (Torx Tamper-resistant T10/T15/T20, tri-wing, oval/"Dyson"-style), spudgers
for clips, multimeter, plus a way to **safety-test** afterwards (insulation resistance and
earth continuity — PAT-style tester, or at least a megger-mode meter).

## 1. Vacuum cleaners: loss of suction (90 % airflow, 10 % motor)
1. Empty the bin/bag; wash filters (let dry 24 h; washing a non-washable HEPA filter ruins it).
2. **Find the blockage** section by section: hose (drop a coin through it, or shine a torch
   through), wand, cyclone inlet, head. Suction at the motor end but not the hose end = hose block.
3. **Brushroll not spinning:** hair wrapped at the bearings (cut along the groove with a seam
   ripper); belt snapped or stretched; on powered heads, the head motor or its contacts.
   Many uprights have a belt-protect clutch/reset.
4. Cordless sticks that pulse on/off: blockage tripping the airflow sensor, or a worn
   battery pack failing under load (check pack under load or swap a known-good one).
5. Motor runs with burning smell/sparks: carbon brushes worn (some motors allow brush
   replacement), or bearings. Brushless digital motors are usually replaced as a unit.

## 2. Kettles
- **Won't switch on:** base connector dirty/burned, or the base cable; the "steam
  thermostat" (bi-metal, often a Strix-type control) or the dry-boil protector has tripped
  or failed. Measure continuity through the control with the switch on.
- **Won't switch off:** steam path blocked (lid not closed, steam tube scaled) so the
  steam thermostat never sees steam. Descale and check the steam channel.
- Scale: citric acid ~1–2 tablespoons per litre of hot water, soak 30–60 min, rinse well
  (twice boil-and-discard).
- Leaking at the element seal: usually not economical to repair; replace the kettle.

## 3. Espresso / coffee machines
1. **No water through the group:** scale. Descale with the maker's descaler or citric
   acid solution; run through the boiler and group. Check the water tank's inlet valve/filter.
2. **Pump noisy but no flow:** airlock (prime by opening the steam/hot-water valve with
   the pump running), blocked inlet, or a failed vibration pump (e.g. Ulka-type:
   replacements are common and cheap; check coil resistance and that it's the correct
   voltage/flow model).
3. **No heat:** thermal fuse/thermal cutoff on the boiler (often one-shot; find why it blew —
   dry boiling, failed thermostat), boiler element resistance, thermostat continuity.
4. **Weak/dribbly espresso but heats fine:** blocked group shower screen and gasket
   (backflush with a blind basket and detergent on machines with a 3-way solenoid valve),
   grind too fine, scaled solenoid.
5. Bean-to-cup: brew unit removal/cleaning and lubrication with food-safe silicone grease
   fixes many errors; follow the model's cleaning sequence.

## 4. Mixers, blenders, fans
- Stand mixers (planetary): grinding noise or the head stalls → worn gear or old grease
  (re-grease with food-grade gear grease; the nylon "worm follower" gear is designed to
  fail first and is a cheap part).
- Fans: dry/seized sleeve bearings (clean and oil with light machine oil), capacitor on
  induction fan motors (slow start/hum) — replace with the same µF and voltage rating.

## 5. After any repair: safety test
- Class I (earthed): earth continuity from plug earth to exposed metal (low ohms).
- Insulation resistance live/neutral to earth or to exposed metal (Class II) ≥ 1 MΩ
  typical PAT limit at 500 V DC.
- Cable: replace damaged mains cables entirely; no taped joints.

## Gotchas
- Thermal fuses blow for a reason; replacing them with a wire link is never acceptable.
- Lithium battery packs: don't open, puncture or charge swollen packs.
- Uncertain: part and fault patterns are common-case heuristics, not universal.

## Verify
- [ ] Appliance unplugged during work; security screws reinstalled.
- [ ] Root cause found (blockage, scale, worn part), not just symptom cleared.
- [ ] Thermal protectors replaced like-for-like, never bypassed.
- [ ] Earth continuity and insulation resistance pass.
- [ ] Appliance runs a full normal cycle without overheating or tripping the RCD.
