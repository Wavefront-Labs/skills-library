---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.hot-stamping-boron-steel
name: hot-stamping-boron-steel
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [hot-stamping, press-hardening, boron-steel, 22mnb5, phs, tailored-tempering, al-si-coating, vda-238-100, ultra-high-strength, crash-materials]
level: practitioner
status: gated
description: "Specify hot-stamped (press-hardened) boron steel parts: process route, coating, tailored properties, trimming, weld and ductility checks, and use in pillars and rails."
sources:
  - "Kramer, Passive Safety of Vehicles (chapter list)"
  - "Steel supplier press-hardening guidelines and VDA 238-100 (plate bending test); confirm current documents"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Hot stamping boron steel

Furnace temperature, cooling-rate and 1500 MPa figures are unconfirmed (gated: unconfirmed, source is paywalled or blocked).

## 1. Process
Blanks of boron-alloyed steel (22MnB5 is the classic grade) are heated in a furnace to austenitise (typically in the region of 900-950 degC), transferred to the press, formed and held in a water-cooled die so the part cools quickly enough to form martensite (a critical cooling rate on the order of tens of kelvin per second is often cited; confirm with the supplier's data). The result is an ultra-high strength part with a tensile strength of about 1500 MPa in the as-quenched state and complex shape with little springback.

## 2. Coating
Uncoated blanks scale and need shot blasting after; Al-Si coated blanks avoid scale and protect against decarburisation (with a furnace dwell that forms an Fe-Al-Si layer); zinc-based coatings exist but need process control to avoid cracking. Coating affects spot weld schedules, adhesive bonding and corrosion performance.

## 3. Tailored properties
- **Tailor-welded blanks:** different thickness or grade in one blank.
- **Tailored tempering:** die zones heated or cooled differently to produce softer, more ductile regions (for example in a B-pillar foot), improving energy absorption at the intrusion limit.
- **Patchwork blanks** to add local thickness.

## 4. Crash use
Pillars, roof rails, sills, tunnel and bumper beams, where intrusion resistance is the target. Low elongation (single-digit percent) means the part can crack under bending; use designs that load it in bending-compression with controlled hinge zones, and soften deliberately (tempered zones) where folding is needed. Include HAZ softening at welds in the CAE.

## 5. Quality and joining
Trimming is hard on tools after hardening: use laser cutting or hot trimming. Check hardness (Vickers) distribution, microstructure, plate bending angle (VDA 238-100 type test), coating thickness and weld nugget strength. Hydrogen-related delayed cracking is a concern for very high strength parts at cut edges and in service; follow supplier controls on hydrogen uptake (furnace atmosphere dew point).

## Verify
- [ ] Blank, coating and furnace cycle specified; cooling rate verified in tooling.
- [ ] Zones needing ductility have tailored tempering or geometry.
- [ ] Weld and adhesive schedules qualified for the coating.
- [ ] Bending angle and hardness acceptance defined and audited.
