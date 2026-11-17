---
id: engineering-technology.environmental-engineering.wastewater-treatment-design.activated-sludge-process-design
name: activated-sludge-process-design
category: engineering-technology
field: environmental-engineering
product: wastewater-treatment-design
tags: [environmental-engineering, wastewater-treatment-design, activated-sludge, sewage-treatment, srt, sludge-age, solids-retention-time, f-m-ratio, food-to-microorganism, mlss, mlvss, aeration, oxygen-demand, sotr, alpha-factor, nitrification, denitrification, biological-nutrient-removal, bnr, secondary-clarifier, solids-flux, state-point-analysis, svi, ras, was, anaerobic-digestion, biosolids, metcalf-and-eddy]
level: practitioner
status: gated
description: "Size an activated-sludge plant: design SRT for nitrification, aeration volume from yield, F:M and MLSS checks, oxygen demand, secondary clarifier loading and sludge wasting."
sources: ["Metcalf & Eddy / AECOM, Wastewater Engineering: Treatment and Resource Recovery", "WEF Manual of Practice No. 8, Design of Water Resource Recovery Facilities", "Grady, Daigger, Love & Filipe, Biological Wastewater Treatment", "US EPA, 40 CFR Part 503 Standards for the Use or Disposal of Sewage Sludge (overview)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Activated-sludge process design — SRT first, everything else follows

**Goal:** size the aeration basin, air system and secondary clarifiers of an
activated-sludge plant so that it meets its BOD, TSS and ammonia (and, if required,
total N) limits at the coldest month and peak loads. The numbers below are textbook
typical ranges; final design needs a licensed engineer and the permit's limits.

## 1. Loads and design conditions
- Build a load table: average, maximum-month and peak-day flow and loads for BOD/COD,
  TSS, TKN, TP. Max-month load (often 1.2–1.5 × average) sizes the biology.
- Fractionate COD (biodegradable soluble/particulate, unbiodegradable) if you will
  run a simulator; the inert particulate fraction dominates sludge production.
- Design temperature = coldest sustained (e.g. two-week) wastewater temperature.

## 2. Choose the design SRT
| Objective | Typical aerobic SRT |
|---|---|
| BOD removal only | 3–6 d |
| Nitrification | ~8–15 d (cold climates longer) |
| BNR (N and P) | ~10–25 d total |
| Extended aeration | 20–30 d |

For nitrification compute the minimum SRT from nitrifier kinetics at design
temperature (growth rate roughly halves per ~10 °C drop; θ ≈ 1.07), then apply a
safety factor of about 1.5–2 for peak TKN loads. Add anoxic mass fraction on top for
denitrification.

## 3. Biomass and volume
Biomass inventory (Metcalf & Eddy form):

X·V = Q·SRT·[ Y(S₀ − S) / (1 + k_d·SRT) + f_d·k_d·Y(S₀ − S)·SRT/(1 + k_d·SRT) + X₀,i ]

with typical heterotroph Y ≈ 0.4–0.6 g VSS/g BOD (≈0.45 g/g bCOD), k_d ≈ 0.06–0.12 d⁻¹
at 20 °C, f_d ≈ 0.15 (textbook values, not checked against the paywalled text (gated: unconfirmed, source is paywalled or blocked)), and X₀,i the influent inert VSS.
Pick MLSS (2,000–4,000 mg/L conventional; up to ~8,000+ for MBR) and solve V.
Checks:
- F:M = Q·S₀ / (V·X_VSS): ~0.2–0.4 kg BOD/kg MLVSS·d conventional, 0.05–0.15 extended.
- HRT 4–8 h conventional, 18–36 h extended aeration.
- Waste sludge: P_x,TSS ≈ X·V / SRT. Control SRT by wasting from the basin or RAS.

## 4. Oxygen and air
R₀ = Q(S₀ − S) − 1.42·P_x,bio + 4.57·Q·NOx (bCOD basis), minus 2.86 g O₂ credit per
g nitrate denitrified. Convert actual to standard oxygen transfer:
SOTR = AOTR / [ α·F·(β·C*_T,H − C)/C*₂₀ · θ^(T−20) ], with θ = 1.024. Typical α for
fine-bubble diffusers 0.4–0.6 (lowest at the basin inlet, at low SRT and with high
surfactant loads; higher at long SRT), fouling factor F ≈ 0.65–0.9, operating DO 1.5–2 mg/L.
Size blowers for peak-day load with the largest unit out of service and the diffuser
grid for min/max airflow per diffuser.

## 5. Alkalinity and nitrogen
Nitrification consumes ~7.14 g CaCO₃ per g NH₄-N; denitrification returns ~3.57 (stoichiometry recomputed: 7.14, 4.57 g O₂/g N, 2.86 g O₂/g NO₃-N, 1.42 g O₂/g cells, all correct; 1.07^10 = 1.97 confirms the halving per 10 °C).
Keep residual alkalinity above ~50–70 mg/L as CaCO₃ or dose. Internal recycle for
pre-anoxic (MLE) denitrification is typically 2–4 × Q.

## 6. Secondary clarifiers
- Surface overflow rate ~16–28 m³/m²·d at average flow, ~40–64 at peak.
- Solids loading ~4–6 kg/m²·h average, ~8 at peak (depends on SVI).
- RAS 25–100 % of Q. Confirm with **state-point analysis** using a settling flux
  curve from measured SVI or stirred SSVI; clarifiers fail on solids, not hydraulics.
- Side water depth ≥ ~4–5 m for large circular units.

## 7. Biosolids
Mesophilic anaerobic digestion at ~35 °C with ≥15 d SRT (a common Class B route under
US Part 503; 15 days at 35 to 55 °C confirmed in 40 CFR 503 Appendix B) destroys ~40–55 % of volatile solids and yields roughly 0.75–1.1 m³
biogas per kg VS destroyed (~60–65 % CH₄) (gated: unconfirmed, source is paywalled or blocked). Check dewatering return-stream ammonia: it
can add 15–25 % to the plant's TKN load.

Design ranges in sections 2, 3, 4 and 6 (SRT, F:M, HRT, alpha, SOR, solids loading, RAS) are textbook typical values from paywalled references (gated: unconfirmed, source is paywalled or blocked); confirm against Metcalf & Eddy, WEF MOP 8 and the permit.

## Gotchas
- Designing at average temperature: nitrification washes out in the first cold month.
- Ignoring the inert particulate fraction underestimates sludge and volume.
- Sizing blowers on average load; diurnal peak oxygen demand can be ~1.5–2 × average.
- Filamentous bulking (high SVI) halves clarifier capacity — provide selectors.
- Return streams from dewatering are a hidden N and P load.

## Verify
- [ ] Design SRT ≥ safety factor × minimum nitrifier SRT at coldest temperature.
- [ ] F:M, HRT and MLSS fall in the ranges for the chosen process.
- [ ] Oxygen and blowers sized for peak load, largest blower out of service.
- [ ] State-point analysis passes at peak flow with design SVI.
- [ ] Mass balance closes for solids, N and alkalinity; reviewed by a licensed engineer.
