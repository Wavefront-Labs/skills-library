---
id: architecture-construction.structural-trades.structural-welding.welding-structural-steel-to-a-wps-with-fit-up-and-inspection
name: welding-structural-steel-to-a-wps-with-fit-up-and-inspection
category: architecture-construction
field: structural-trades
product: structural-welding
tags: [structural-trades, structural-welding, welding, wps, pqr, welder-qualification, aws-d1-1, as-nzs-1554, iso-5817, bs-en-1090, fcaw, smaw, gmaw, stick-welding, flux-core, fillet-weld, cjp, complete-joint-penetration, groove-weld, fit-up, root-gap, backing-bar, preheat, interpass-temperature, low-hydrogen, electrode-storage, undercut, porosity, visual-inspection, ndt, ultrasonic-testing]
level: advanced
status: draft
description: "Weld load-bearing steel to a qualified WPS: joint prep and fit-up, preheat, positional technique, consumable control, and visual inspection to the code's acceptance criteria."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Welding structural steel to a WPS, with fit-up and inspection

**Goal:** welds that meet the structural welding code because each one was made to a
qualified procedure by a qualified welder, on a properly fitted joint, and then inspected.
(Codes: AWS D1.1 in the US, AS/NZS 1554.1 in AU/NZ, ISO 5817/BS EN 1090-2 in Europe/UK.)

## 1. The WPS is the rulebook
- A **Welding Procedure Specification** defines: process (SMAW, FCAW, GMAW), base
  metal and thickness range, filler/consumable, joint design (groove angle, root opening,
  root face), position, preheat and interpass temperatures, electrical parameters
  (amps, volts, travel speed, polarity), and shielding gas.
- It's supported by qualification testing (PQR) or is prequalified per the code.
- Welders must be **qualified** for the process, position and thickness — check their
  current certificate/continuity record.
- Read the WPS for each joint before starting. Changing a variable outside its range
  means the weld isn't to procedure.

## 2. Joint prep and fit-up
- Bevel (flame/plasma cut or machined) to the WPS angle and root face; grind off slag,
  scale, paint, oil, galvanising (where welding galvanised steel is allowed it needs
  specific procedures and fume control) and moisture ~25 mm each side.
- Fit-up gap/root opening within the WPS tolerance — too tight = lack of penetration;
  too wide = burn-through and excess weld.
- Backing bars fused fully where specified; tack welds made by qualified welders to the
  same WPS (tacks become part of the weld).
- Check alignment/misalignment limits and fillet leg sizes required on the drawing.

## 3. Preheat and conditions
- Preheat per WPS — depends on thickness, carbon equivalent and hydrogen level. Thicker
  sections and higher-strength steels need more (e.g., ~10–150 °C+ ranges in tables).
- Measure with temperature crayons/contact thermometer at the specified distance from
  the joint, on the opposite face where possible.
- Respect maximum interpass temperature.
- Protect from wind (shielding gas blown away → porosity), rain and cold. Dry the joint.

## 4. Consumables
- **Low-hydrogen** electrodes (e.g., E7018) stored in heated ovens once opened, per
  manufacturer/code exposure limits; re-dry or discard exposed rods. Wet consumables
  cause hydrogen cracking — sometimes hours after welding.
- FCAW wire kept dry and clean; correct gas/flux combination.

## 5. Technique by position
- Flat (1G/1F) easiest; vertical (3G/3F) up-hill for structural work usually required
  (downhill only if the WPS permits); overhead (4G/4F) with smaller beads.
- Clean slag between every pass; grind starts/stops; stagger stops on multipass welds.
- Back-gouge CJP welds to sound metal before welding the second side where specified.

## 6. Inspection
- **Visual (100%)**: profile, size (fillet gauge), undercut, porosity, cracks, overlap,
  arc strikes, spatter — against the code acceptance criteria for the loading type.
- **NDT** as specified: MT/PT for surface cracks, UT or RT for CJP groove welds; often a
  percentage of welds, increased if defects found.
- Delayed inspection for hydrogen cracking on high-strength/thick materials (the code may
  require a wait time).
- Repairs to an approved repair procedure; re-inspect.

## Gotchas
- Welding outside the WPS ("I've always done it this way").
- Damp electrodes → delayed cracking.
- No preheat on thick flanges in cold weather.
- Undersized fillets because gaps weren't accounted for (fillet size increases with gap
  in many codes).

## Verify
- [ ] WPS available at the joint; welder qualified for process/position/thickness.
- [ ] Fit-up checked (gap, bevel, alignment) before welding.
- [ ] Preheat measured and recorded.
- [ ] Visual inspection to the code criteria; NDT results on file.
- [ ] Repairs documented and re-inspected.

*Status: draft — summary of common code requirements; the project's specified code and
WPS govern every value.*
