---
id: engineering-technology.structural-engineering.etabs-sap2000.building-lateral-model
name: building-lateral-model
category: engineering-technology
field: structural-engineering
product: etabs-sap2000
tags: [etabs, sap2000, csi, structural-engineering, lateral-analysis, building-model, diaphragm, semi-rigid-diaphragm, mass-source, seismic-weight, cracked-section, property-modifiers, p-delta, modal-analysis, ritz-vectors, response-spectrum, rsa, elf, accidental-torsion, story-drift, base-shear-scaling, asce-7, aci-318, eurocode-8]
level: advanced
status: verified
description: "Build an ETABS/SAP2000 building model for lateral analysis: diaphragms, mass source, cracked stiffness, P-delta, ELF and RSA cases, scaling, drift and model checks."
sources:
  - "ASCE/SEI 7 Minimum Design Loads and Associated Criteria for Buildings and Other Structures (Chapter 12)"
  - "ACI 318 Building Code Requirements for Structural Concrete (section 6.6.3)"
  - "CSI Analysis Reference Manual (Computers and Structures, Inc.)"
  - "ETABS User's Guide and technical knowledge base (Computers and Structures, Inc.)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# ETABS / SAP2000 building lateral model — a model you can defend

**Goal:** a building model whose mass, stiffness and load cases are right for lateral
(wind and seismic) design, scaled per code, with drift and modal results you have
checked against hand numbers before any member design starts.

Numbers below are ASCE 7-16/7-22 and ACI 318-19 unless stated; the engineer of record
must confirm the governing code edition. ASCE 7 and ACI 318 are paywalled, so clause numbers and factors below are unconfirmed against the code text (gated: unconfirmed, source is paywalled or blocked), except where noted. Secondary sources (Structure magazine FAQ; ideCAD help citing the clause) agree that ASCE 7-16 12.9.1.4.1 scales RSA forces to 100% of ELF V and that the superseded practice was 85%; 12.9.1.4.2 is the drift clause. Menu paths move between ETABS versions —
the ones named here are from recent versions (v20+) and may differ in yours.

## 1. Geometry and stiffness
1. Set units and grid first; model to centrelines, with rigid end zones (ETABS
   "end length offsets") of 0 to 0.5. Use 0 for a conservative drift check, and only
   go higher if you can justify it for concrete joints.
2. **Cracked properties** (ACI 318 6.6.3.1.1, strength-level lateral analysis): beams
   0.35 Ig, columns 0.70 Ig, cracked walls 0.35 Ig, uncracked walls 0.70 Ig, flat
   plates/slabs 0.25 Ig (gated: unconfirmed, source is paywalled or blocked). Assign them as property modifiers. Many offices run a separate
   wind-serviceability model with stiffer modifiers (ACI permits 1.4 times the
   strength values for service drift) (gated: unconfirmed, source is paywalled or blocked).
3. **Slabs in a lateral model:** model them as membrane/shell with near-zero bending
   modifiers (or a 0.25 modifier) unless you deliberately want slab-frame action.
   Otherwise a full-stiffness slab quietly becomes a moment frame.
4. **Diaphragms:** rigid is fine for compact concrete floors. Use **semi-rigid** for
   transfer levels, large openings, long thin plans, podium/backstay floors and any
   place where you need diaphragm forces. Collectors only get force from a semi-rigid
   diaphragm.
5. **Supports:** columns fixed or pinned at the foundation to match the real detail.
   Bound podium backstay stiffness (stiff and soft) rather than guessing one value.

## 2. Mass source
Define the mass source from element self-mass plus additional mass from load patterns:
SDL at 1.0, and live at 0.25 for storage areas only. Add partitions at the greater of
the actual load or 10 psf (0.5 kPa), and flat-roof snow at 0.2 where the flat-roof snow
load exceeds 30 psf (ASCE 7 12.7.2) (gated: unconfirmed, source is paywalled or blocked).
**Gotcha:** if the Dead pattern has a self-weight multiplier of 1 *and* you tick
"element self mass", do not also add the Dead pattern as mass. That double-counts W.

## 3. Load cases
- **P-Delta:** set it once, from a gravity combination (typically 1.2D + 0.5L, or
  1.0D + 0.25L), iterative or non-iterative based on loads. Linear cases then use the
  P-delta stiffness. Check the ASCE 7 stability coefficient θ anyway.
- **Modal:** Ritz vectors seeded from the lateral loads and gravity, with enough modes
  for 90% mass participation in each direction. ASCE 7-22 also allows including the
  residual mass instead, so check your edition.
- **ELF:** user coefficient or the built-in auto-seismic. Enter the period limit
  (Cu·Ta) and the 5% accidental eccentricity in both directions. Some versions apply
  eccentricity through the diaphragm eccentricity override, so check the load-case
  output.
- **RSA:** CQC modal combination, SRSS directional combination (or 100% + 30%
  orthogonal combinations), scale factor g·Ie/R, plus accidental eccentricity.
- **Wind:** use auto-wind per ASCE 7, or apply story forces from a hand or tunnel
  calculation, including the torsional cases (ASCE 7 Fig. 27.3-8 cases 2 to 4; gated: unconfirmed, source is paywalled or blocked).

## 4. Scaling and drift
1. Compare the RSA base shear to the ELF base shear in each direction. ASCE 7-16/22
   12.9.1.4 requires scaling *forces* to 100% of ELF V. Before ASCE 7-16 it was 85%.
2. Drifts can use the unscaled RSA (with the Cs minimum provisions in 12.9.1.4.2), and
   ELF drift may use the computed period without the Cu·Ta cap (12.8.6.2).
3. Design story drift Δ = Cd·δxe/Ie at the building corners, not the centre of mass.
   Common limit: 0.020 hsx for Risk Category I/II (ASCE 7 Table 12.12-1) (gated: unconfirmed, source is paywalled or blocked); check structure type, since the limit varies.

## 5. Model sanity checks (do them every time)
- Base reactions under each gravity pattern equal hand totals within about 2%.
- Seismic weight per floor area looks plausible: roughly 100–200 psf (5–10 kPa) for
  concrete floors and 60–100 psf (3–5 kPa) for steel composite floors. These are rough
  office rules of thumb (gated: unconfirmed, source is paywalled or blocked).
- Mode 1 and mode 2 are translational and mode 3 is torsional. A torsional first mode
  means a lateral system layout problem, not a modelling one.
- The computed T is within about 1.5 × Cu·Ta (rule of thumb; gated: unconfirmed, source is paywalled or blocked). Much longer usually means missing
  stiffness or bad releases.
- Animate the mode shapes to spot floating joints and unintended mechanisms.
- Run Analyze › Check Model before every analysis, and treat all warnings, including
  ill-conditioning, as errors.

## Verify
- [ ] Gravity reactions match hand totals; seismic weight is not double-counted.
- [ ] Cracked modifiers are assigned and match the purpose (strength vs serviceability).
- [ ] Modal mass participation is at least 90% (or the residual is included) in both directions.
- [ ] RSA forces are scaled to the code fraction of ELF V for the governing edition.
- [ ] Corner drifts are amplified by Cd/Ie and below the Table 12.12-1 limit.
- [ ] No unresolved Check Model warnings or ill-conditioning messages.
