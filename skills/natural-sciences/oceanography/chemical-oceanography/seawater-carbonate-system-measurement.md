---
id: natural-sciences.oceanography.chemical-oceanography.seawater-carbonate-system-measurement
name: seawater-carbonate-system-measurement
category: natural-sciences
field: oceanography
product: chemical-oceanography
tags: [chemical-oceanography, carbonate-chemistry, carbonate-system, dic, dissolved-inorganic-carbon, total-alkalinity, ta, ph, total-scale, pco2, aragonite-saturation, omega, ocean-acidification, co2sys, pyco2sys, seacarb, crm, dickson-crm, mercuric-chloride, sop, sampling, titration, spectrophotometric-ph, dissociation-constants]
level: practitioner
status: verified
description: "Sample, measure and calculate the seawater CO2 system: DIC/TA bottle sampling and poisoning, CRMs, pH scales, choosing the input pair and constants in CO2SYS/PyCO2SYS, and error budgets."
sources: ["Dickson, Sabine & Christian (eds.) 2007, Guide to Best Practices for Ocean CO2 Measurements (PICES Special Publication 3)", "Riebesell et al. 2010, Guide to best practices for ocean acidification research", "PyCO2SYS documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Seawater carbonate system measurement

**Goal:** carbonate-system data good enough for ocean acidification and carbon-budget
work: collected without gas exchange, calibrated against reference materials, and
computed with stated constants.

## 1. The system in one paragraph
Four measurable parameters — **DIC** (dissolved inorganic carbon), **TA** (total
alkalinity), **pH** and **pCO2** (or fCO2). Measure any two (plus temperature, salinity,
pressure, and ideally silicate and phosphate) and calculate the rest, including the
aragonite/calcite saturation states (Ω). Which pair you measure affects the uncertainty
of what you compute.

## 2. Sampling DIC/TA from a Niskin (SOP-style)
1. Draw carbonate samples **early** — right after gases like O2 (before salts, nutrients).
2. Clean borosilicate glass bottles (typically ~250–500 mL) with ground-glass stoppers.
3. Fill from the bottom with a tube, no bubbles; rinse first, overflow at least half and preferably one full bottle volume (Dickson et al. 2007, SOP 1). A typical carbon order is fCO2, pH, DIC, then TA.
4. Leave a small **headspace** (~1% of volume) for thermal expansion.
5. **Poison** with saturated mercuric chloride (a small volume, e.g. ~0.02–0.05% of sample
   volume) to stop biological activity. HgCl2 is toxic: gloves, labelled waste, follow
   local disposal rules. *Some labs now analyse quickly instead or use alternatives.*
6. Grease stopper (Apiezon L), secure with a band/clip, store cool and dark.

## 3. Measurement
- **DIC:** acidification and coulometric (SOMMA-type) or infrared (NDIR) detection of
  extracted CO2. Precision of ~1–2 µmol/kg is achievable.
- **TA:** open-cell potentiometric titration with HCl, fitted by non-linear least squares.
- **pH:** spectrophotometric with purified m-cresol purple (impure dye biases results);
  report on the **total scale** at a stated temperature (often 25 °C).
- **Certified Reference Materials** (Dickson CRMs) every run: correct to the certified
  DIC/TA values; track CRM results on a control chart.
- Run duplicates on a subset of samples (~10%).

## 4. Calculation (CO2SYS family)
```python
import PyCO2SYS as pyco2
r = pyco2.sys(par1=2300, par2=2050, par1_type=1, par2_type=2,   # TA, DIC in µmol/kg
              salinity=35, temperature=25, temperature_out=12, pressure_out=500,
              total_silicate=10, total_phosphate=1,
              opt_k_carbonic=10, opt_pH_scale=1)                  # Lueker 2000, total scale
r["saturation_aragonite"], r["pH_total_out"]
```
- State the **dissociation constants** (K1, K2; `opt_k_carbonic=10` is Lueker et al. 2000, used above;
  other sets suit for low salinity or cold waters), KSO4,
  and total-boron formulation. *Recommendations evolve; check current best practice.*
- Include nutrients — silicate and phosphate contribute to TA.
- Units: µmol/kg (per kg seawater), not µmol/L. Convert with density.
- Use the uncertainty propagation (PyCO2SYS `uncertainty_from`) to report errors on
  computed Ω or pCO2.

## 5. Choosing the measured pair
TA–DIC is the common pair for bottle samples. Calculating pCO2 from TA–DIC amplifies
errors (PyCO2SYS 1.8.3 at TA 2300, DIC 2050, 25 °C: 2 µmol/kg uncertainty in each gives u(pCO2) about 1.3 %, 6.8 of 509 µatm; more with larger errors); if pCO2 matters, measure it or pH directly. Over-determination (3+
parameters) checks internal consistency.

## Gotchas
- Bubbles or delayed sampling → CO2 exchange, ruined DIC.
- Mixing pH scales (NBS/free/seawater/total) — at pH 8.0 total, S 35, 25 °C: SWS 7.99, free 8.11, NBS 8.14 (PyCO2SYS).
- Coastal/estuarine water: organic alkalinity breaks the standard TA model.
- Forgetting to recompute at in-situ temperature and pressure.

## Verify
- [ ] Sampling log shows draw order, overflow, headspace and poisoning.
- [ ] CRM recoveries within lab control limits each run.
- [ ] pH scale and temperature stated; constants named in the methods.
- [ ] Computed values at in-situ T and P, with propagated uncertainty.
- [ ] Duplicates agree within method precision.
