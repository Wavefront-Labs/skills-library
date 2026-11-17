---
id: engineering-technology.materials-engineering.polymer-engineering.plastic-part-creep-design
name: plastic-part-creep-design
category: engineering-technology
field: materials-engineering
product: polymer-engineering
tags: [materials-engineering, polymer-engineering, plastics, polymers, thermoplastics, creep, creep-modulus, apparent-modulus, isochronous-stress-strain, stress-relaxation, hdt, heat-deflection-temperature, iso-75, astm-d648, glass-transition, tg, rti, ul-746b, injection-moulding, injection-molding, weld-lines, knit-lines, moisture-absorption, nylon, polycarbonate, pom, acetal, glass-filled, campus-database, environmental-stress-cracking]
level: practitioner
status: gated
description: "Design load-bearing plastic parts for creep and temperature: creep modulus from isochronous data, HDT limits, moisture, weld lines and moulding effects."
sources:
  - "Crawford, Plastics Engineering (Butterworth-Heinemann)"
  - "Osswald and Menges, Materials Science of Polymers for Engineers (Hanser)"
  - "Malloy, Plastic Part Design for Injection Molding (Hanser)"
  - "ISO 899-1, Plastics: Determination of creep behaviour, tensile creep"
  - "ISO 75 / ASTM D648, temperature of deflection under load"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plastic part creep design — sizing thermoplastics for long-term load

**Goal:** size a load-bearing plastic part so it still meets its deflection and
strength limits after years at temperature, using time- and temperature-dependent
data instead of the short-term datasheet modulus.

## 1. Define the real service envelope
Write down: sustained load (and how long — hours, 1 year, 10 years), peak temperature
and how long it lasts, humidity/water contact, chemicals (oils, cleaners, sunscreens),
and allowable deflection or strain. A latch loaded for seconds and a bracket loaded
for ten years at 60 °C need entirely different moduli.

## 2. Use the creep (apparent) modulus, not the tensile modulus
Polymers are viscoelastic: strain grows under constant stress. For hand calculations,
substitute a **creep modulus** E_c(t, T, σ) = σ / ε(t) into ordinary elastic formulas
("pseudo-elastic design").
1. Get creep data for the exact grade: tensile creep curves (ISO 899-1 / ASTM D2990)
   at your temperature, or **isochronous stress–strain curves** (stress vs strain at
   fixed times such as 1 h, 1000 h, 10⁴ h). The CAMPUS database and supplier design
   guides publish these for many grades.
2. Pick the time = design life, read strain at your stress, compute E_c.
3. Extrapolation: on a log-time plot, extending data by about one decade is commonly
   accepted; further needs time-temperature superposition or testing.
4. Illustrative magnitudes (verify with grade data (gated: unconfirmed, source is paywalled or blocked)): unfilled POM at 23 °C may fall
   from ~2.8 GPa short-term to roughly 1.2–1.5 GPa after 1000 h at moderate stress;
   glass-filled grades retain a larger fraction.

Also cap strain: many designers limit sustained strain to roughly 0.5–1% for amorphous
plastics (PC, ABS, PMMA — prone to crazing) and 1–2% for tough semi-crystallines
(PP, PE, PA, POM). These are rules of thumb (gated: unconfirmed, source is paywalled or blocked); use the supplier's guidance.

## 3. Temperature limits — know what HDT does not mean
- **HDT** (ISO 75 / ASTM D648) is the temperature at which a bar deflects a set amount
  under 0.45 or 1.8 MPa in a short ramp test. It is a **ranking** number, not a
  service limit. Long-term load-bearing use is usually well below it.
- **Tg** matters most for amorphous polymers: stiffness collapses near Tg (PC ~145 °C,
  ABS ~105 °C; typical values (gated: unconfirmed, source is paywalled or blocked)). Semi-crystallines keep useful stiffness between Tg and melting,
  especially glass-filled.
- **RTI** (UL 746B) gives a long-term thermal ageing temperature for electrical,
  mechanical-with-impact and mechanical-without-impact properties — use it for
  thermal ageing, separately from creep.

## 4. Account for moisture and processing
- **Nylons (PA6, PA66) absorb water**: unfilled PA6/PA66 figures of ~2.5–3% at 50% RH equilibrium and ~8–9%
  saturated are typical values (gated: unconfirmed, source is paywalled or blocked) (supplier datasheets for glass-filled grades show 1.2–2.6% equilibrium absorption and a conditioned modulus 15–50% below dry, so the effect is grade-dependent). Modulus can drop by half from
  "dry as moulded" (DAM) values. Design with conditioned data.
- **Weld (knit) lines** can retain only ~50–90% of base strength (gated: unconfirmed, source is paywalled or blocked), much less in glass-
  filled grades where fibres do not cross the line. Ask for a mould-flow analysis and
  move gates so weld lines avoid high-stress zones.
- **Fibre orientation** in glass-filled parts makes stiffness and shrinkage anisotropic:
  cross-flow stiffness may be ~50–70% of flow-direction values (gated: unconfirmed, source is paywalled or blocked).
- **Moulded-in stress** and sharp corners: keep inside radius ≥ ~0.5× wall thickness;
  uniform walls (typically 1–4 mm) reduce sink, warp and residual stress.

## 5. Check strength with a safety factor
Compare sustained stress to **creep rupture** data at the design life and temperature,
not to short-term yield. Typical overall factors of 2–4 on rupture stress are common
practice (gated: unconfirmed, source is paywalled or blocked); the governing product standard may set its own.

## Gotchas
- **Environmental stress cracking**: amorphous plastics (PC, ABS) under modest strain
  can crack within days in contact with oils, alcohols or cleaners. Test with the
  real chemical at the real strain.
- **Stress relaxation** loosens press fits and screw bosses over time; use metal
  inserts or design for loss of preload.
- Datasheet values are dry, 23 °C, short-term, on ideal test bars.
- Regrind content and colour masterbatch can change properties; specify them.

## Verify
- [ ] Deflection was computed with a creep modulus at design life and maximum temperature.
- [ ] Sustained strain is within the material's recommended limit.
- [ ] Service temperature justified against creep data/RTI, not HDT alone.
- [ ] Moisture-conditioned properties used for hygroscopic polymers.
- [ ] Weld lines and fibre orientation checked against high-stress regions.
- [ ] Chemical exposure tested at the design strain.
