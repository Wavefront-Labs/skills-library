---
id: engineering-technology.environmental-engineering.solid-waste-engineering.landfill-cell-leachate-and-gas-design
name: landfill-cell-leachate-and-gas-design
category: engineering-technology
field: environmental-engineering
product: solid-waste-engineering
tags: [environmental-engineering, solid-waste-engineering, landfill, landfill-design, landfill-cell, airspace, composite-liner, hdpe-geomembrane, compacted-clay-liner, gcl, leachate, leachate-collection, help-model, water-balance, giroud-equation, landfill-gas, lfg, methane, landgem, gas-collection, gas-wells, flare, final-cover, capping, subtitle-d, landfill-directive, municipal-solid-waste, msw]
level: practitioner
status: gated
description: "Design a municipal landfill cell: airspace and phasing, composite liner, leachate generation (HELP water balance) and drainage spacing, and first-order gas generation and collection."
sources: ["Tchobanoglous, Theisen & Vigil, Integrated Solid Waste Management", "Qian, Koerner & Gray, Geotechnical Aspects of Landfill Design and Construction", "US EPA, Hydrologic Evaluation of Landfill Performance (HELP) Model documentation", "US EPA, Landfill Gas Emissions Model (LandGEM) User's Guide", "US 40 CFR Part 258 (Subtitle D) criteria for MSW landfills", "EU Council Directive 1999/31/EC on the landfill of waste"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Landfill cell, leachate and gas design — contain it, drain it, capture it

**Goal:** lay out a landfill cell with enough airspace for its design life, a lining
and leachate system that keeps head on the liner low, and a gas system that captures
methane safely. Liner and cap minimums are regulatory and jurisdiction-specific; final
design needs a qualified engineer and regulator approval.

## 1. Airspace and phasing
- Required airspace = annual tonnage ÷ in-place density × (1 + cover allowance).
  Typical in-place MSW density with modern compactors ~0.8–1.0 t/m³ (gated: unconfirmed, source is paywalled or blocked) (lower with
  poor compaction); daily/intermediate cover takes ~10–20 % of airspace (less with
  alternative covers such as tarps or foam).
- Phase cells so each is filled in roughly 1–3 years: smaller open area = less
  leachate. Grade the base ≥2 % (often 2–5 %) towards sumps; check post-settlement
  slopes as the subgrade consolidates.
- Side slopes of waste typically no steeper than about 3H:1V; check global and
  veneer stability (geomembrane/soil interfaces govern — use site-specific shear tests).

## 2. Lining system
| Regime | Typical minimum (check current rule) |
|---|---|
| US MSW (Subtitle D) | Composite: FML of at least 30 mil (60 mil if HDPE, i.e. 1.5 mm) over at least 2 ft (0.6 m) compacted soil with k ≤ 1×10⁻⁷ cm/s, leachate depth kept below 30 cm (all confirmed in 40 CFR 258.40) |
| EU non-hazardous (Landfill Directive) | Geological barrier k ≤ 1×10⁻⁹ m/s and ≥1 m thick (confirmed, Directive 1999/31/EC Annex I 3.2) or equivalent, plus artificial liner and drainage layer ≥0.5 m (drainage thickness not confirmed (gated: unconfirmed, source is paywalled or blocked)) |

A GCL may replace clay where the regulator accepts equivalence. Protect the
geomembrane with a geotextile cushion sized against puncture by the drainage stone.
Construction quality assurance (seam testing, electrical leak location) is as important
as the specification.

## 3. Leachate generation — water balance
HELP-style balance over each phase:
Percolation L = P − R − ET − ΔS (precipitation minus runoff, evapotranspiration and
change in storage, including the waste's absorptive capacity until field capacity).
- Model **open active cell** (worst case, little runoff), **intermediate cover** and
  **final cap** conditions separately; peak daily and peak monthly leachate rates size
  pipes, pumps and storage, annual volumes size treatment.
- Use long-term local climate records, not a single average year.

## 4. Leachate collection layout
Maximum head on the liner between collection pipes depends on impingement rate,
drainage-layer permeability, slope and pipe spacing (Giroud or McEnroe solutions; HELP
reports it too). Typical choices:
- Granular drainage layer k ≥ 1×10⁻² cm/s (often 1×10⁻¹ or coarser gravel), or a
  geocomposite with a reduced long-term transmissivity (apply creep, intrusion and
  clogging reduction factors).
- Perforated HDPE pipes, often 150–200 mm, spacing from the head calculation
  (commonly tens of metres); cleanout access at both ends; check pipe deflection and
  buckling under full waste height.
- Biological and chemical clogging (calcium carbonate) of fine media is the classic
  long-term failure — use coarse, carbonate-poor stone around pipes.

## 5. Landfill gas generation and collection
- First-order decay (LandGEM form): Q_CH₄ = Σ k·L₀·Mᵢ·e^(−k·t), summed over annual
  waste masses Mᵢ (computed in tenths of a year). US EPA defaults include
  k = 0.05 yr⁻¹ and L₀ = 170 m³ CH₄/Mg (Clean Air Act defaults) and inventory values of
  k ≈ 0.04 and L₀ ≈ 100 (confirmed in the LandGEM v2.0 manual and EPA presentations; check v3.x defaults); arid sites use lower k (~0.02). Use site data where possible.
- LFG is roughly 50–55 % CH₄ and 45–50 % CO₂ by volume.
- Vertical wells at roughly 30–60 m spacing (overlapping radius of influence) plus
  horizontal collectors in active cells; slope headers ≥3 % (more where settlement is
  large) to condensate knockouts.
- Collection efficiency: roughly 50–90 % depending on cover type and system coverage —
  regulators publish defaults.
- Destruction: enclosed flares (combustion typically ≥ ~1,000 °C with defined residence
  time in UK/EU guidance) or engines; monitor perimeter probes for methane migration
  (explosive range roughly 5–15 % CH₄ in air (gated: unconfirmed, source is paywalled or blocked)).

## 6. Closure
Final cover typically includes a gas-venting layer, barrier (geomembrane and/or clay
or GCL) and drainage layer under vegetated soil. The US Subtitle D minimum is an infiltration layer of at least 18 in plus an erosion layer of at least 6 in (40 CFR 258.60, confirmed), so about 0.6 m (24 in) of soil in total, of which only the top 6 in must sustain native plants; post-closure care is typically 30 years or more (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Leachate design on annual averages: storms on an open cell overwhelm sumps.
- Ignoring geomembrane interface friction — many landfill slides are on smooth HDPE.
- Gas headers without settlement allowance pond condensate and block the system.
- Over-pulling wells draws in air (O₂ >~5 %) and can start subsurface fires.
- Recirculating leachate accelerates gas generation — redesign the gas system to match.

## Verify
- [ ] Airspace and fill sequence meet the design life with realistic density.
- [ ] Liner meets or exceeds the governing regulation; CQA plan specified.
- [ ] Leachate peak and annual volumes modelled for open, intermediate and closed states.
- [ ] Head on liner below the regulatory limit at the chosen pipe spacing.
- [ ] Gas model, well layout, flare capacity and migration monitoring defined.
