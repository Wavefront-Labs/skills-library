---
id: engineering-technology.materials-engineering.corrosion-engineering.galvanic-corrosion-and-cathodic-protection
name: galvanic-corrosion-and-cathodic-protection
category: engineering-technology
field: materials-engineering
product: corrosion-engineering
tags: [materials-engineering, corrosion-engineering, corrosion, galvanic-corrosion, bimetallic-corrosion, dissimilar-metals, galvanic-series, area-ratio, cathodic-protection, cp, sacrificial-anode, galvanic-anode, iccp, impressed-current, design-current-density, coating-breakdown-factor, anode-mass, anode-utilisation, aluminium-anode, zinc-anode, magnesium-anode, ag-agcl, cse-reference-electrode, protection-potential, dnv-rp-b401, iso-15589, ampp, isolation-kit, seawater, buried-pipeline]
level: practitioner
status: gated
description: "Assess galvanic corrosion with the galvanic series and area ratio, then size a sacrificial-anode cathodic protection system from design current density."
sources:
  - "Jones, Principles and Prevention of Corrosion (Prentice Hall)"
  - "Revie and Uhlig, Corrosion and Corrosion Control (Wiley)"
  - "DNV-RP-B401, Cathodic Protection Design (DNV)"
  - "ISO 15589-1 and -2, Cathodic protection of pipeline systems"
  - "Peabody, Control of Pipeline Corrosion (NACE/AMPP)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Galvanic corrosion and cathodic protection — judge the couple, then size the anodes

**Goal:** decide whether a dissimilar-metal joint will corrode and how to stop it,
and produce a first-pass sacrificial-anode cathodic protection (CP) design whose
numbers a CP specialist can check.

## 1. Is there a galvanic problem?
Galvanic corrosion needs all four: two metals at different potentials, electrical
contact, a shared electrolyte, and a cathodic reaction (usually dissolved oxygen).
Break any one and it stops.

Galvanic series in flowing seawater, most active (anodic) first, approximate (qualitative ordering from standard texts (gated: unconfirmed, source is paywalled or blocked)):
magnesium → zinc → aluminium alloys → carbon/low-alloy steel, cast iron → active
stainless, lead, tin → brasses, copper, bronzes → copper-nickel → passive stainless
(304/316) and nickel alloys → titanium → graphite/carbon fibre.

Rules for a couple:
- **Potential gap**: commonly quoted guidance is ≤ ~0.15 V for harsh (marine, outdoor
  wet), ≤ ~0.25 V for normal, ≤ ~0.5 V for dry controlled environments (gated: unconfirmed, source is paywalled or blocked). Treat as
  screening, not a guarantee; check the relevant standard for your sector.
- **Area ratio dominates**: corrosion rate of the anode scales roughly with cathode/
  anode area. Steel rivets in a copper sheet fail fast; copper rivets in steel sheet are
  usually tolerable. Never make the fastener the anode.
- **Carbon fibre (CFRP) is strongly cathodic**: aluminium in contact with CFRP needs a
  glass-fibre ply or sealant barrier.

## 2. Mitigation options (in order of preference)
1. Choose metals close in the series, or make the fastener the more noble metal.
2. **Isolate**: non-conductive washers, sleeves and gaskets (flange isolation kits);
   check that no other path (earthing, pipe supports) shorts it.
3. **Coat the cathode** (or both) — never coat only the anode: a holiday in the anode
   coating creates a tiny anode next to a huge cathode.
4. Exclude the electrolyte: sealants, drainage, avoid crevices.
5. Apply cathodic protection.

## 3. Sacrificial-anode CP sizing (first pass)
1. **Protection criterion** (typical, verify against your standard): steel in seawater
   −0.80 V vs Ag/AgCl/seawater (confirmed, DNV-RP-B401 2010 §5.4); buried steel −0.85 V vs Cu/CuSO₄ (CSE) with IR drop
   considered, or ≥100 mV polarisation shift (ISO 15589 / AMPP criteria (gated: unconfirmed, source is paywalled or blocked)). More negative than about −1.10 V
   (Ag/AgCl) risks hydrogen embrittlement of high-strength steels and coating
   disbondment.
2. **Surface area** A (m²) for each zone (submerged, buried, splash).
3. **Design current density** i (A/m², bare steel). Illustrative magnitudes: seawater
   ~0.06–0.25 A/m² (confirmed: DNV-RP-B401 mean values 0.06–0.12, initial up to 0.25, tabulated by depth and climate); soil ~0.01–0.03 A/m² (gated: unconfirmed, source is paywalled or blocked); seabed mud 0.020 (confirmed).
4. **Coating breakdown factor** fc (0 = perfect, 1 = bare), increasing with time; take
   from the standard for your coating category. I_c = A · i · fc.
5. **Anode mass** for mean current over design life t (years):
   M = I_mean · t · 8760 / (u · ε), where u = utilisation factor (0.80–0.90 per DNV-RP-B401 Table 10-8: 0.90 long slender stand-off, 0.85 short, 0.80 short flush-mounted) and ε = electrochemical capacity.

| Anode | Driving potential vs steel | Capacity ε (Ah/kg), typical design |
|---|---|---|
| Al-Zn-In | ~0.25 V (−1.05 V closed circuit vs −0.80 V) | 2000 in seawater, 1500 in sediment (DNV design values; ≥2500 is the minimum for qualified material) |
| Zinc | ~0.20 V (−1.00 V closed circuit vs −0.80 V) | 780 in seawater, 700 in sediment (DNV design values) |
| Magnesium (high-potential) | ~0.7–0.9 V (gated: unconfirmed, source is paywalled or blocked) | ~1100–1200 (≈50% efficiency) (gated: unconfirmed, source is paywalled or blocked) |

Mg suits high-resistivity soils and fresh water; Al and Zn suit seawater and low-
resistivity environments. Zinc can passivate above ~50 °C (gated: unconfirmed, source is paywalled or blocked).
6. **Check current output** at end of life: I_a = ΔE / R_a, using an anode resistance
   formula (e.g. Dwight's for a slender anode) with environment resistivity. Number of
   anodes N must satisfy both mass and current (initial and final) — take the larger.

## Gotchas
- **Stray current** from DC traction or welding sets causes rapid local attack that
  CP design does not address; survey for it.
- Isolation joints with an anode-side CP system can shift corrosion to the unprotected
  side.
- **Stainless in crevices** corrodes regardless of the series position; galvanic
  rules do not cover crevice or pitting corrosion.
- Reference-electrode type changes the numbers by roughly 0.05–0.1 V (CSE vs Ag/AgCl) (gated: unconfirmed, source is paywalled or blocked); always
  state the reference.
- Pipelines, tanks and offshore structures require a qualified CP engineer and the
  governing code/regulator; this is a preliminary estimate only.

## Verify
- [ ] Every dissimilar contact listed with its potential gap, area ratio and environment.
- [ ] Mitigation never leaves a small coated-only anode next to a large bare cathode.
- [ ] CP current uses the standard's current density and coating breakdown for each life stage.
- [ ] Anode count satisfies both mass and end-of-life current output.
- [ ] Commissioning survey (potential readings with stated reference electrode) planned.
