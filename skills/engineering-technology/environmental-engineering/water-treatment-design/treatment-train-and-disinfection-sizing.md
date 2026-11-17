---
id: engineering-technology.environmental-engineering.water-treatment-design.treatment-train-and-disinfection-sizing
name: treatment-train-and-disinfection-sizing
category: engineering-technology
field: environmental-engineering
product: water-treatment-design
tags: [environmental-engineering, water-treatment-design, drinking-water, potable-water, treatment-train, coagulation, flocculation, velocity-gradient, sedimentation, overflow-rate, rapid-gravity-filter, dual-media-filter, filtration, backwash, disinfection, ct-value, chlorination, baffling-factor, log-removal, giardia, cryptosporidium, membrane-filtration, ultrafiltration, reverse-osmosis, flux, disinfection-by-products, surface-water-treatment-rule, jar-test]
level: practitioner
status: gated
description: "Select and size a drinking-water treatment train: coagulation/flocculation G and t, settling and filter loading rates, CT disinfection with baffling factors, membrane flux."
sources: ["MWH (Crittenden et al.), Water Treatment: Principles and Design", "AWWA, Water Quality and Treatment", "US EPA, LT1ESWTR Disinfection Profiling and Benchmarking Guidance Manual", "Great Lakes-Upper Mississippi River Board, Recommended Standards for Water Works (Ten States Standards)", "Davis, Water and Wastewater Engineering"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Treatment-train selection and disinfection sizing — from raw water to compliant CT

**Goal:** pick a treatment train that meets the pathogen log-removal and chemical
targets for a given raw water, and size the unit processes with defensible loading
rates. Drinking water is safety-critical: the final design must be produced and
signed off by a licensed/competent engineer under the governing regulator's rules.

## 1. Characterise the source, then pick the train
Collect at least a year of turbidity, TOC/UV254, colour, alkalinity, pH, temperature,
iron/manganese, algae and microbial data (peaks matter more than means).

| Raw water | Typical train |
|---|---|
| Low turbidity (<~10 NTU), low TOC | Direct or in-line filtration, or MF/UF |
| Moderate/variable turbidity, TOC | Conventional: coagulation → flocculation → sedimentation/DAF → filtration |
| Algae, low-density floc | Dissolved air flotation instead of settling |
| High TOC / DBP precursors | Enhanced coagulation, GAC, or NF |
| Brackish/saline, nitrate, hardness | RO/NF after suitable pretreatment |
| Groundwater, Fe/Mn | Oxidation + filtration (greensand/catalytic media) |

Process loading rates, G values, flux and recovery figures below are textbook typical ranges (gated: unconfirmed, source is paywalled or blocked); confirm against MWH, Ten States Standards and vendor data.

## 2. Coagulation and flocculation
- Choose coagulant and dose from **jar tests** across the seasonal range; dose varies
  enormously with water quality.
- Velocity gradient: G = √(P / (μ·V)). Rapid mix G ≈ 600–1000 s⁻¹ for 10–60 s
  (or in-line static mixers). Flocculation G ≈ 20–80 s⁻¹, tapered, 20–30 min total,
  Gt ≈ 10⁴–10⁵.
- Provide at least 3 compartments to limit short-circuiting.

## 3. Clarification and filtration
- Conventional settling: surface overflow rate roughly 1–2.5 m/h; plate/tube settlers
  allow several times more (vendor dependent). DAF typically 10–20 m/h.
- Rapid gravity dual-media filters: about 5–12 m/h filtration rate; check the
  N−1 case (one filter backwashing, one out of service) at peak flow.
- Backwash with air scour then water, to roughly 20–30 % bed expansion; recycle or
  filter-to-waste the first water after backwash.
- Performance target: combined filter effluent ≤0.3 NTU in 95 % of monthly samples and never above 1 NTU
  under US rules (40 CFR 141.173, confirmed), and operators aim for <0.1 NTU. Individual filter turbidity
  monitoring catches the one bad filter.

## 4. Disinfection by the CT method
1. Required log inactivation = total required − credit from physical removal.
   Under the US Surface Water Treatment Rule framework the total is 3-log Giardia,
   4-log virus (confirmed as 99.9 % and 99.99 % in 40 CFR 141.173); conventional treatment typically earns 2.5-log Giardia and 2-log
   virus credit (gated: unconfirmed, source is paywalled or blocked); Cryptosporidium is handled separately (filtration, UV or ozone).
   Other jurisdictions differ — use yours.
2. Effective contact time T10 = baffling factor × (V / Q_peak), at the minimum
   operating level:

   | Baffling | T10/T |
   |---|---|
   | Unbaffled (mixed) | 0.1 |
   | Poor | 0.3 |
   | Average | 0.5 |
   | Superior | 0.7 |
   | Perfect (pipe flow) | 1.0 |

   Factors are the widely published defaults (Walkerton Clean Water Centre, secondary); regulators differ (Pennsylvania assigns other values), so use your regulator's table. A tracer test replaces the assumed factor.
3. CT provided = residual C (mg/L, at the outlet) × T10 (min). Compare with the
   regulatory CT tables at the **lowest temperature and highest pH** you expect.
   Free chlorine CT for Giardia rises steeply with cold water and pH >8 (look up the exact value in your regulator's CT table (gated: unconfirmed, source is paywalled or blocked)); virus CT
   is far lower (single digits for 4-log at moderate temperature).
4. Sum log inactivation across segments if residual is measured at each.

## 5. Membranes
- MF/UF: design flux typically 30–100 L/m²/h depending on water and vendor,
  temperature-corrected to the coldest month; allow for CIP, backwash and an
  integrity test (pressure-decay) for log-removal credit.
- RO: brackish water flux about 15–25 L/m²/h with ~75–85 % recovery; seawater
  ~40–50 % recovery. Limiting recovery is set by scaling (run the antiscalant
  vendor's projection software).

## 6. Residual and by-products
Balance CT against DBPs (US limits: TTHM 80 µg/L, HAA5 60 µg/L, as locational running
annual averages; confirmed in 40 CFR 141.64). Remove precursors before chlorinating, or use chloramine for the
distribution residual after primary disinfection.

## Gotchas
- Using average flow or full-tank volume overstates CT; use peak hourly flow and
  minimum level.
- Cold water slows floc formation and multiplies required CT at the same time.
- Coagulation pH drift (alum consumes alkalinity) ruins both TOC removal and CT.
- Filter ripening spikes after backwash are a classic pathogen-passage window.
- Membrane vendor flux numbers assume their pretreatment; pilot when in doubt.

## Verify
- [ ] Train choice justified against seasonal worst-case raw-water data.
- [ ] Every unit checked at peak flow with one unit out of service.
- [ ] CT calculated at peak flow, minimum level, lowest temperature, highest pH.
- [ ] Log-removal credits and CT tables match the governing regulation.
- [ ] DBP formation assessed; design reviewed and stamped by a licensed engineer.
